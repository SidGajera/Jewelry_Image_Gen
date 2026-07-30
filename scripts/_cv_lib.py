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
    """Fraction of skin-tone pixels (YCrCb). CAD render ~0; worn photo >> 5%."""
    ycrcb = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    cr, cb = ycrcb[:, :, 1], ycrcb[:, :, 2]
    mask = (cr >= 135) & (cr <= 180) & (cb >= 85) & (cb <= 135)
    return float(mask.mean())


def detect_watermark(bgr):
    """(found, detail). OCR (pytesseract) for any repeated text/vendor overlay;
    fallback = periodic-tiling autocorrelation when tesseract is absent."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    if HAVE_OCR:
        txt = pytesseract.image_to_string(gray).lower()
        words = [w.strip(".,-_|") for w in txt.split() if len(w.strip(".,-_|")) >= 4]
        if words:
            from collections import Counter
            tok, n = Counter(words).most_common(1)[0]
            if n >= 3:
                return True, f"OCR repeated overlay token '{tok}' x{n}"
        if words:
            return True, f"OCR found text overlay: {words[:5]}"
        return False, "OCR: no text overlay"
    g = gray.astype(np.float32)
    hp = g - cv2.GaussianBlur(g, (0, 0), 3)
    hp -= hp.mean()
    f = np.fft.fft2(hp)
    ac = np.fft.fftshift(np.fft.ifft2(f * np.conj(f)).real)
    ac /= (ac.max() + 1e-9)
    h, w = ac.shape
    cy, cx = h // 2, w // 2
    ac[cy - 8:cy + 8, cx - 8:cx + 8] = 0
    peak = float(ac.max())
    return peak > 0.35, f"tiling-autocorr peak={peak:.2f} (OCR unavailable; heuristic)"


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
