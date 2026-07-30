#!/usr/bin/env python3
"""Measure each render gate against the golden sets so promotion to BLOCKING is
earned, not guessed (the same PASS+FAIL method that fixed the source gate).

Golden layout:
  tests/golden/cases.json                     -> FAIL cases (id, sku, slot, gate, image, expect:fail)
  tests/golden/pass_<sku>_<slot>/<slot>_case.png + case.json  -> PASS cases ({expect:PASS,sku,slot})

For every gate, over the FULL golden set, it prints:
  TP   -- of that gate's FAIL cases, how many it caught (fail)
  FP   -- of PASS cases, how many it wrongly failed  (MUST be 0 to promote)
  LOWC -- fraction of all cases where it returned unmeasurable/skip

A gate is PROMOTABLE when: FP == 0  AND  caught all its FAIL cases  AND  LOWC < 10%.
calibrate.py NEVER edits gates.json -- it reports; you flip the flag deliberately.

Usage: python scripts/calibrate.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
import validate_render as vr  # noqa: E402

GDIR = ROOT / "tests" / "golden"


def _slot(sku, slotid):
    matrix = json.loads((ROOT / "config" / "angle_matrix.json").read_text(encoding="utf-8"))
    spec = json.loads((ROOT / "specs" / f"{sku}.json").read_text(encoding="utf-8"))
    return {s["slot"]: s for s in matrix["categories"][spec["category"]]["slots"]}[slotid]


def _gate_status(res, gate):
    hits = [r for r in res if r["gate"] == gate]
    if any(h["status"] == "fail" for h in hits):
        return "fail"
    if hits and any(h["status"] in ("unmeasurable",) for h in hits) and not any(h["status"] == "pass" for h in hits):
        return "lowc"
    if hits and all(h["status"] in ("pass", "skip") for h in hits):
        return "pass"
    return "skip"


def collect():
    cases = []
    fc = json.loads((GDIR / "cases.json").read_text(encoding="utf-8"))["cases"]
    for c in fc:
        if c.get("expect") == "pass":
            continue  # PASS goldens live in pass_<sku>_<slot>/ dirs, not the FAIL-case file
        img = GDIR / c["image"] if c.get("image") else None
        if img and img.exists():
            cases.append({"expect": "fail", "sku": c["sku"], "slot": c["slot"],
                          "target": c["gate"], "image": img})
    for d in sorted(GDIR.glob("pass_*")):
        cj = d / "case.json"
        if not cj.exists():
            continue
        meta = json.loads(cj.read_text(encoding="utf-8"))
        imgs = [p for p in d.glob("*_case.png")]
        if imgs:
            cases.append({"expect": "pass", "sku": meta["sku"], "slot": meta["slot"],
                          "target": None, "image": imgs[0]})
    return cases


def main():
    gates_cfg = json.loads((ROOT / "config" / "gates.json").read_text(encoding="utf-8"))["gates"]
    cases = collect()
    n_pass = sum(c["expect"] == "pass" for c in cases)
    n_fail = sum(c["expect"] == "fail" for c in cases)
    print(f"golden set: {n_pass} PASS, {n_fail} FAIL")
    if n_pass == 0:
        print("!! zero PASS goldens -- FALSE-POSITIVE rate is unmeasurable, so NO gate can be promoted.")
        print("   add tests/golden/pass_<sku>_<slot>/ (user-approved renders) across >=2 SKUs, studio+lifestyle.")

    per = {g: {"tp": 0, "fn": 0, "fp": 0, "lowc": 0, "seen": 0} for g in gates_cfg}
    for c in cases:
        res = vr.validate_image(c["sku"], c["image"], _slot(c["sku"], c["slot"]))
        for g in gates_cfg:
            st = _gate_status(res, g)
            per[g]["seen"] += 1
            if st == "lowc":
                per[g]["lowc"] += 1
            if c["expect"] == "pass" and st == "fail":
                per[g]["fp"] += 1
            if c["expect"] == "fail" and c["target"] == g:
                per[g]["tp" if st == "fail" else "fn"] += 1

    print(f"\n{'gate':<18}{'block':<7}{'TP':<7}{'FN':<5}{'FP':<5}{'LOWC%':<7}promotable")
    for g, cfg in gates_cfg.items():
        s = per[g]
        lowc = (s["lowc"] / s["seen"] * 100) if s["seen"] else 0
        promotable = (n_pass > 0 and s["fp"] == 0 and s["fn"] == 0 and (s["tp"] > 0) and lowc < 10)
        print(f"{g:<18}{str(cfg['blocking']):<7}{s['tp']:<7}{s['fn']:<5}{s['fp']:<5}{lowc:<7.0f}"
              + ("YES" if promotable else ("" if cfg["blocking"] else "no")))
    print("\nPromote a gate in config/gates.json only when promotable=YES; then record its rates in memory/failures.json.")


if __name__ == "__main__":
    main()
