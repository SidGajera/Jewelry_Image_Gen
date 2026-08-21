#!/usr/bin/env python3
"""Regression suite — runs the mapped gate against every golden case.

For each case in tests/golden/cases.json that HAS a sample image, run the full
gate set and assert the named gate produced the expected outcome (fail/pass).
A gate that stops catching a past failure => this suite fails => the build fails.
Cases with image=null are PENDING (a real sample must be added) and are listed
but do not fail the build.

Usage:
    python tests/run_gates.py            # assert available cases
    python tests/run_gates.py --strict   # PENDING cases also fail the build
Exit 0 = all available cases correct; 1 = a regression (or PENDING under --strict).
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
import validate_render as vr  # noqa: E402

GDIR = ROOT / "tests" / "golden"


def gate_status(res, gate):
    hits = [r for r in res if r["gate"] == gate]
    if any(h["status"] == "fail" for h in hits):
        return "fail"
    if hits and all(h["status"] == "pass" for h in hits):
        return "pass"
    return "other"  # skip/unmeasurable


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    import make_fixtures
    make_fixtures.make_all()   # deterministic; no fixture images are committed

    cases = json.loads((GDIR / "cases.json").read_text(encoding="utf-8"))["cases"]
    matrix = json.loads((ROOT / "config" / "angle_matrix.json").read_text(encoding="utf-8"))

    passed = regressions = pending = 0
    for c in cases:
        if not c.get("image"):
            pending += 1
            print(f"PENDING  {c['id']:<34} {c['gate']:<18} (no sample image yet)")
            continue
        img = GDIR / c["image"]
        if not img.exists():
            pending += 1
            print(f"PENDING  {c['id']:<34} {c['gate']:<18} (image missing: {c['image']})")
            continue
        spec = json.loads((ROOT / "specs" / f"{c['sku']}.json").read_text(encoding="utf-8"))
        slot = {s["slot"]: s for s in matrix["categories"][spec["category"]]["slots"]}[c["slot"]]
        res = vr.validate_image(c["sku"], img, slot)
        got = gate_status(res, c["gate"])
        ok = (got == c["expect"])
        passed += ok
        regressions += (not ok)
        print(f"{'OK ' if ok else 'REGRESSION'}  {c['id']:<34} {c['gate']:<18} expect={c['expect']} got={got}")

    print(f"\n{passed} ok · {regressions} regressions · {pending} pending-samples")
    if regressions or (args.strict and pending):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
