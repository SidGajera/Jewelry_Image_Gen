#!/usr/bin/env python3
"""Regression suite for scripts/verify_drift.py — the source-vs-render drift check.

A drift check is only worth having if it does two things: stay quiet when the
design did not change, and fire when it did. Both are asserted here against
forgeries built from the same synthetic plate, so the answer is known in advance.

  CONTROL   the deterministic cleanup (design provably untouched)  -> must PASS
  FORGERY 1 stone scaled 1.12x, the classic generative drift       -> must FAIL
  FORGERY 2 round stone squashed to an oval                        -> must FAIL
  FORGERY 3 yellow gold recoloured to white gold                   -> must FAIL

Forgery 1 is the reason `stone_vs_metal_area` exists. Measured as a share of the
whole piece a solitaire's stone already dominates the mask, so a 25% larger stone
moved that number only 3.9% and slipped under any sane threshold. Measured against
the band it moves 40% and is caught. Do not remove that measure.

Usage:
    python3 tests/test_verify_drift.py
Exit 0 = the check has teeth and no false alarm; 1 = a regression.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
from test_clean_photo import build_plate, STONE_C  # noqa: E402

DRIFT = ROOT / "scripts" / "verify_drift.py"
CLEAN = ROOT / "scripts" / "clean_photo.py"


def forge_bigger_stone(src, factor=1.12):
    out = src.copy()
    m = np.zeros(src.shape[:2], np.uint8)
    cv2.circle(m, STONE_C, 118, 1, -1)
    warped = cv2.warpAffine(src, cv2.getRotationMatrix2D(STONE_C, 0, factor),
                            (src.shape[1], src.shape[0]))
    out[m.astype(bool)] = warped[m.astype(bool)]
    return out


def forge_oval(src):
    out = src.copy()
    m = np.zeros(src.shape[:2], np.uint8)
    cv2.circle(m, STONE_C, 118, 1, -1)
    M = np.float32([[1.0, 0, 0], [0, 0.80, STONE_C[1] * 0.20]])
    warped = cv2.warpAffine(src, M, (src.shape[1], src.shape[0]))
    out[m.astype(bool)] = warped[m.astype(bool)]
    return out


def forge_white_gold(src):
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV).astype(np.int16)
    gold = (hsv[:, :, 0] >= 12) & (hsv[:, :, 0] <= 45) & (hsv[:, :, 1] >= 60)
    hsv[:, :, 1][gold] = (hsv[:, :, 1][gold] * 0.25).astype(np.int16)
    return cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)


def main():
    failures = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        plate, _, _ = build_plate(tmp)
        src = cv2.imread(str(plate))

        control = tmp / "control.png"
        r = subprocess.run([sys.executable, str(CLEAN), "--in", str(plate), "--out", str(control)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("cleanup failed, cannot build the control:\n" + r.stdout + r.stderr)
            return 1

        cases = [("control (design untouched)", control, 0)]
        for name, img, want in (("forgery: stone 1.12x", forge_bigger_stone(src), 1),
                                ("forgery: round -> oval", forge_oval(src), 1),
                                ("forgery: yellow -> white gold", forge_white_gold(src), 1)):
            p = tmp / (name.split(":")[-1].strip().replace(" ", "_") + ".png")
            cv2.imwrite(str(p), img)
            cases.append((name, p, want))

        for name, path, want in cases:
            r = subprocess.run([sys.executable, str(DRIFT), "--source", str(plate),
                                "--candidate", str(path)], capture_output=True, text=True)
            ok = r.returncode == want
            verdict = "held" if r.returncode == 0 else "drift detected"
            print(("  PASS  " if ok else "  FAIL  ") + f"{name:<32} -> {verdict}")
            if not ok:
                failures.append(name)
                print("        expected exit %d, got %d" % (want, r.returncode))

    print("\n" + ("FAILED: " + ", ".join(failures) if failures else
                  "DRIFT CHECK HAS TEETH AND RAISES NO FALSE ALARM"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
