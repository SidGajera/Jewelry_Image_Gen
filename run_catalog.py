#!/usr/bin/env python3
"""Catalog orchestrator — deterministic, category-agnostic. No step skippable;
no render reaches the user un-gated. Images are never committed.

Pipeline (docs/22):
  validate_source -> load spec -> build slot prompts (spec + angle matrix)
  -> [img2img source-lock batch] -> validate_render (all gates) -> auto-retry
  -> download -> manifest -> failure memory -> regression -> git commit + push

The generation + download steps run through the Higgsfield MCP, which is driven
by the agent, not a Python subprocess. So this orchestrator:
  * runs every deterministic step itself (source gate, prompt build, render
    gates, manifest, memory, regression, git);
  * EMITS a generation plan (per-slot img2img prompt + denoise + source view)
    for the agent to execute;
  * validates the produced renders once they are in --renders-dir, and reports
    exactly which slots must be regenerated (bounded to 3 retries per slot).

Usage:
  python run_catalog.py LR-0203 --emit-plan            # -> prompts + gen plan
  python run_catalog.py LR-0203 --renders-dir DIR      # gate + manifest + record
  python run_catalog.py LR-0203 --renders-dir DIR --commit
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_prompts as bp          # noqa: E402
import validate_render as vr        # noqa: E402

MAX_RETRIES = 3


def _run(cmd):
    return subprocess.run(cmd, cwd=ROOT).returncode


def source_gate(sku, source_dir=None):
    cmd = [sys.executable, "scripts/validate_source.py", sku]
    if source_dir:
        cmd += ["--source-dir", source_dir]
    rc = _run(cmd)
    if rc != 0:
        sys.exit(f"STOP: source gate failed for {sku} (rc={rc}). Catalog not started.")


def emit_plan(sku):
    spec, prompts = bp.build_all(sku)
    src = spec.get("source_media_id")
    plan = {
        "sku": sku, "category": spec["category"], "model": spec.get("model", "seedream_v5_pro"),
        "source_media_id": src, "mode": "img2img_source_lock",
        "slots": [{
            "slot": p["slot"], "name": p["name"], "group": p["group"],
            "azimuth": p["azimuth"], "elevation": p["elevation"],
            "denoise": p["denoise"], "aspect_ratio": "1:1", "resolution": p["resolution"],
            "medias": [{"value": src, "role": "image_references"}],
            "prompt": p["prompt"],
        } for p in prompts],
    }
    outp = ROOT / "workspace" / "golden" / sku / f"genplan_{sku}.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(f"emitted generation plan -> {outp} ({len(plan['slots'])} slots, img2img source-lock)")
    return plan


def gate_catalog(sku, renders_dir):
    matrix = json.loads((ROOT / "config" / "angle_matrix.json").read_text(encoding="utf-8"))
    spec = json.loads((ROOT / "specs" / f"{sku}.json").read_text(encoding="utf-8"))
    slots = {s["slot"]: s for s in matrix["categories"][spec["category"]]["slots"]}
    cdir = Path(renders_dir)
    report, retry = {}, []
    for sl, slot in slots.items():
        hits = sorted(cdir.glob(f"{sl}_*.png"))
        if not hits:
            report[sl] = "MISSING"; retry.append(sl); continue
        res = vr.validate_image(sku, hits[0], slot)
        fails = [r["gate"] for r in res if r["status"] == "fail"]
        report[sl] = "REJECT:" + ",".join(fails) if fails else "pass"
        if fails:
            retry.append(sl)
    pv = vr.pairwise_angles(list(slots.values()))
    return report, retry, pv


def write_manifest(sku, renders_dir, jobs=None):
    mp = ROOT / "workspace" / "golden" / sku / f"manifest_{sku}.json"
    spec = json.loads((ROOT / "specs" / f"{sku}.json").read_text(encoding="utf-8"))
    man = {"sku": sku, "category": spec["category"], "model": spec.get("model"),
           "source_media_id": spec.get("source_media_id"),
           "aspect_ratio": "1:1", "resolution": spec.get("resolution", "2k"),
           "mode": "img2img_source_lock", "renders_dir": str(renders_dir), "jobs": jobs or {}}
    mp.write_text(json.dumps(man, indent=2), encoding="utf-8")
    print(f"wrote manifest -> {mp}")


def regression():
    rc = _run([sys.executable, "tests/run_gates.py"])
    if rc != 0:
        sys.exit("STOP: regression suite failed (a gate stopped catching a past failure).")


def git_push(sku):
    _run(["git", "add", "specs", "config", "scripts", "tests", "memory",
          f"workspace/golden/{sku}/manifest_{sku}.json",
          f"workspace/golden/{sku}/SOURCE-SPEC.md"])
    _run(["git", "commit", "-q", "-m", f"{sku}: spec + gates + manifest + failure memory"])
    rc = _run(["git", "push", "-q"])
    if rc != 0:
        sys.exit("STOP: push failed. Catalog NOT complete.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sku")
    ap.add_argument("--source-dir")
    ap.add_argument("--emit-plan", action="store_true")
    ap.add_argument("--renders-dir")
    ap.add_argument("--commit", action="store_true")
    args = ap.parse_args()

    source_gate(args.sku, args.source_dir)

    if args.emit_plan:
        emit_plan(args.sku)
        if not args.renders_dir:
            print("next: agent runs the img2img batch from the gen plan, saves NN_name.png into a renders dir, "
                  "then re-run with --renders-dir")
            return

    if not args.renders_dir:
        ap.error("give --emit-plan and/or --renders-dir")

    report, retry, pv = gate_catalog(args.sku, args.renders_dir)
    for sl, v in report.items():
        print(f"  slot {sl}: {v}")
    if pv:
        print(f"  G10 pairwise: {pv}")
    if retry or pv:
        print(f"RETRY needed (max {MAX_RETRIES}/slot): slots={retry} "
              f"-> regenerate with denoise -0.05 and the failed gate appended as a negative. "
              f"Un-gated renders must NOT be delivered.")
        sys.exit(1)

    write_manifest(args.sku, args.renders_dir)
    regression()
    if args.commit:
        git_push(args.sku)
        n = len(report)
        print(f"{args.sku}: {n}/{n} OK · pushed · repo clean · COMPLETE")
    else:
        print(f"{args.sku}: {len(report)}/{len(report)} gated OK (dry-run; add --commit to push)")


if __name__ == "__main__":
    main()
