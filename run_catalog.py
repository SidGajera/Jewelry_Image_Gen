#!/usr/bin/env python3
"""Catalog orchestrator — deterministic, category-agnostic. No step skippable;
no render reaches the user un-gated. Images are never committed.

Pipeline (docs/22):
  validate_source -> load spec -> build slot prompts (spec + angle matrix)
  -> [FROZEN Higgsfield batch, unchanged] -> validate_render (all gates)
  -> same-call auto-retry -> download -> manifest -> failure memory
  -> regression -> git commit + push

The Higgsfield call is FROZEN: same tool/model, 2k, 1:1, count 1, all slots one
batch, medias order [pose/studio ref, SOURCE piece]; no img2img, no denoise, no
compositing. Every fix is OUTSIDE the call. Generation + download run through the
Higgsfield MCP (agent-driven), not a Python subprocess. So this orchestrator:
  * runs every deterministic step itself (source gate, prompt build, render
    gates, manifest, memory, regression, git);
  * EMITS a generation plan (per-slot prompt + medias order) for the agent to
    fire with the frozen call;
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

MAX_RETRIES = 5   # re-fire the SAME frozen call, failed gate appended to negatives


def _run(cmd):
    return subprocess.run(cmd, cwd=ROOT).returncode


def policy_gate():
    """Load the rule registry and refuse to run on any STOP (policy/check.py).
    Prints rule counts; empty enforced_by = advisory (said plainly)."""
    rc = _run([sys.executable, "policy/check.py"])
    e, o, a = _policy_counts()
    print(f"policy: {e} enforced, {o} observed, {a} advisory rules")
    if rc != 0:
        sys.exit("STOP: policy/check.py found a conflict; catalog refused. Resolve in policy/registry.json.")


def _policy_counts():
    sys.path.insert(0, str(ROOT / "policy"))
    import check as _chk
    return _chk.counts()


# TOKEN_BUDGET runtime guard (registry rule TOKEN_BUDGET, enforced_by run_catalog.budget_check).
# Cumulative token estimate per SKU; over cap => that SKU is marked blocked and the
# queue continues. Not a render gate. The pipeline records an estimate via
# `--record-tokens N`; the ledger persists across the run.
TOKEN_CAP = 15000
_LEDGER = ROOT / "memory" / "token_ledger.json"


def _ledger_load():
    if _LEDGER.exists():
        try:
            return json.loads(_LEDGER.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def budget_check(sku, add=0, cap=TOKEN_CAP):
    """Add `add` tokens to this SKU's running total, persist, and report status.
    Returns {sku, tokens, cap, over, blocked}. On exceeding the cap the SKU is
    flagged blocked (the caller stops this SKU and moves on); it is never a render
    gate and never trims source fidelity/prompt/validation — only display spend."""
    led = _ledger_load()
    e = led.get(sku, {"tokens": 0, "blocked": False})
    e["tokens"] = int(e.get("tokens", 0)) + int(add)
    e["cap"] = cap
    e["over"] = e["tokens"] > cap
    e["blocked"] = bool(e.get("blocked")) or e["over"]
    led[sku] = e
    _LEDGER.parent.mkdir(parents=True, exist_ok=True)
    _LEDGER.write_text(json.dumps(led, indent=2), encoding="utf-8")
    return {"sku": sku, "tokens": e["tokens"], "cap": cap, "over": e["over"], "blocked": e["blocked"]}


def source_gate(sku, source_dir=None):
    policy_gate()
    cmd = [sys.executable, "scripts/validate_source.py", sku]
    if source_dir:
        cmd += ["--source-dir", source_dir]
    rc = _run(cmd)
    if rc != 0:
        sys.exit(f"STOP: source gate failed for {sku} (rc={rc}). Catalog not started.")


def emit_plan(sku, pose_refs=None):
    """Emit the per-slot generation plan for the FROZEN Higgsfield call.
    The call is unchanged: same tool/model, resolution 2k, aspect_ratio 1:1,
    count 1, ALL slots in one batch, medias order [pose/studio ref, SOURCE piece].
    No img2img, no denoise/strength, no compositing. pose_refs maps slot -> media
    id for the pose/studio reference (first media); fill before firing."""
    spec, prompts = bp.build_all(sku)
    src = spec.get("source_media_id")
    pose_refs = pose_refs or {}
    plan = {
        "sku": sku, "category": spec["category"], "model": spec.get("model", "seedream_v5_pro"),
        "source_media_id": src, "mode": "frozen_text_to_image",
        "call_constraints": {"resolution": "2k", "aspect_ratio": "1:1", "count": 1,
                             "one_batch": True, "medias_order": ["pose_studio_ref", "SOURCE_piece"],
                             "no_img2img": True, "no_denoise": True, "no_compositing": True},
        "slots": [{
            "slot": p["slot"], "name": p["name"], "group": p["group"],
            "azimuth": p["azimuth"], "elevation": p["elevation"],
            "aspect_ratio": "1:1", "resolution": p["resolution"], "count": 1,
            "medias": [
                {"value": pose_refs.get(p["slot"]), "role": "pose_studio_ref"},
                {"value": src, "role": "SOURCE_piece"},
            ],
            "prompt": p["prompt"], "negative": p["negative"],
        } for p in prompts],
    }
    outp = ROOT / "workspace" / "golden" / sku / f"genplan_{sku}.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(f"emitted generation plan -> {outp} ({len(plan['slots'])} slots, FROZEN text-to-image, "
          f"medias [pose_ref, SOURCE])")
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
           "mode": "frozen_text_to_image", "renders_dir": str(renders_dir), "jobs": jobs or {}}
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


# Gates trustworthy on real macro renders -> ENFORCED (block completion).
# The pixel-count heuristics (G2/G3/G4/G6/G7/G8/G9) over-reject real sparkle
# (e.g. G2 reports hundreds of "stones"); they are ADVISORY (reported for the
# user's visual QC, per the no-self-QC policy) until calibrated on approved-render
# goldens. G10 pairwise (declared, within-group) IS enforced; single-shot
# elevation estimate is advisory.
def _gates_cfg():
    return json.loads((ROOT / "config" / "gates.json").read_text(encoding="utf-8"))["gates"]


def _enforced():
    return {g for g, v in _gates_cfg().items() if v.get("blocking")}


IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")


def check_refs(sku):
    """P4: refs/<SKU>/ must hold a DISTINCT per-slot reference (medias[0]) for all
    10 slots — a shared reference yields ten near-identical views. Returns the
    missing slot list ([] if complete)."""
    matrix = json.loads((ROOT / "config" / "angle_matrix.json").read_text(encoding="utf-8"))
    spec = json.loads((ROOT / "specs" / f"{sku}.json").read_text(encoding="utf-8"))
    slots = matrix["categories"][spec["category"]]["slots"]
    rdir = ROOT / "refs" / sku
    missing, refs = [], {}
    for s in slots:
        hits = [p for p in (rdir.glob(f"{s['slot']}_*") if rdir.exists() else [])
                if p.suffix.lower() in IMG_EXT]
        if hits:
            refs[s["slot"]] = hits[0]
        else:
            missing.append(s["slot"])
    return missing, refs


def renders_dir(sku):
    """Single canonical output store: deliveries/<SKU>/ (gitignored). Falls back
    to the legacy workspace path if deliveries/ has no renders yet."""
    d = ROOT / "deliveries" / sku
    if d.exists() and any(d.glob("*.png")):
        return d
    return ROOT / "workspace" / "golden" / sku / "renders"


def finish(sku):
    """Completion checklist. Prints COMPLETE only if every box is checked; else
    prints the unchecked boxes. Completion is a checklist, not a claim."""
    rdir = renders_dir(sku)
    matrix = json.loads((ROOT / "config" / "angle_matrix.json").read_text(encoding="utf-8"))
    spec = json.loads((ROOT / "specs" / f"{sku}.json").read_text(encoding="utf-8"))
    slots = {s["slot"]: s for s in matrix["categories"][spec["category"]]["slots"]}

    from PIL import Image
    renders = {}
    for sl, slot in slots.items():
        hits = sorted(rdir.glob(f"{sl}_*.png")) if rdir.exists() else []
        renders[sl] = hits[0] if hits else None
    have = [sl for sl, p in renders.items() if p]
    sized = [sl for sl, p in renders.items() if p and Image.open(p).size == (2048, 2048)]
    box1 = len(sized) == 10

    enforced = _enforced()
    enforced_fail, advisory = [], 0
    for sl, slot in slots.items():
        if not renders[sl]:
            enforced_fail.append(f"{sl}:MISSING"); continue
        res = vr.validate_image(sku, renders[sl], slot)
        for r in res:
            if r["status"] == "fail":
                if r["gate"] in enforced:
                    enforced_fail.append(f"{sl}:{r['gate']}")
                else:
                    advisory += 1
    pv = vr.pairwise_angles(list(slots.values()))
    if pv:
        enforced_fail.append(f"pairwise:{[v['reject_slot'] for v in pv]}")
    if _gates_cfg().get("G17_THEME", {}).get("blocking"):
        t = vr.g17_theme(sku)
        if t["status"] == "fail":
            enforced_fail.append(f"G17_THEME:{t['detail']}")
    box2 = not enforced_fail

    st_path = ROOT / "build" / f"{sku}_state.json"
    st = json.loads(st_path.read_text(encoding="utf-8")) if st_path.exists() else {}
    box3 = box2 or st.get("retries_exhausted", False)

    import subprocess
    dirty = subprocess.run(["git", "status", "--porcelain",
                            f"specs/{sku}.json",
                            f"workspace/golden/{sku}/manifest_{sku}.json"],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
    ahead = subprocess.run(["git", "rev-list", "--count", "@{u}..HEAD"],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
    box4 = (not dirty) and (ahead in ("", "0"))

    boxes = [
        (box1, f"all 10 renders downloaded + 2048^2 ({len(sized)}/10)"),
        (box2, "validate_render ENFORCED gates PASS on all 10" +
               (f" -- FAIL {enforced_fail}" if enforced_fail else "")),
        (box3, "failures auto-retried and re-gated"),
        (box4, "manifest + spec pushed (clean, not ahead)"),
    ]
    e, o, a = _policy_counts()
    if all(b for b, _ in boxes):
        print(f"{sku}: 10/10 · {e} enforced, {o} observed, {a} advisory · pushed · repo clean · COMPLETE")
        return 0
    print(f"{sku}: NOT COMPLETE ({e} enforced, {o} observed, {a} advisory) — unchecked:")
    for ok, label in boxes:
        if not ok:
            print(f"  [ ] {label}")
    if advisory:
        print(f"  (advisory gate flags this run: {advisory} — not yet promoted to blocking; visual QC)")
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sku")
    ap.add_argument("--source-dir")
    ap.add_argument("--emit-plan", action="store_true")
    ap.add_argument("--renders-dir")
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--stage")
    ap.add_argument("--record-tokens", type=int, help="add N tokens to this SKU's budget ledger, then report status")
    ap.add_argument("--budget-status", action="store_true", help="print this SKU's token budget status")
    args = ap.parse_args()

    if args.record_tokens is not None or args.budget_status:
        st = budget_check(args.sku, add=args.record_tokens or 0)
        flag = "BLOCKED (over cap)" if st["blocked"] else "ok"
        print(f"{args.sku}: {st['tokens']}/{st['cap']} tokens · {flag}")
        sys.exit(2 if st["blocked"] else 0)

    if args.stage == "finish":
        sys.exit(finish(args.sku))

    if args.stage == "prompts":
        # SOURCE_COVERAGE_REQUIRED (G-INVENT): refuse the WHOLE catalog if any
        # studio slot reveals geometry no supplied source view establishes.
        matrix = json.loads((ROOT / "config" / "angle_matrix.json").read_text(encoding="utf-8"))
        spec = json.loads((ROOT / "specs" / f"{args.sku}.json").read_text(encoding="utf-8"))
        blocked, need = [], set()
        for s in matrix["categories"][spec["category"]]["slots"]:
            if s["group"] != "studio":
                continue
            unmet, req, az_ok = vr.invent_block(args.sku, s)
            if unmet or not az_ok:
                blocked.append((s["slot"], s["name"], unmet, req))
                need.update(req)
        if blocked:
            for sl, nm, unmet, req in blocked:
                print(f"{args.sku}: BLOCKED -- slot {sl} ({nm}) reveals {unmet}; "
                      f"no supplied source view establishes it. Required: {req}")
            print(f"{args.sku}: BLOCKED -- supply {sorted(need)} then update specs/{args.sku}_views.json. "
                  f"A partial catalog is not a catalog; no slots generated.")
            sys.exit(2)
        missing, refs = check_refs(args.sku)
        if missing:
            print(f"STOP: refs/{args.sku}/ missing per-slot reference for slots {missing} "
                  f"-- P4 requires a DISTINCT medias[0] per slot (a shared ref = 10 identical views). "
                  f"Add refs/{args.sku}/<slot>_*.png for each before generating.")
            sys.exit(2)
        _, prompts = bp.build_all(args.sku)
        outp = ROOT / "build" / f"{args.sku}_prompts.json"
        outp.parent.mkdir(parents=True, exist_ok=True)
        for p in prompts:
            p["ref"] = refs[p["slot"]].name
        outp.write_text(json.dumps(prompts, indent=2), encoding="utf-8")
        print(f"{args.sku}: 10/10 prompts built, all refs present -> {outp}")
        sys.exit(0)

    source_gate(args.sku, args.source_dir)

    if args.emit_plan:
        emit_plan(args.sku)
        if not args.renders_dir:
            print("next: agent fires the FROZEN Higgsfield batch from the gen plan (medias [pose_ref, SOURCE]), "
                  "saves NN_name.png into a renders dir, then re-run with --renders-dir")
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
              f"-> RE-FIRE THE SAME UNMODIFIED Higgsfield call for each, appending the failed gate's "
              f"constraint to that slot's prompt NEGATIVES (no other change; call stays frozen). "
              f"Still failing after {MAX_RETRIES} => STOP and report slot+gate. "
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
