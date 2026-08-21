#!/usr/bin/env python3
"""Source-intake gate regression (calibration harness). Runs validate_source
against three golden sets and asserts the gate KEEPS catching known-bad source:
  source_clean_cad/    -> PASS  (the 5 LR-0206 clean CAD views)
  source_watermarked/  -> FAIL via watermark  (tiled-grid overlay)
  source_worn_photo/   -> FAIL via cad_only    (worn/gloved-hand retail photo)
The gate must pass all three before any catalog generates. Images live locally
(gitignored); on a fresh clone with no images a set is reported PENDING.
Exit 0 = all present sets correct; 1 = a regression.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate_source as vs  # noqa: E402

GDIR = ROOT / "tests" / "golden"
CASES = [
    ("source_clean_cad",   True,  None),
    ("source_watermarked", False, "watermark"),
    ("source_worn_photo",  False, "cad_only"),
]


def main():
    fails = pending = 0
    for name, expect_ok, expect_item in CASES:
        d = GDIR / name
        imgs = [p for p in d.glob("*") if p.is_file()] if d.exists() else []
        if not imgs:
            pending += 1
            print(f"PENDING  {name} (no images locally)")
            continue
        res = vs.validate("LR-0206", source_dir=str(d))
        ok = (res["ok"] == expect_ok) and (expect_ok or res.get("item") == expect_item)
        fails += not ok
        got = "PASS" if res["ok"] else f"FAIL:{res.get('item')}"
        print(f"{'OK ' if ok else 'REGRESSION'}  {name:<20} expect={'PASS' if expect_ok else 'FAIL:'+expect_item} got={got}")
    print(f"\n{len(CASES)-fails-pending} ok · {fails} regressions · {pending} pending")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
