#!/usr/bin/env python3
"""Shared, category-agnostic computer-vision helpers for the Lucent gate pipeline.

Works for rings, bracelets, pendants, earrings, necklaces — nothing product-
specific is hard-coded. Geometry gates (accent count/size/run, setting-element
tips, ellipse L:W, raised-rail, unauthorized clusters) are HEURISTIC; their
thresholds are calibrated against tests/golden approved renders. Each helper
returns a measurement plus a status of 'ok' | 'unmeasurable'; a gate turns that
into pass/fail/skip. 'unmeasurable' never hard-blocks; only a confident fail
rejects. Format and piece-count are exact/robust.
"""
from __future__ import annotations
import numpy as np

try:
    import cv2
    HAVE_CV2 = True
except Exception:  # pragma: no cover
    HAVE_CV2 = False

try:
    import pytesseract
    _ = pytesseract.get_tesseract_version()
    HAVE_OCR = True
except Exception:
    HAVE_OCR = False

from PIL import Image


# ---------- IO ----------
def load_bgr(path):
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:  # webp / odd formats -> via PIL
        pil = Image.open(path).convert("RGB")
        img = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    return img


# ---------- source-intake primitives ----------
def skin_fraction(bgr):
    """Fraction of skin-tone pixels. Must NOT count yellow gold (gold overlaps
    skin in YCrCb). Discriminate in HSV: skin is reddish (low hue) with MODERATE
    saturation; polished gold is yellower (higher hue) and/or highly saturated
    with strong specular. Require BOTH the YCrCb skin rule AND the HSV reddish-
    moderate-sat rule, excluding gold's yellow/high-sat band."""
    ycrcb = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    cr, cb = ycrcb[:, :, 1], ycrcb[:, :, 2]
    ycc = (cr >= 135) & (cr <= 178) & (cb >= 90) & (cb <= 132)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    reddish = (h <= 17)                     # skin ~red-orange; gold ~yellow (18-40) excluded
    moderate_sat = (s >= 40) & (s <= 170)   # gold is often > 170 (highly saturated polish)
    val_ok = (v >= 60) & (v <= 235)
    mask = ycc & reddish & moderate_sat & val_ok
    return float(mask.mean())


def detect_watermark(bgr):
    """(found, detail). A tiled watermark has THREE properties a CAD render's
    specular speckle lacks together: (1) REGULAR SPACING of its glyphs, (2) LOW
    CONTRAST vs the surface, (3) wide SPREAD across the frame. Flag only when all
    three hold. OCR (pytesseract) is used first when available."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    if HAVE_OCR:
        txt = pytesseract.image_to_string(gray).lower()
        words = [w.strip(".,-_|") for w in txt.split() if len(w.strip(".,-_|")) >= 4]
        from collections import Counter
        if words:
            tok, n = Counter(words).most_common(1)[0]
            if n >= 3:
                return True, f"OCR repeated overlay token '{tok}' x{n}"
        # fall through to the geometric test even with OCR (catches faint tiling)
    g = gray.astype(np.float32)
    hp = g - cv2.GaussianBlur(g, (0, 0), 3.0)          # high-pass
    amp = np.abs(hp)
    mark = (amp > 6).astype(np.uint8)                   # low-contrast marks only
    mark = cv2.morphologyEx(mark, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    n, _, stats, cent = cv2.connectedComponentsWithStats(mark, 8)
    H, W = gray.shape
    pts, contrasts = [], []
    for i in range(1, n):
        a = stats[i, cv2.CC_STAT_AREA]
        if 6 <= a <= (H * W) * 0.002:                   # glyph-sized
            pts.append(cent[i])
            contrasts.append(amp[int(cent[i][1]), int(cent[i][0])])
    if len(pts) < 12:
        return False, "no tiled overlay (too few glyph-sized marks)"
    pts = np.array(pts)
    # nearest-neighbour spacing regularity
    d = np.sqrt(((pts[:, None, :] - pts[None, :, :]) ** 2).sum(2))
    np.fill_diagonal(d, np.inf)
    nn = d.min(1)
    cv_spacing = float(nn.std() / (nn.mean() + 1e-9))
    spread = float((np.ptp(pts[:, 0]) * np.ptp(pts[:, 1])) / (H * W))
    low_contrast = float(np.median(contrasts)) < 30.0
    regular = cv_spacing < 0.35                          # tiled grid; speckle > 0.6
    spread_ok = spread > 0.25
    found = regular and low_contrast and spread_ok
    return found, (f"spacing_cv={cv_spacing:.2f} spread={spread:.2f} "
                   f"low_contrast={low_contrast} -> {'TILED WATERMARK' if found else 'clean (speckle/detail)'}")


def metal_hue_peak(bgr):
    """Dominant metal hue (OpenCV hue 0-180) from moderately-saturated foreground
    pixels — angle-invariant identity signal. Gold ~ 20-35; white metal has low
    saturation -> returns None (treated as 'white' bucket)."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    m = (s > 60) & (v > 60) & (v < 250)
    if m.sum() < 2000:
        return None                                     # white/platinum (low sat)
    hist = np.bincount(h[m].ravel(), minlength=180)
    return int(np.argmax(hist))


def primary_stone_count(bgr):
    """Count PRIMARY stones (angle-invariant identity): bright blobs comparably
    large to the dominant one. Accents are far smaller than the primary and are
    excluded, so a single-primary design reads 1 from every angle. Returns None
    when nothing large resolves (occluded back view) so it never false-STOPs."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    H, W = gray.shape
    _, th = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    nn, _, stats, _ = cv2.connectedComponentsWithStats(th, 8)
    areas = [stats[i, cv2.CC_STAT_AREA] for i in range(1, nn)]
    big = [a for a in areas if a >= H * W * 0.02]
    if not big:
        return None
    amax = max(big)
    return sum(1 for a in big if a >= 0.6 * amax)   # only a true co-primary counts; accents excluded


def accent_present(bgr):
    """True/False/None — are small accent stones present (identity signal)."""
    rois = accent_rois(bgr)
    counts = [count_small_stones(r) for r in rois.values()]
    counts = [c for c in counts if c is not None]
    if not counts:
        return None
    return max(counts) >= 3


def focal_phash(bgr, box=0.5):
    """pHash of the normalized centre (focal) crop. Coarse 'same design' check
    across source views (loose threshold) — different angles differ, so this
    only catches a grossly different second design in the set."""
    import imagehash
    h, w = bgr.shape[:2]
    m = (1 - box) / 2
    crop = bgr[int(h * m):int(h * (1 - m)), int(w * m):int(w * (1 - m))]
    return imagehash.phash(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)))


# ---------- render-gate primitives ----------
def foreground_mask(bgr):
    """Segment the piece from a bright near-white / velvet studio background."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    v, s = hsv[:, :, 2], hsv[:, :, 1]
    bg = np.median(v[[0, -1], :])
    mask = (((v < bg - 35) | (v > 250) | (s > 60)) * 255).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    return mask


def large_components(mask, k=5, min_area_frac=0.002):
    n, lbl, stats, cent = cv2.connectedComponentsWithStats(mask, 8)
    tot = mask.shape[0] * mask.shape[1]
    comps = sorted(((stats[i, cv2.CC_STAT_AREA], i) for i in range(1, n)), reverse=True)
    return [(a, i) for a, i in comps[:k] if a / tot >= min_area_frac], lbl, stats, cent


def count_pieces(bgr, min_area_frac=0.02):
    comps, *_ = large_components(foreground_mask(bgr), k=6, min_area_frac=min_area_frac)
    return len(comps)


def primary_ellipse_lw(bgr, expected_n=1):
    """Fit ellipses to the brightest large blobs (primary stones); return list of
    L:W ratios ordered by distance to centre. Catches shape drift
    (oval->round, marquise->oval, hexagon->emerald)."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    _, th = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    found = []
    for c in cnts:
        if len(c) < 5 or cv2.contourArea(c) < (h * w) * 0.008:
            continue
        (ex, ey), (MA, ma), _ = cv2.fitEllipse(c)
        lw = max(MA, ma) / max(min(MA, ma), 1e-6)
        d = ((ex - w / 2) ** 2 + (ey - h / 2) ** 2) ** 0.5
        found.append((d, float(lw)))
    found.sort()
    return [lw for _, lw in found[:max(expected_n, 1)]]


def accent_rois(bgr):
    """Return named ROIs likely to contain accent runs. Category-agnostic: left
    and right of centre (ring shoulders / bracelet-necklace link rows) plus a
    girdle band. validate_render maps spec accent_run ids onto these."""
    h, w = bgr.shape[:2]
    y0, y1 = int(h * 0.35), int(h * 0.8)
    return {
        "left":  bgr[y0:y1, int(w * 0.03):int(w * 0.42)],
        "right": bgr[y0:y1, int(w * 0.58):int(w * 0.97)],
        "center_row": bgr[int(h * 0.42):int(h * 0.62), int(w * 0.15):int(w * 0.85)],
    }


def _stone_components(roi):
    """Connected components of small bright specular blobs (accent stones),
    EXCLUDING large blobs (a primary stone leaking into the ROI). Uses a
    brightness-percentile threshold — robust for compact specular stones on both
    a dark basket and a bright metal shoulder — with an absolute size window."""
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    thr = np.percentile(gray, 88)                 # top ~12% brightest = stone facets
    bw = ((gray >= max(thr, 200)) * 255).astype(np.uint8)
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    n, _, stats, _ = cv2.connectedComponentsWithStats(bw, 8)
    roi_area = roi.shape[0] * roi.shape[1]
    hi = max(roi_area * 0.02, 64)                 # too big to be an accent stone
    rows = [stats[i] for i in range(1, n) if 6 <= stats[i, cv2.CC_STAT_AREA] <= hi]
    if not rows:
        return []
    med = float(np.median([r[cv2.CC_STAT_AREA] for r in rows]))
    return [r for r in rows if 0.15 * med <= r[cv2.CC_STAT_AREA] <= 6 * med]


def count_small_stones(roi):
    """Count small bright specular blobs (accent stones). Heuristic; calibrated
    on golden cases. Robust to a dominant bright primary blob in the ROI."""
    if roi is None or roi.size == 0:
        return None
    return len(_stone_components(roi))


def small_stone_median_diam(roi):
    if roi is None or roi.size == 0:
        return None
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    th = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    _, bw = cv2.threshold(th, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    n, _, stats, _ = cv2.connectedComponentsWithStats(bw, 8)
    diams = [((stats[i, cv2.CC_STAT_WIDTH] + stats[i, cv2.CC_STAT_HEIGHT]) / 2)
             for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] >= 4]
    return float(np.median(diams)) if diams else None


def stone_run_extent(roi):
    """Horizontal fraction of the ROI spanned by the accent stones (proxy for
    coverage_fraction = stone-run length / structure length)."""
    if roi is None or roi.size == 0:
        return None
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    th = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    _, bw = cv2.threshold(th, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cols = np.where(bw.max(axis=0) > 0)[0]
    if cols.size == 0:
        return 0.0
    return float((cols.max() - cols.min()) / bw.shape[1])


def detect_raised_rail(roi):
    """Detect a long continuous straight metal edge below the stones (a raised
    channel rail). Returns (has_rail, detail) via Hough lines."""
    if roi is None or roi.size == 0:
        return False, "empty roi"
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 160)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=60,
                            minLineLength=int(roi.shape[1] * 0.5), maxLineGap=8)
    if lines is None:
        return False, "no long horizontal edge"
    for x1, y1, x2, y2 in lines[:, 0]:
        if abs(y2 - y1) <= 3 and abs(x2 - x1) >= roi.shape[1] * 0.5:
            return True, f"long straight edge len~{abs(x2 - x1)}"
    return False, "no long horizontal edge"


def estimate_elevation(bgr):
    """Coarse elevation estimate from the silhouette aspect (top-down => wide,
    side => tall). Sanity flag only; azimuth from a single view is unreliable."""
    comps, _, stats, _ = large_components(foreground_mask(bgr), k=1, min_area_frac=0.02)
    if not comps:
        return None
    _, i = comps[0]
    ar = stats[i, cv2.CC_STAT_HEIGHT] / max(stats[i, cv2.CC_STAT_WIDTH], 1)
    return float(np.clip(90 - ar * 45, 0, 90))
