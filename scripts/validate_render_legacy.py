#!/usr/bin/env python
"""Automated pre-delivery QC for catalog renders.

Runs the checks that can be decided from pixels alone, so a batch run does not
need a human to eyeball every frame. Anything this script cannot decide is
reported as UNKNOWN rather than silently passed - it never invents a verdict.

Gates implemented here (see docs/11, docs/18, prompts/07):
  velvet      background reads as plush velvet, not flat/woven cloth  [docs/11]
  whitebal    cloth is neutral white, no warm/cream/tinted cast        [docs/11]
  exposure    no blown-out clipping across the stones                  [prompts/07 P2]
  centered    ring centered horizontally and vertically                [prompts/07]
  geometry    stone-run signature vs the SKU source (front views only) [docs/13]

Usage:
    python scripts/validate_render.py RENDER.png [--source SOURCE.png] [--json]

Exit code 0 = all implemented gates passed, 1 = at least one FAIL.
"""
from __future__ import annotations

import argparse
import json
import sys

import numpy as np
from PIL import Image

# --- thresholds -------------------------------------------------------------
# Calibrated against the approved reference plates (Offie_photoshoot 1-5) and
# the locked failure records in config/QUALITY_MEMORY.json.
WARM_CAST_MAX = 6.0     # mean (R-B) over cloth pixels; above this reads cream/warm
SAT_NEUTRAL_MAX = 14.0  # mean saturation over cloth pixels
CLIP_FRAC_MAX = 0.020   # fraction of frame at 255 in all channels
VELVET_SOFT_MIN = 0.55  # pile softness score; woven/flat cloth scores lower
CENTER_TOL = 0.06       # allowed offset of ring centroid from frame centre


def _load(path: str) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB")).astype(np.float64)


def _cloth_mask(a: np.ndarray) -> np.ndarray:
    """Bright, low-saturation, non-metal pixels - i.e. the background cloth."""
    mx, mn = a.max(2), a.min(2)
    sat = mx - mn
    return (mx > 120) & (sat < 60)


def _jewel_mask(a: np.ndarray) -> np.ndarray:
    """Gold metal: warm, saturated, mid-to-bright."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 90) & (r - b > 28) & (r >= g)


def check_whitebalance(a: np.ndarray) -> dict:
    m = _cloth_mask(a)
    if m.sum() < 5000:
        return {"gate": "whitebal", "verdict": "UNKNOWN", "detail": "cloth not found"}
    r, g, b = a[..., 0][m], a[..., 1][m], a[..., 2][m]
    warm = float((r - b).mean())
    sat = float((np.maximum(r, np.maximum(g, b)) - np.minimum(r, np.minimum(g, b))).mean())
    ok = warm <= WARM_CAST_MAX and sat <= SAT_NEUTRAL_MAX
    return {
        "gate": "whitebal",
        "verdict": "PASS" if ok else "FAIL",
        "warm_rb": round(warm, 2),
        "sat": round(sat, 2),
        "detail": "neutral white" if ok else "warm/tinted cast - run whiten_cloth.py (0 credits)",
    }


def check_velvet(a: np.ndarray) -> dict:
    """Velvet has a soft dense pile: fine high-frequency noise with low contrast
    and no periodic weave. Cotton/linen show a regular weave grid; a flat sheet
    shows almost no micro-texture at all."""
    m = _cloth_mask(a)
    if m.sum() < 5000:
        return {"gate": "velvet", "verdict": "UNKNOWN", "detail": "cloth not found"}
    lum = a.mean(2)
    # local micro-contrast via a 3x3 laplacian on cloth regions only
    lap = (
        4 * lum[1:-1, 1:-1]
        - lum[:-2, 1:-1] - lum[2:, 1:-1] - lum[1:-1, :-2] - lum[1:-1, 2:]
    )
    mm = m[1:-1, 1:-1]
    micro = np.abs(lap[mm])
    if micro.size < 1000:
        return {"gate": "velvet", "verdict": "UNKNOWN", "detail": "insufficient cloth"}
    fine = float(np.percentile(micro, 75))
    harsh = float(np.percentile(micro, 99))
    # velvet: present but gentle micro-texture. weave: harsh periodic edges.
    # flat sheet: fine ~ 0.
    softness = 0.0 if harsh <= 0 else float(1.0 - min(1.0, fine / max(harsh, 1e-6)))
    textured = fine > 0.6
    ok = textured and softness >= VELVET_SOFT_MIN
    if not textured:
        detail = "cloth reads flat/texture-less - not velvet"
    elif softness < VELVET_SOFT_MIN:
        detail = "harsh periodic texture - reads woven (cotton/linen), not velvet pile"
    else:
        detail = "soft dense pile consistent with velvet"
    return {
        "gate": "velvet",
        "verdict": "PASS" if ok else "FAIL",
        "fine": round(fine, 3),
        "softness": round(softness, 3),
        "detail": detail,
    }


def check_logo_natural(a: np.ndarray) -> dict:
    """A logo printed INTO velvet shares the cloth's shading: the pile's folds
    still modulate it. A pasted/sticker logo sits on a locally flat patch and
    often brings a lighter 'white box' with it.

    Returns PASS (natural), FAIL (artificial - remove it and ship plain velvet
    per docs/11 fallback), or UNKNOWN when no gold ink is found, which is the
    plain-velvet case and is itself compliant.
    """
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = a.mean(2)
    cloth = _cloth_mask(a)
    # gold ink on white cloth: warm but far less saturated/dark than 18K metal
    ink = _ink_mask(a)
    if ink.sum() < 1500:
        return {"gate": "logo_natural", "verdict": "UNKNOWN",
                "detail": "no logo ink detected - plain velvet (compliant under the fallback)"}

    ys, xs = np.nonzero(ink)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    box = lum[y0:y1 + 1, x0:x1 + 1]
    boxcloth = cloth[y0:y1 + 1, x0:x1 + 1] & ~ink[y0:y1 + 1, x0:x1 + 1]
    if boxcloth.sum() < 500:
        return {"gate": "logo_natural", "verdict": "UNKNOWN", "detail": "logo region too dense to judge"}

    # 1) white-box test: cloth inside the logo box should not be brighter than
    #    cloth elsewhere - a pasted asset usually carries a lighter plate.
    outside = cloth.copy()
    outside[y0:y1 + 1, x0:x1 + 1] = False
    if outside.sum() < 2000:
        return {"gate": "logo_natural", "verdict": "UNKNOWN", "detail": "not enough surrounding cloth"}
    lift = float(box[boxcloth].mean() - lum[outside].mean())

    # 2) shading test: fold shading must continue across the logo. If the cloth
    #    under the logo is flatter than the cloth around it, the logo is pasted.
    var_in = float(box[boxcloth].std())
    var_out = float(lum[outside].std())
    flatness = var_in / var_out if var_out > 1e-6 else 1.0

    natural = lift <= 6.0 and flatness >= 0.45
    if lift > 6.0:
        detail = "logo sits on a lighter patch (white-box) - reads pasted"
    elif flatness < 0.45:
        detail = "cloth under logo is flatter than surrounding pile - reads overlaid"
    else:
        detail = "logo shares the velvet's shading - reads naturally printed"
    return {
        "gate": "logo_natural",
        "verdict": "PASS" if natural else "FAIL",
        "box_lift": round(lift, 2),
        "flatness": round(flatness, 3),
        "detail": detail if natural else detail + " - remove logo, ship PLAIN velvet (docs/11 fallback)",
    }


def _ink_mask(a: np.ndarray) -> np.ndarray:
    """Gold logo ink printed on cloth.

    Calibrated against the reference plates: plain white velvet sits at
    R-B ~ -3, gold logo ink at R-B ~ +20..+40. The ring's own gold must be
    excluded explicitly - without that, its highlights fall inside the cloth
    mask and the 'logo' reads as ~15% of the frame when the real logo is ~2%.
    """
    r, b = a[..., 0], a[..., 2]
    lum = a.mean(2)
    return _cloth_mask(a) & ~_jewel_mask(a) & (r - b > 20) & (r - b < 70) & (lum > 120)


def check_jewelry_hero(a: np.ndarray) -> dict:
    """The jewelry must be the clear focus. Two ways that fails: the ring is not
    the sharpest thing in frame, or the logo has grown big enough to compete."""
    jewel, ink = _jewel_mask(a), _ink_mask(a)
    if jewel.sum() < 2000:
        return {"gate": "jewelry_hero", "verdict": "UNKNOWN", "detail": "ring not found"}

    lum = a.mean(2)
    lap = (
        4 * lum[1:-1, 1:-1]
        - lum[:-2, 1:-1] - lum[2:, 1:-1] - lum[1:-1, :-2] - lum[1:-1, 2:]
    )
    jm, bgm = jewel[1:-1, 1:-1], (~jewel & ~ink)[1:-1, 1:-1]
    if jm.sum() < 500 or bgm.sum() < 500:
        return {"gate": "jewelry_hero", "verdict": "UNKNOWN", "detail": "masks too small"}

    # focus: the ring should carry markedly more detail energy than the backdrop
    sharp_ratio = float(np.abs(lap[jm]).mean() / max(np.abs(lap[bgm]).mean(), 1e-6))
    ink_vs_jewel = float(ink.sum() / max(jewel.sum(), 1))

    ok = sharp_ratio >= 1.6 and ink_vs_jewel <= 0.60
    if sharp_ratio < 1.6:
        detail = "ring is not distinctly sharper than the background - jewelry is not the hero"
    elif ink_vs_jewel > 0.60:
        detail = "logo covers too much relative to the ring - it competes with the jewelry"
    else:
        detail = "jewelry is the clear focus"
    return {
        "gate": "jewelry_hero",
        "verdict": "PASS" if ok else "FAIL",
        "sharp_ratio": round(sharp_ratio, 2),
        "ink_vs_jewel": round(ink_vs_jewel, 3),
        "detail": detail,
    }


def check_logo_subtle(a: np.ndarray) -> dict:
    """Logo stays secondary: small, edge-biased, mostly cropped or lost in folds.
    Centred or large lockups fail even when they print naturally."""
    ink = _ink_mask(a)
    frac = float(ink.mean())
    if ink.sum() < 1500:
        return {"gate": "logo_subtle", "verdict": "UNKNOWN",
                "detail": "no logo ink - plain velvet (compliant)"}
    h, w = ink.shape
    ys, xs = np.nonzero(ink)
    # distance of the ink centroid from frame centre, 0 = dead centre, 1 = corner
    off = float(max(abs(xs.mean() / w - 0.5), abs(ys.mean() / h - 0.5)) * 2)
    ok = frac <= 0.05 and off >= 0.45
    if frac > 0.05:
        detail = f"logo covers {frac*100:.1f}% of frame - too prominent, shrink it"
    elif off < 0.45:
        detail = "logo sits too near frame centre - move it to the margin"
    else:
        detail = f"logo subtle: {frac*100:.1f}% of frame, edge-biased"
    return {
        "gate": "logo_subtle",
        "verdict": "PASS" if ok else "FAIL",
        "frame_frac": round(frac, 4),
        "off_center": round(off, 2),
        "detail": detail,
    }


def check_exposure(a: np.ndarray) -> dict:
    clipped = float(((a >= 254.5).all(2)).mean())
    ok = clipped <= CLIP_FRAC_MAX
    return {
        "gate": "exposure",
        "verdict": "PASS" if ok else "FAIL",
        "clipped_frac": round(clipped, 4),
        "detail": "no blown highlights" if ok else "blown-out white areas - facets unreadable",
    }


def check_centered(a: np.ndarray) -> dict:
    m = _jewel_mask(a)
    if m.sum() < 2000:
        return {"gate": "centered", "verdict": "UNKNOWN", "detail": "ring not found"}
    ys, xs = np.nonzero(m)
    h, w = m.shape
    dx = abs(xs.mean() / w - 0.5)
    dy = abs(ys.mean() / h - 0.5)
    ok = dx <= CENTER_TOL and dy <= CENTER_TOL
    return {
        "gate": "centered",
        "verdict": "PASS" if ok else "FAIL",
        "dx": round(dx, 3),
        "dy": round(dy, 3),
        "detail": "centered" if ok else "ring off-centre beyond tolerance",
    }


def stone_signature(path: str) -> list[dict]:
    """Segment the stone run along the band: returns each stone's width and a
    round/baguette classification. Front-elevation views only."""
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    mx, mn = a.max(2), a.min(2)
    sat = mx - mn
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    bg = (r > 238) & (g > 238) & (b > 238)
    dia = (mx > 110) & (sat < 38) & (b > 90) & ~bg
    rows = dia.sum(1)
    if rows.max() == 0:
        return []
    r0 = int(np.argmax(rows))
    band = slice(max(0, r0 - 70), r0 + 70)
    d = dia[band].sum(0)
    s = sat[band].mean(0)
    segs, cur = [], None
    for x in range(a.shape[1]):
        is_stone = d[x] > 25 and s[x] < 22
        if is_stone and cur is None:
            cur = x
        elif not is_stone and cur is not None:
            if x - cur >= 18:
                segs.append((cur, x))
            cur = None
    if cur is not None:
        segs.append((cur, a.shape[1]))
    if not segs:
        return []

    # Classify by SHAPE, not by width alone. Width is unreliable: toward the
    # ring's edges perspective foreshortens stones and merges neighbours into
    # one blob, which drags a width-median far off the true round size.
    #
    # A step-cut baguette fills its bounding box almost completely (fill ~1.0);
    # a round brilliant is a circle inscribed in its box (fill ~pi/4 = 0.79);
    # a merged run of rounds fills even less and is much wider than one stone.
    sub = dia[band]
    unit = float(np.percentile([e - s0 for s0, e in segs], 25))  # one round's width

    out = []
    for s0, e in segs:
        w = e - s0
        blob = sub[:, s0:e]
        ys = np.nonzero(blob.any(1))[0]
        h = int(ys.max() - ys.min() + 1) if ys.size else 1
        fill = float(blob.sum()) / max(w * h, 1)
        n_est = max(1, int(round(w / unit))) if unit > 0 else 1
        if fill >= 0.72 and 1.3 * unit < w < 2.1 * unit:
            kind, count = "baguette", 1
        elif n_est >= 2:
            kind, count = "round-group", n_est
        else:
            kind, count = "round", 1
        out.append({"x0": s0, "x1": e, "w": w, "h": h, "fill": round(fill, 3),
                    "kind": kind, "count": count})
    return out


def check_geometry(render: str, source: str) -> dict:
    rs, ss = stone_signature(render), stone_signature(source)
    if not ss:
        return {"gate": "geometry", "verdict": "UNKNOWN", "detail": "no stone run in source"}
    if not rs:
        return {"gate": "geometry", "verdict": "UNKNOWN", "detail": "no stone run in render"}
    def pat(sig):
        return "".join("B" if x["kind"] == "baguette" else "R" * x["count"] for x in sig)

    r_pat, s_pat = pat(rs), pat(ss)
    ok = r_pat == s_pat
    return {
        "gate": "geometry",
        "verdict": "PASS" if ok else "FAIL",
        "render_pattern": r_pat,
        "source_pattern": s_pat,
        "detail": "stone run matches source"
        if ok
        else f"stone run drifted: render {r_pat} vs source {s_pat}",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("render")
    ap.add_argument("--source", help="SKU source image for the geometry gate")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    a = _load(args.render)
    results = [
        check_jewelry_hero(a),
        check_velvet(a),
        check_logo_natural(a),
        check_logo_subtle(a),
        check_whitebalance(a),
        check_exposure(a),
        check_centered(a),
    ]
    if args.source:
        results.append(check_geometry(args.render, args.source))

    failed = [r for r in results if r["verdict"] == "FAIL"]
    unknown = [r for r in results if r["verdict"] == "UNKNOWN"]
    verdict = "REJECT" if failed else ("REVIEW" if unknown else "PASS")

    if args.json:
        print(json.dumps({"render": args.render, "verdict": verdict, "gates": results}, indent=2))
    else:
        print(f"{args.render}  ->  {verdict}")
        for r in results:
            print(f"  [{r['verdict']:7}] {r['gate']:9} {r['detail']}")
        if unknown:
            print("  NOTE: UNKNOWN gates were not decided - inspect manually, do not assume pass.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
