#!/usr/bin/env python3
"""Regression suite for scripts/clean_photo.py — the no-AI cleanup pass.

Builds a synthetic plate with the properties of the real shot (dark glossy ground,
soft light band, out-of-focus bokeh, gold band, faceted stone, sensor grain) and
then injects known defects. Because the clean plate is known exactly, every claim
can be measured rather than eyeballed.

Asserted, in order of importance:
  1. the design does not move            — structure F1 at 1px, gradient correlation
  2. nothing is invented                 — no pixel becomes specular outside a repair
  3. defects actually go                 — error at speck sites drops materially
  4. the photograph stays a photograph   — bokeh and grain survive
  5. the guard has teeth                 — over-aggressive settings are REJECTED

Usage:
    python3 tests/test_clean_photo.py
Exit 0 = all invariants hold; 1 = a regression.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "clean_photo.py"
STONE_C, STONE_R = (450, 400), 96
BAND_C = (450, 560)


def build_plate(tmp):
    """Return (defective_path, clean_truth, dust_sites)."""
    rng = np.random.default_rng(3)
    H = W = 900
    img = np.zeros((H, W, 3), np.float32)
    yy = np.linspace(0, 1, H)[:, None]
    img += (8 + 26 * np.exp(-((yy - 0.42) ** 2) / 0.004))[..., None]

    for _ in range(9):                                   # intentional bokeh
        c = (int(rng.integers(60, W - 60)), int(rng.integers(60, int(H * 0.55))))
        r = int(rng.integers(18, 34))
        layer = np.zeros((H, W), np.float32)
        cv2.circle(layer, c, r, 1.0, -1)
        img += cv2.GaussianBlur(layer, (0, 0), r * 0.45)[..., None] * rng.uniform(20, 45)

    band = np.zeros((H, W), np.float32)                  # the design
    cv2.ellipse(band, BAND_C, (150, 130), 0, 200, 340, 1.0, 16)
    img += cv2.GaussianBlur(band, (0, 0), 1.2)[..., None] * np.array([60., 175., 225.], np.float32)
    stone = np.zeros((H, W), np.float32)
    cv2.circle(stone, STONE_C, STONE_R, 1.0, -1)
    img += cv2.GaussianBlur(stone, (0, 0), 1.0)[..., None] * np.array([205., 212., 214.], np.float32)
    facets = np.zeros((H, W), np.float32)
    for a in range(0, 360, 30):
        t = np.deg2rad(a)
        cv2.line(facets, STONE_C,
                 (int(STONE_C[0] + STONE_R * np.cos(t)), int(STONE_C[1] + STONE_R * np.sin(t))), 1.0, 2)
    cv2.circle(facets, STONE_C, 52, 1.0, 2)
    img += cv2.GaussianBlur(facets, (0, 0), 0.6)[..., None] * 34

    img = np.clip(img, 0, 255)
    truth = img.copy()

    dust = []
    for _ in range(70):                                  # dust on the ground
        c = (int(rng.integers(5, W - 5)), int(rng.integers(5, H - 5)))
        if np.hypot(c[0] - STONE_C[0], c[1] - STONE_C[1]) < 110: continue
        if np.hypot(c[0] - BAND_C[0], c[1] - BAND_C[1]) < 165: continue
        cv2.circle(img, c, int(rng.integers(1, 3)), float(rng.integers(70, 150)), -1)
        dust.append(c)
    for _ in range(22):                                  # dust on the piece
        t, rad = rng.uniform(0, 2 * np.pi), rng.uniform(10, 88)
        c = (int(STONE_C[0] + rad * np.cos(t)), int(STONE_C[1] + rad * np.sin(t)))
        cv2.circle(img, c, int(rng.integers(1, 3)), float(rng.integers(70, 130)), -1)
        dust.append(c)

    img += rng.normal(0, 1.7, img.shape)                 # sensor grain
    img = np.clip(img, 0, 255).astype(np.uint8)
    path = tmp / "plate.png"
    cv2.imwrite(str(path), img)
    return path, np.clip(truth, 0, 255).astype(np.uint8), np.array(dust)


def run(src, dst, *extra):
    return subprocess.run([sys.executable, str(SCRIPT), "--in", str(src), "--out", str(dst), *extra],
                          capture_output=True, text=True)


def grain_sigma(bgr, region):
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    return float((g - cv2.GaussianBlur(g, (0, 0), 1.4))[region].std())


def main():
    failures = []

    def check(name, ok, detail):
        print(("  PASS  " if ok else "  FAIL  ") + f"{name}: {detail}")
        if not ok:
            failures.append(name)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        plate, truth, dust = build_plate(tmp)
        out_path, report = tmp / "clean.png", tmp / "r.json"

        r = run(plate, out_path, "--report", str(report))
        if r.returncode != 0:
            print("cleanup run failed:\n" + r.stdout + r.stderr)
            return 1
        import json
        rep = json.loads(report.read_text())
        src = cv2.imread(str(plate)).astype(np.float32)
        out = cv2.imread(str(out_path)).astype(np.float32)
        ref = truth.astype(np.float32)

        print("\n1. the design does not move")
        v = rep["verification"]
        check("structure_f1", v["structure_f1_1px"] >= 0.999,
              f"{v['structure_f1_1px']:.5f} of jewellery edges within 1px of source")
        check("gradient_corr", v["gradient_correlation"] >= 0.999,
              f"{v['gradient_correlation']:.5f}")

        print("\n2. nothing is invented")
        repaired = np.zeros(src.shape[:2], np.uint8)
        for x, y in dust:
            cv2.circle(repaired, (int(x), int(y)), 5, 1, -1)
        newly = (out.max(2) > 245) & (src.max(2) < 200) & ~repaired.astype(bool)
        check("no_invention", int(newly.sum()) == 0,
              f"{int(newly.sum())} pixels became specular outside a repair")

        print("\n3. defects actually go")
        eb, ea = [], []
        for x, y in dust:
            x, y = int(x), int(y)
            sl = (slice(max(0, y - 4), y + 5), slice(max(0, x - 4), x + 5))
            eb.append(np.abs(src[sl] - ref[sl]).mean())
            ea.append(np.abs(out[sl] - ref[sl]).mean())
        on = [i for i, (x, y) in enumerate(dust)
              if np.hypot(x - STONE_C[0], y - STONE_C[1]) < 95]
        off = [i for i in range(len(dust)) if i not in on]
        g_gain = 1 - np.mean([ea[i] for i in off]) / np.mean([eb[i] for i in off])
        p_gain = 1 - np.mean([ea[i] for i in on]) / np.mean([eb[i] for i in on])
        check("ground_dust", g_gain >= 0.35, f"{g_gain * 100:.0f}% closer to the clean plate")
        check("piece_dust", p_gain >= 0.12, f"{p_gain * 100:.0f}% closer to the clean plate")

        print("\n4. the photograph stays a photograph")
        g = cv2.cvtColor(truth, cv2.COLOR_BGR2GRAY).astype(np.float32)
        bok = (g - cv2.GaussianBlur(g, (0, 0), 60) > 8)
        near = np.zeros(g.shape, np.uint8)
        cv2.circle(near, STONE_C, 140, 1, -1)
        bok &= ~near.astype(bool)
        bok[520:, :] = False
        drift = abs(out[..., 1][bok].mean() / src[..., 1][bok].mean() - 1)
        check("bokeh_kept", drift <= 0.01, f"bokeh level moved {drift * 100:.2f}%")
        plain = np.zeros(src.shape[:2], bool)
        plain[700:880, 60:300] = True
        gs, go = grain_sigma(src.astype(np.uint8), plain), grain_sigma(out.astype(np.uint8), plain)
        check("grain_kept", go >= 0.85 * gs, f"grain sigma {gs:.3f} -> {go:.3f}")

        print("\n5. the guard has teeth")
        bad = run(plate, tmp / "bad.png", "--metal-blotch-amp", "60", "--metal-smudge", "1.0")
        check("guard_rejects", bad.returncode == 1 and not (tmp / "bad.png").exists(),
              "over-aggressive settings rejected and nothing written")

    print("\n" + ("FAILED: " + ", ".join(failures) if failures else "ALL INVARIANTS HOLD"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
