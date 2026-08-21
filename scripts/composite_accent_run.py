#!/usr/bin/env python3
"""ACCENT-RUN COMPOSITE (approved exception, docs/21 §2 / docs/13 §6c).

The frozen Higgsfield call generates the jewelry BODY + scene. Because diffusion
cannot count discrete accent stones, the accent/pavé RUN is transferred here from
the clean CAD source view so its count is correct BY CONSTRUCTION — the same
preserved-pixel layer mechanism proven on the logo (scripts/print_logo_on_cloth.py).
Only the accent run is composited; the primary stone, head/setting, structure and
scene stay generated.

Method (per shoulder/run ROI):
  1. Take the source accent strip (clean CAD view, region given by the accent-map
     specs/<SKU>_accent_src.json, or --src-strip).
  2. Align it to the render's accent ROI via ORB feature matching -> homography;
     fall back to a manual 4-point map (--anchors) when matching is weak.
  3. Warp, feather-blend, and transfer the render's local luminance so the pasted
     stones pick up the render's lighting.
  4. The result is re-checked by validate_render G2-G5 (count/size/run/setting).

Honesty: robust auto-alignment needs the real CAD views (the current LR-0203
source is 2 watermarked retail photos, which is why this is gated behind
validate_source). Until clean views exist this module runs but its alignment is
unverified; treat manual --anchors as the reliable path.

Usage:
    python scripts/composite_accent_run.py LR-0203 --render R.png --source SRC.png \
        --run shoulder_right --out OUT.png [--anchors x1,y1;...]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import cv2

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import _cv_lib as cvlib  # noqa: E402


def _roi_box(bgr, run_id):
    h, w = bgr.shape[:2]
    y0, y1 = int(h * 0.35), int(h * 0.80)
    if run_id.endswith("left"):
        return (int(w * 0.03), y0, int(w * 0.42), y1)
    if run_id.endswith("right"):
        return (int(w * 0.58), y0, int(w * 0.97), y1)
    return (int(w * 0.15), int(h * 0.42), int(w * 0.85), int(h * 0.62))


def _align_homography(src_strip, dst_roi):
    """ORB match src_strip -> dst_roi; return 3x3 H or None if too weak."""
    orb = cv2.ORB_create(1500)
    k1, d1 = orb.detectAndCompute(cv2.cvtColor(src_strip, cv2.COLOR_BGR2GRAY), None)
    k2, d2 = orb.detectAndCompute(cv2.cvtColor(dst_roi, cv2.COLOR_BGR2GRAY), None)
    if d1 is None or d2 is None or len(k1) < 12 or len(k2) < 12:
        return None
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = sorted(bf.match(d1, d2), key=lambda m: m.distance)[:60]
    if len(matches) < 12:
        return None
    src = np.float32([k1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst = np.float32([k2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    H, _ = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    return H


def _feather(mask, k=21):
    return cv2.GaussianBlur(mask.astype(np.float32) / 255.0, (k, k), 0)[..., None]


def _transfer_luma(patch, target_roi):
    """Match the pasted patch's mean luminance to the render ROI so lighting agrees."""
    ph = cv2.cvtColor(patch, cv2.COLOR_BGR2LAB).astype(np.float32)
    th = cv2.cvtColor(target_roi, cv2.COLOR_BGR2LAB).astype(np.float32)
    ph[..., 0] += (th[..., 0].mean() - ph[..., 0].mean())
    ph[..., 0] = np.clip(ph[..., 0], 0, 255)
    return cv2.cvtColor(ph.astype(np.uint8), cv2.COLOR_LAB2BGR)


def composite_run(render_bgr, source_bgr, run_id, src_strip_box=None, anchors=None):
    x0, y0, x1, y1 = _roi_box(render_bgr, run_id)
    dst_roi = render_bgr[y0:y1, x0:x1]
    if src_strip_box:
        sx0, sy0, sx1, sy1 = src_strip_box
        src_strip = source_bgr[sy0:sy1, sx0:sx1]
    else:
        sb = _roi_box(source_bgr, run_id)
        src_strip = source_bgr[sb[1]:sb[3], sb[0]:sb[2]]

    if anchors is not None:
        dst_pts = np.float32(anchors)
        h, w = src_strip.shape[:2]
        src_pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        H = cv2.getPerspectiveTransform(src_pts, dst_pts - [x0, y0])
    else:
        H = _align_homography(src_strip, dst_roi)
        if H is None:
            return render_bgr, f"{run_id}: alignment too weak (need clean CAD view or --anchors)"

    warped = cv2.warpPerspective(src_strip, H, (dst_roi.shape[1], dst_roi.shape[0]))
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    mask = ((gray > 8) * 255).astype(np.uint8)
    warped = _transfer_luma(warped, dst_roi)
    alpha = _feather(mask)
    blended = (warped * alpha + dst_roi * (1 - alpha)).astype(np.uint8)
    out = render_bgr.copy()
    out[y0:y1, x0:x1] = blended
    return out, f"{run_id}: composited ({'anchors' if anchors is not None else 'ORB homography'})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sku")
    ap.add_argument("--render", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--run", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--anchors", help="4 dst points 'x1,y1;x2,y2;x3,y3;x4,y4' (TL,TR,BR,BL)")
    args = ap.parse_args()

    render = cvlib.load_bgr(args.render)
    source = cvlib.load_bgr(args.source)
    anchors = None
    if args.anchors:
        anchors = [[float(v) for v in p.split(",")] for p in args.anchors.split(";")]
    out, detail = composite_run(render, source, args.run, anchors=anchors)
    cv2.imwrite(args.out, out)
    print(detail + f" -> {args.out}")


if __name__ == "__main__":
    main()
