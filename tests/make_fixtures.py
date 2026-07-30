#!/usr/bin/env python3
"""Deterministically regenerate the synthetic gate fixtures used by the
regression suite, so NO image needs to be committed. These are crude stand-ins
that prove each gate FIRES; replace any of them with a real approved/rejected
render by dropping the file in tests/golden/ and pointing cases.json at it.
"""
from pathlib import Path
import numpy as np
import cv2

GDIR = Path(__file__).resolve().parent / "golden"
S = 2048


def _blank():
    return np.full((S, S, 3), 245, np.uint8)


def make_all():
    GDIR.mkdir(parents=True, exist_ok=True)
    # G1 pass — square blank
    cv2.imwrite(str(GDIR / "fixture_square_blank.png"), _blank())
    # G1 fail — portrait
    cv2.imwrite(str(GDIR / "bad_portrait.png"), np.full((S, 1536, 3), 245, np.uint8))
    # G9 fail — two separate pieces
    img = _blank()
    cv2.circle(img, (650, 1024), 300, (40, 40, 40), -1)
    cv2.circle(img, (1400, 1024), 300, (40, 40, 40), -1)
    cv2.imwrite(str(GDIR / "fixture_two_pieces.png"), img)
    # G8 fail — hidden halo: plain oval + bright accent row under it on a dark basket
    img = _blank()
    cv2.circle(img, (1024, 1024), 300, (30, 30, 30), 44)
    cv2.ellipse(img, (1024, 900), (150, 215), 0, 0, 360, (250, 250, 250), -1)
    cv2.rectangle(img, (int(0.28 * S), int(0.53 * S)), (int(0.72 * S), int(0.63 * S)), (25, 25, 25), -1)
    for x in np.linspace(0.31 * S, 0.69 * S, 16).astype(int):
        cv2.circle(img, (int(x), int(0.58 * S)), 8, (255, 255, 255), -1)
    cv2.imwrite(str(GDIR / "fixture_hidden_halo.png"), img)
    print(f"regenerated fixtures in {GDIR}")


if __name__ == "__main__":
    make_all()
