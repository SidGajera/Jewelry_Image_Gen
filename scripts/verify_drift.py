#!/usr/bin/env python3
"""DESIGN DRIFT — measure how far a candidate render moved from the source piece.

Written for the case where a GENERATIVE engine (Nano Banana 2, either route) is
asked to clean or re-render a photograph. A generative call re-synthesises what it
draws, so "the jewellery is unchanged" is a claim that has to be measured, not
assumed — exactly the honest limit recorded in policy/GENERATION_LAW.md LAW-02 and
docs/27. This script produces the number.

Two families of measurement, deliberately:

  DESIGN MEASURES are scale- and position-tolerant, so a render that is merely
  framed differently still passes. They come from scripts/_cv_lib.py, the same
  helpers the catalog gates use — piece count, stone count, stone aspect, stone
  share of the piece, metal hue. A change here means the DESIGN changed.

  STRUCTURE MEASURES are pixel-level and need alignment first. They answer the
  finer question of whether facet and prong geometry sits where it did. Alignment
  can fail on a heavily re-rendered frame; per repo convention that reports as
  'unmeasurable' and never blocks on its own.

Usage:
    python3 scripts/verify_drift.py --source ring.jpg --candidate cleaned.png
    python3 scripts/verify_drift.py --source ring.jpg --candidate cleaned.png --report d.json
Exit 0 = within tolerance; 1 = the design moved; 2 = could not measure.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import _cv_lib as cvl                      # noqa: E402  (shared gate helpers)
import clean_photo as cp                   # noqa: E402  (segmentation + structure check)


def design_measures(bgr):
    """Scale- and position-tolerant description of the piece itself."""
    out = {}
    try:
        out["piece_count"] = int(cvl.count_pieces(bgr))
    except Exception:
        out["piece_count"] = None
    try:
        out["stone_count"] = int(cvl.primary_stone_count(bgr))
    except Exception:
        out["stone_count"] = None
    try:
        lw = cvl.primary_ellipse_lw(bgr)
        out["stone_aspect_lw"] = round(float(lw[0] if isinstance(lw, (tuple, list)) else lw), 4)
    except Exception:
        out["stone_aspect_lw"] = None
    try:
        out["metal_hue"] = round(float(cvl.metal_hue_peak(bgr)), 2)
    except Exception:
        out["metal_hue"] = None

    # stone share of the piece — a ratio, so reframing does not move it
    jewel, metal, stone, _ = cp.segment(bgr)
    j, s = float(jewel.sum()), float(stone.sum())
    m = float(metal.sum())
    out["stone_share_of_piece"] = round(s / j, 4) if j > 0 else None

    # Stone against METAL, not against the whole piece. Share-of-piece saturates on a
    # solitaire — the stone already dominates the mask, so even a 25% larger stone
    # moves it only a few percent and the drift hides under any sane threshold.
    # Measured against the band it is a clean, scale-invariant reading of exactly what
    # "the diamond changed size" means, and it is the check that caught a forged
    # 1.12x stone the share-of-piece test waved through.
    out["stone_vs_metal_area"] = round(s / m, 4) if m > 0 else None
    return out


def stability(bgr):
    """Which measures can this source support?

    A measure is only evidence if it survives a nudge that changes no design. Each
    one is recomputed on a slightly blurred and a slightly brightened copy; a
    measure that moves under that is threshold-sitting on this particular frame and
    is reported UNMEASURABLE rather than being allowed to fail the render. This is
    the convention scripts/_cv_lib.py already documents — only a confident fail
    rejects — and it is what stops a brittle count from manufacturing false drift.
    """
    probes = [bgr,
              cv2.GaussianBlur(bgr, (0, 0), 0.6),
              np.clip(bgr.astype(np.float32) * 1.02, 0, 255).astype(np.uint8)]
    runs = [design_measures(p) for p in probes]
    stable = {}
    for key in runs[0]:
        vals = [r[key] for r in runs]
        if any(v is None for v in vals):
            stable[key] = False
        elif isinstance(vals[0], int):
            stable[key] = len(set(vals)) == 1
        else:
            m = np.mean([abs(v) for v in vals])
            stable[key] = (max(vals) - min(vals)) <= max(0.02 * m, 1e-6)
    return stable


def align(source, candidate):
    """Bring the candidate onto the source's pixel grid. Returns (warped, how)."""
    h, w = source.shape[:2]
    cand = cv2.resize(candidate, (w, h), interpolation=cv2.INTER_AREA)
    g0 = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY).astype(np.float32)
    g1 = cv2.cvtColor(cand, cv2.COLOR_BGR2GRAY).astype(np.float32)
    warp = np.eye(2, 3, dtype=np.float32)
    try:
        crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
        cv2.findTransformECC(g0, g1, warp, cv2.MOTION_AFFINE, crit, None, 5)
        cand = cv2.warpAffine(cand, warp, (w, h),
                              flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                              borderMode=cv2.BORDER_REPLICATE)
        shift = float(np.hypot(warp[0, 2], warp[1, 2]))
        return cand, {"method": "resize+ecc_affine", "translation_px": round(shift, 2)}
    except cv2.error:
        return cand, {"method": "resize_only", "translation_px": None,
                      "note": "ECC did not converge — the render differs too much to align"}


def pct(a, b):
    if a in (None, 0) or b is None:
        return None
    return round(100.0 * (b - a) / abs(a), 2)


def main():
    ap = argparse.ArgumentParser(description="Measure design drift between a source photo and a render.")
    ap.add_argument("--source", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--report", default=None)
    ap.add_argument("--max-aspect-drift", type=float, default=5.0, help="%% change in stone L:W")
    ap.add_argument("--max-share-drift", type=float, default=10.0, help="%% change in stone share of the piece")
    ap.add_argument("--max-stone-metal-drift", type=float, default=8.0,
                    help="%% change in stone area measured against the band")
    ap.add_argument("--max-hue-drift", type=float, default=6.0, help="degrees of metal hue shift")
    args = ap.parse_args()

    for p in (args.source, args.candidate):
        if not Path(p).exists():
            print(f"ERROR: not found: {p}", file=sys.stderr)
            return 2

    src = cvl.load_bgr(args.source)
    cand_raw = cvl.load_bgr(args.candidate)
    rep = {"source": args.source, "candidate": args.candidate,
           "source_size": [src.shape[1], src.shape[0]],
           "candidate_size": [cand_raw.shape[1], cand_raw.shape[0]]}

    a, b = design_measures(src), design_measures(cand_raw)
    ok_to_use = stability(src)
    rep["design"] = {"source": a, "candidate": b, "usable_on_this_source": ok_to_use}

    verdicts = []

    def judge(name, key, sa, sb, ok, shown):
        if not ok_to_use.get(key, False):
            verdicts.append({"measure": name, "source": sa, "candidate": sb,
                             "delta": "unmeasurable", "ok": True, "unmeasurable": True})
            return
        verdicts.append({"measure": name, "source": sa, "candidate": sb,
                         "delta": shown, "ok": bool(ok), "unmeasurable": False})

    judge("piece count", "piece_count", a["piece_count"], b["piece_count"],
          a["piece_count"] == b["piece_count"], "same" if a["piece_count"] == b["piece_count"] else "CHANGED")
    judge("stone count", "stone_count", a["stone_count"], b["stone_count"],
          a["stone_count"] == b["stone_count"], "same" if a["stone_count"] == b["stone_count"] else "CHANGED")

    d = pct(a["stone_aspect_lw"], b["stone_aspect_lw"])
    judge("stone aspect L:W", "stone_aspect_lw", a["stone_aspect_lw"], b["stone_aspect_lw"],
          d is not None and abs(d) <= args.max_aspect_drift, f"{d:+.2f}%" if d is not None else "unmeasurable")

    d = pct(a["stone_share_of_piece"], b["stone_share_of_piece"])
    judge("stone share of piece", "stone_share_of_piece",
          a["stone_share_of_piece"], b["stone_share_of_piece"],
          d is not None and abs(d) <= args.max_share_drift, f"{d:+.2f}%" if d is not None else "unmeasurable")

    d = pct(a["stone_vs_metal_area"], b["stone_vs_metal_area"])
    judge("stone vs metal area", "stone_vs_metal_area",
          a["stone_vs_metal_area"], b["stone_vs_metal_area"],
          d is not None and abs(d) <= args.max_stone_metal_drift,
          f"{d:+.2f}%" if d is not None else "unmeasurable")

    hd = None if None in (a["metal_hue"], b["metal_hue"]) else round(b["metal_hue"] - a["metal_hue"], 2)
    judge("metal hue", "metal_hue", a["metal_hue"], b["metal_hue"],
          hd is not None and abs(hd) <= args.max_hue_drift, f"{hd:+.2f}" if hd is not None else "unmeasurable")

    cand, how = align(src, cand_raw)
    rep["alignment"] = how
    jewel, _, _, _ = cp.segment(src)
    none_repaired = np.zeros(src.shape[:2], np.uint8)
    rep["structure"] = cp.verify_design_unchanged(src, cand, jewel, none_repaired)

    print(f"\nSOURCE     {Path(args.source).name}  {rep['source_size'][0]}x{rep['source_size'][1]}")
    print(f"CANDIDATE  {Path(args.candidate).name}  {rep['candidate_size'][0]}x{rep['candidate_size'][1]}")
    print(f"ALIGNMENT  {how['method']}"
          + (f", offset {how['translation_px']}px" if how.get("translation_px") is not None else ""))
    print("\nDESIGN MEASURES (scale- and position-tolerant)")
    print(f"  {'measure':<22} {'source':>10} {'candidate':>10} {'delta':>12}   verdict")
    for v in verdicts:
        mark = "n/a" if v.get("unmeasurable") else ("ok" if v["ok"] else "DRIFTED")
        print(f"  {v['measure']:<22} {str(v['source']):>10} {str(v['candidate']):>10} "
              f"{str(v['delta']):>12}   {mark}")

    s = rep["structure"]
    print("\nSTRUCTURE (pixel geometry inside the piece, after alignment)")
    print(f"  edges within 1px of source : {s['structure_f1_1px']:.4f}")
    print(f"  gradient correlation       : {s['gradient_correlation']:.4f}")

    hard = [v for v in verdicts if not v["ok"]]
    skipped = [v["measure"] for v in verdicts if v.get("unmeasurable")]
    rep["verdicts"] = verdicts
    rep["design_held"] = not hard
    if hard:
        print("\nDESIGN DRIFTED — " + ", ".join(v["measure"] for v in hard))
    else:
        print("\nDESIGN HELD across every measurable check.")
    if skipped:
        print("Not usable on this source (threshold-sitting, so not counted either way): "
              + ", ".join(skipped))
    print("Structure numbers describe how faithfully the pixels were reproduced; "
          "on a generative render they are expected to be well below 1.0.")

    if args.report:
        Path(args.report).write_text(json.dumps(rep, indent=2))
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
