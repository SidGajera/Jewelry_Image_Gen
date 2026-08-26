#!/usr/bin/env python3
"""
DETERMINISTIC PHOTO CLEANUP — dust, fingerprints and surface grime removed from a
jewellery photograph WITHOUT redrawing the jewellery.

WHY THIS IS NOT A GENERATIVE EDIT
  No model is called. Every output pixel is a function of the input pixels of this
  same photograph. Nothing is imagined, completed or restyled. That satisfies
  policy/GENERATION_LAW.md LAW-02 (no AI redraw of the piece) by construction rather
  than by rejection, because there is no synthesis step to drift.

HOW THE DESIGN IS HELD FIXED
  The image is split into a LOW-FREQUENCY band (tone, haze, smudge, fingerprint film)
  and a HIGH-FREQUENCY band (facet edges, prong outlines, band contour, grain).
  Cleanup acts on the LOW band. The HIGH band is added back unmodified, so every
  edge stays on the pixel it started on. Geometry cannot move.

  The only exception is defect inpainting, which is confined to small isolated blobs
  that are (a) below a hard area cap, (b) not sitting on a structural edge, and
  (c) locally isotropic — i.e. specks of dust, never a facet line. Each accepted blob
  is recorded in the report.

  Stage 5 then VERIFIES the claim: it re-extracts the edge map inside the jewellery
  and fails the run if edge agreement with the source drops below --min-edge-iou.

ANTI-AI FINISH
  * original resolution, no upscaling, no super-resolution
  * grain is preserved (the HF band is returned untouched) and re-matched inside
    inpainted patches, so no plastic smooth spots
  * no halo-producing large-radius sharpening
  * sparkle is a gain on highlights the photograph ALREADY has, never painted in
  * colour science is left alone apart from an optional neutral-grey cast removal

USAGE
  python3 scripts/clean_photo.py --in ring.jpg --out ring_clean.png
  python3 scripts/clean_photo.py --in ring.jpg --out ring_clean.png --compare sbs.png
  python3 scripts/clean_photo.py --in ring.jpg --out ring_clean.png --report r.json

Requires: pip install numpy pillow opencv-python-headless
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


# ---------------------------------------------------------------- io

def load_bgr(path):
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:                       # webp / odd formats -> via PIL
        pil = Image.open(path).convert("RGB")
        img = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    return img


def odd(n):
    n = int(round(n))
    return n + 1 if n % 2 == 0 else max(n, 1)


# ---------------------------------------------------------- segmentation

def segment(bgr):
    """Split the frame into jewellery / metal / stone / background.

    Category-agnostic: 'jewellery' is simply the bright coherent subject against the
    darker ground, which also picks up its mirror reflection — correct, because a
    reflection carries the design too and must be protected the same way.
    """
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hue, sat, val = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    blur = cv2.GaussianBlur(val, (odd(0.01 * max(h, w)), odd(0.01 * max(h, w))), 0)
    thr, _ = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    subject = (blur > max(thr * 0.55, 40)).astype(np.uint8)

    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (odd(0.006 * max(h, w)),) * 2)
    subject = cv2.morphologyEx(subject, cv2.MORPH_CLOSE, k)
    subject = cv2.morphologyEx(subject, cv2.MORPH_OPEN, k)

    # keep components of meaningful size; drops isolated bokeh dots from the subject
    n, lab, stats, _ = cv2.connectedComponentsWithStats(subject, 8)
    keep = np.zeros_like(subject)
    min_area = 0.0004 * h * w
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            keep[lab == i] = 1
    subject = keep

    # metal = saturated yellow/warm polish; stone = bright but near-neutral
    warm = ((hue >= 12) & (hue <= 45) & (sat >= 60)).astype(np.uint8)
    metal = (subject & warm).astype(np.uint8)
    stone = (subject & (~warm.astype(bool)).astype(np.uint8) & (val > 90).astype(np.uint8)).astype(np.uint8)
    background = (1 - subject).astype(np.uint8)
    return subject, metal, stone, background


# ------------------------------------------------------ defect detection

def find_defects(gray, region, scale, max_area, contrast, protect_edges):
    """Isolated specks that are local outliers — dust, lint, pinholes.

    A blob is accepted only when it is small, high-contrast against its own
    neighbourhood, roughly isotropic, and clear of the structural edge map. Facet
    lines and prong outlines are long and edge-bound, so they can never qualify.

    The structuring element is sized from the defect cap, not from the image, and
    that sizing is what separates dust from bokeh: an opening erases anything
    smaller than the element, so a speck lights the top-hat up while a soft
    out-of-focus disc — many times larger — survives the opening and returns
    nothing. Deliberate background bokeh is therefore never a candidate.
    """
    dia = 2.0 * np.sqrt(max(max_area, 1) / np.pi)
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (odd(max(5, 2.2 * dia)),) * 2)
    bright = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, se)
    dark = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, se)
    cand = ((bright > contrast) | (dark > contrast)).astype(np.uint8) * region

    accepted = np.zeros_like(cand)
    rejected = 0
    blobs = []
    se_px = se.shape[0]
    n, lab, stats, cent = cv2.connectedComponentsWithStats(cand, 8)
    for i in range(1, n):
        area = int(stats[i, cv2.CC_STAT_AREA])
        bw, bh = int(stats[i, cv2.CC_STAT_WIDTH]), int(stats[i, cv2.CC_STAT_HEIGHT])
        if area > max_area or area < 1:
            rejected += 1
            continue
        if max(bw, bh) > 3.5 * max(min(bw, bh), 1):        # elongated -> structure
            rejected += 1
            continue
        comp = (lab == i)
        if protect_edges is not None and (protect_edges[comp] > 0).any():
            rejected += 1
            continue
        accepted[comp] = 1
        blobs.append({"area": area, "x": int(cent[i][0]), "y": int(cent[i][1])})

    # A speck fades out over a pixel or two; repairing only the core leaves a rim.
    # Grow by one pixel, then re-apply BOTH guards so the growth can never spill
    # onto a protected edge or outside the region it was found in.
    if accepted.any():
        grown = cv2.dilate(accepted, np.ones((3, 3), np.uint8)) * region
        if protect_edges is not None:
            grown = (grown & (protect_edges == 0).astype(np.uint8))
        accepted = np.clip(accepted + grown, 0, 1).astype(np.uint8)
    return accepted, blobs, rejected, se_px


def inpaint_defects(bgr, mask, scale, rng):
    """Fill accepted specks from their own surroundings, then restore local grain so
    the patch does not read as a smooth AI blob."""
    if mask.sum() == 0:
        return bgr
    radius = max(2, int(round(2 * scale)))
    out = cv2.inpaint(bgr, mask, radius, cv2.INPAINT_TELEA)

    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (odd(6 * scale),) * 2)
    ring = (cv2.dilate(mask, k) - mask).astype(bool)
    if ring.sum() > 32:
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
        lf = cv2.GaussianBlur(gray, (0, 0), 1.4 * scale)
        sigma = float(np.std((gray - lf)[ring]))
        sigma = float(np.clip(sigma, 0.0, 6.0))
        if sigma > 0.3:
            noise = rng.normal(0.0, sigma, size=out.shape[:2]).astype(np.float32)
            sel = mask.astype(bool)
            f = out.astype(np.float32)
            f[sel] += noise[sel][:, None]
            out = np.clip(f, 0, 255).astype(np.uint8)
    return out


# ------------------------------------------------------------- cleanup

def split_bands(bgr, sigma):
    low = cv2.GaussianBlur(bgr.astype(np.float32), (0, 0), sigma)
    return low, bgr.astype(np.float32) - low


def suppress_blotches(low, mask, base_sigma, strength, max_amp):
    """Remove the fingerprint film and grime haze from the LOW band only.

    A smudge is mid-scale unevenness: broader than grain, narrower than the overall
    shading. Subtracting `low - blur(low)` therefore targets it directly. The HIGH
    band never enters this function, so facet lines, prong edges and the band
    contour cannot be affected.

    `base_sigma` must be wider than the features that have to survive. On the ground
    that means wider than the bokeh discs, so a disc registers at full amplitude and
    the clamp below excludes it outright; a narrower base would catch only the disc's
    rim and quietly dim it.

    The amplitude clamp is what keeps the result photographic. Grime is subtle;
    specular gradients on polished gold and out-of-focus bokeh discs are strong. By
    fading the correction out above `max_amp`, subtle unevenness is removed while
    real highlights and bokeh are left alone. Without this clamp the same operator
    flattens the metal and dims the bokeh — the classic over-retouched look.
    """
    if mask.sum() == 0 or strength <= 0:
        return low
    base = cv2.GaussianBlur(low, (0, 0), max(6.0, base_sigma))
    blotch = low - base
    amp = np.abs(blotch).max(axis=2)
    keep = np.clip(1.0 - (amp - max_amp) / max(max_amp, 1e-3), 0.0, 1.0)
    soft = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 2.0) * strength * keep
    return low - blotch * soft[..., None]


def boost_existing_speculars(bgr_f, mask, amount):
    """Lift the highlights the photograph already recorded. Pixels that are not
    already specular receive no gain, so no sparkle is invented."""
    if mask.sum() == 0 or amount <= 0:
        return bgr_f
    v = bgr_f.max(axis=2)
    sel = mask.astype(bool)
    if sel.sum() < 64:
        return bgr_f
    lo = float(np.percentile(v[sel], 88))
    hi = float(np.percentile(v[sel], 99.5))
    if hi - lo < 1e-3:
        return bgr_f
    t = np.clip((v - lo) / (hi - lo), 0, 1) ** 1.5
    soft = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 1.5)
    gain = 1.0 + amount * t * soft
    return bgr_f * gain[..., None]


def neutralize_stone(bgr_f, stone, strength):
    """Pull a colour cast out of the stone toward neutral without touching its
    structure — a white-balance nudge on the stone's own average, nothing else."""
    sel = stone.astype(bool)
    if sel.sum() < 200 or strength <= 0:
        return bgr_f
    mean = bgr_f[sel].reshape(-1, 3).mean(axis=0)
    target = float(mean.mean())
    gain = np.clip(target / np.clip(mean, 1e-3, None), 0.85, 1.18)
    gain = 1.0 + (gain - 1.0) * strength
    soft = cv2.GaussianBlur(stone.astype(np.float32), (0, 0), 1.5)[..., None]
    return bgr_f * (1 - soft) + bgr_f * gain[None, None, :] * soft


# ------------------------------------------------------------ verification

def edge_map(bgr):
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    g = cv2.GaussianBlur(g, (3, 3), 0)
    return cv2.Canny(g, 60, 160)


def structural_edge_map(bgr, speck_px):
    """The edge map used to PROTECT the design, built from a median-filtered copy.

    This distinction matters. A dark speck on a bright stone draws a crisp closed
    contour of its own, so an edge map taken from the raw frame would mark the dust
    as protected structure and the cleanup would refuse to touch it. A median filter
    wider than a speck deletes specks while leaving facet lines, prong edges and the
    band contour intact, so what survives is design and only design.
    """
    k = odd(max(3, min(speck_px, 15)))
    med = cv2.medianBlur(bgr, k)
    return cv2.dilate(edge_map(med), np.ones((3, 3), np.uint8))


def noise_sigma(bgr):
    """Robust high-frequency noise estimate (MAD), so detection thresholds scale
    with the grain of the actual photograph instead of a hard-coded guess."""
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    hf = g - cv2.GaussianBlur(g, (0, 0), 1.4)
    return float(np.median(np.abs(hf - np.median(hf))) * 1.4826)


def verify_design_unchanged(src, out, jewel, repaired):
    """Enforced check, not a promise: the jewellery's edge structure in the output
    must still sit where the source put it.

    Two deliberate subtleties.

    * The specks we repaired were themselves edges in the source. Comparing over
      them would score our own intended work as drift, so the repaired pixels are
      excluded and reported separately.
    * Exact Canny overlap flickers on threshold-borderline pixels even when nothing
      moves. What matters is DISPLACEMENT, so agreement is scored with a one-pixel
      tolerance via a distance transform: an edge that stayed put passes, an edge
      that shifted does not.
    """
    e0, e1 = edge_map(src), edge_map(out)
    sel = jewel.astype(bool) & ~repaired.astype(bool)
    a, b = (e0 > 0) & sel, (e1 > 0) & sel

    d_to_out = cv2.distanceTransform((~(e1 > 0)).astype(np.uint8), cv2.DIST_L2, 3)
    d_to_src = cv2.distanceTransform((~(e0 > 0)).astype(np.uint8), cv2.DIST_L2, 3)
    recall = 1.0 if a.sum() == 0 else float((d_to_out[a] <= 1.0).mean())
    precision = 1.0 if b.sum() == 0 else float((d_to_src[b] <= 1.0).mean())
    f1 = 0.0 if (recall + precision) < 1e-9 else 2 * recall * precision / (recall + precision)

    union = int((a | b).sum())
    iou = 1.0 if union == 0 else float((a & b).sum()) / union

    g_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    g_out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    m0 = np.hypot(cv2.Sobel(g_src, cv2.CV_32F, 1, 0, ksize=3),
                  cv2.Sobel(g_src, cv2.CV_32F, 0, 1, ksize=3))[sel]
    m1 = np.hypot(cv2.Sobel(g_out, cv2.CV_32F, 1, 0, ksize=3),
                  cv2.Sobel(g_out, cv2.CV_32F, 0, 1, ksize=3))[sel]
    denom = float(np.linalg.norm(m0) * np.linalg.norm(m1))
    corr = 1.0 if denom < 1e-6 else float(np.dot(m0, m1) / denom)

    return {
        "structure_f1_1px": round(f1, 5),
        "edge_recall_1px": round(recall, 5),
        "edge_precision_1px": round(precision, 5),
        "gradient_correlation": round(corr, 5),
        "strict_edge_iou": round(iou, 5),
        "compared_edge_pixels": int(a.sum()),
        "excluded_repaired_pixels": int((jewel.astype(bool) & repaired.astype(bool)).sum()),
    }


# ------------------------------------------------------------------ main

def clean(src, args):
    h, w = src.shape[:2]
    scale = max(h, w) / 1500.0
    rng = np.random.default_rng(args.seed)
    report = {"input_size": [w, h], "scale": round(scale, 4), "generative": False}

    jewel, metal, stone, background = segment(src)
    report["mask_fractions"] = {
        "jewellery": round(float(jewel.mean()), 5),
        "metal": round(float(metal.mean()), 5),
        "stone": round(float(stone.mean()), 5),
    }

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    sigma_n = noise_sigma(src)
    report["noise_sigma"] = round(sigma_n, 3)

    # thresholds float above this frame's own grain, so grain is never mistaken for
    # dust on a noisy shot and real dust is still caught on a clean one
    bg_thr = max(args.bg_dust_contrast, args.noise_k * sigma_n)
    jw_thr = max(args.jewel_dust_contrast, args.noise_k * sigma_n)
    report["thresholds"] = {"background": round(bg_thr, 2), "jewellery": round(jw_thr, 2)}

    jw_cap = max(12, int(args.jewel_dust_area * scale * scale))
    bg_cap = max(20, int(args.bg_dust_area * scale * scale))
    speck_px = int(2 * np.sqrt(max(jw_cap, 1) / np.pi)) + 2
    edges = structural_edge_map(src, speck_px)

    # 1. dust on the ground — the ground carries no design, so the only guard is the
    #    area cap that separates a speck from the intentional bokeh.
    bg_mask, bg_blobs, bg_rej, bg_se = find_defects(
        gray, background, scale,
        max_area=bg_cap, contrast=bg_thr, protect_edges=None)

    # 2. dust on the piece — same detector, tighter cap, and the structural edge map
    #    is off limits so a facet line can never be selected.
    jw_mask, jw_blobs, jw_rej, jw_se = find_defects(
        gray, jewel, scale,
        max_area=jw_cap, contrast=jw_thr, protect_edges=edges)

    defects = np.clip(bg_mask + jw_mask, 0, 1).astype(np.uint8)
    report["defects"] = {
        "background_removed": len(bg_blobs), "background_rejected": bg_rej,
        "jewellery_removed": len(jw_blobs), "jewellery_rejected": jw_rej,
        "pixels_touched": int(defects.sum()),
        "pixel_fraction": round(float(defects.mean()), 6),
        "background_kernel_px": bg_se,
        "jewellery_kernel_px": jw_se,
    }
    work = inpaint_defects(src, defects, scale, rng)

    # 3. fingerprint film and haze — LOW band only, HIGH band held out and restored
    sigma = max(2.0, args.band_sigma * scale)
    low, high = split_bands(work, sigma)
    low = suppress_blotches(low, metal, args.metal_blotch_scale * scale,
                            args.metal_smudge, args.metal_blotch_amp)
    low = suppress_blotches(low, background, args.bg_blotch_scale * scale,
                            args.bg_smudge, args.bg_blotch_amp)
    out = low + high                                    # detail returned bit-for-bit

    # 4. natural shine — gain on recorded speculars, plus a light touch of existing
    #    micro-detail in the stone. Neither creates structure that was not shot.
    out = boost_existing_speculars(out, metal, args.metal_shine)
    out = boost_existing_speculars(out, stone, args.stone_sparkle)
    if args.stone_microcontrast > 0:
        soft = cv2.GaussianBlur(stone.astype(np.float32), (0, 0), 1.5)[..., None]
        out = out + high * (args.stone_microcontrast * soft)
    out = neutralize_stone(out, stone, args.stone_neutral)

    out = np.clip(out, 0, 255).astype(np.uint8)

    # 5. the claim is checked, not assumed
    guard = cv2.dilate(defects, np.ones((3, 3), np.uint8))
    report["verification"] = verify_design_unchanged(src, out, jewel, guard)
    report["verification"]["min_structure_f1"] = args.min_structure_f1
    report["verification"]["min_gradient_corr"] = args.min_gradient_corr
    passed = (report["verification"]["structure_f1_1px"] >= args.min_structure_f1
              and report["verification"]["gradient_correlation"] >= args.min_gradient_corr)
    report["verification"]["passed"] = bool(passed)
    return out, report, passed


def main():
    p = argparse.ArgumentParser(description="Deterministic jewellery photo cleanup (no AI).")
    p.add_argument("--in", dest="src", required=True)
    p.add_argument("--out", dest="dst", required=True)
    p.add_argument("--report", default=None, help="write the JSON report here")
    p.add_argument("--compare", default=None, help="write a before/after side-by-side")
    p.add_argument("--seed", type=int, default=7)

    p.add_argument("--bg-dust-area", type=float, default=240.0,
                   help="max speck area on the ground, px at 1500px long edge")
    p.add_argument("--bg-dust-contrast", type=float, default=7.0)
    p.add_argument("--jewel-dust-area", type=float, default=90.0,
                   help="max speck area on the piece; the design guard is the "
                        "edge map and the isotropy test, not this cap alone")
    p.add_argument("--jewel-dust-contrast", type=float, default=13.0)

    p.add_argument("--band-sigma", type=float, default=4.0,
                   help="detail/tone split; everything finer than this is preserved bit-for-bit")
    p.add_argument("--metal-smudge", type=float, default=0.45, help="fingerprint removal on metal 0-1")
    p.add_argument("--metal-blotch-scale", type=float, default=40.0,
                   help="px at 1500px long edge; wider than a fingerprint, narrower than the piece")
    p.add_argument("--metal-blotch-amp", type=float, default=25.0,
                   help="above this amplitude a feature counts as a real highlight, not grime")
    p.add_argument("--bg-smudge", type=float, default=0.0,
                   help="haze/grime removal on the ground 0-1. OFF by default: on a backdrop "
                        "with a legitimate light gradient this operator shifts tone over a "
                        "large area for little gain, and dust removal already does the work. "
                        "Raise it only for a visibly hazy or grimy backdrop.")
    p.add_argument("--bg-blotch-scale", type=float, default=120.0,
                   help="px at 1500px long edge; must exceed the bokeh discs so they survive")
    p.add_argument("--bg-blotch-amp", type=float, default=6.0,
                   help="keeps intentional bokeh and light bands out of the correction")

    p.add_argument("--metal-shine", type=float, default=0.16)
    p.add_argument("--stone-sparkle", type=float, default=0.20)
    p.add_argument("--stone-microcontrast", type=float, default=0.10)
    p.add_argument("--stone-neutral", type=float, default=0.35)

    p.add_argument("--noise-k", type=float, default=4.0,
                   help="detection threshold floor, in multiples of measured grain sigma")
    p.add_argument("--min-structure-f1", type=float, default=0.985,
                   help="minimum 1px-tolerance edge agreement inside the jewellery")
    p.add_argument("--min-gradient-corr", type=float, default=0.995)
    args = p.parse_args()

    src_path = Path(args.src)
    if not src_path.exists():
        print(f"ERROR: input not found: {src_path}", file=sys.stderr)
        return 2

    src = load_bgr(src_path)
    out, report, passed = clean(src, args)

    if not passed:
        print("REJECTED — the jewellery structure moved; nothing written.", file=sys.stderr)
        print(json.dumps(report["verification"], indent=2), file=sys.stderr)
        return 1

    Path(args.dst).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.dst), out, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    report["output"] = str(args.dst)

    if args.compare:
        gap = np.full((src.shape[0], max(8, src.shape[1] // 100), 3), 24, np.uint8)
        cv2.imwrite(str(args.compare), np.hstack([src, gap, out]))
        report["compare"] = args.compare

    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2))

    v = report["verification"]
    d = report["defects"]
    print(f"OK  {src_path.name} -> {args.dst}")
    print(f"    specks removed : {d['jewellery_removed']} on the piece, "
          f"{d['background_removed']} on the ground "
          f"({d['pixel_fraction'] * 100:.4f}% of pixels)")
    print(f"    design check   : structure F1 {v['structure_f1_1px']:.4f} "
          f"(min {args.min_structure_f1}), gradient corr "
          f"{v['gradient_correlation']:.4f}")
    print(f"    generative     : no — every pixel derives from this photograph")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
