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


_YUNET = None


def _yunet():
    global _YUNET
    if _YUNET is None:
        from pathlib import Path
        m = Path(__file__).resolve().parent.parent / "models" / "face_detection_yunet.onnx"
        if not m.exists():
            return None
        _YUNET = cv2.FaceDetectorYN.create(str(m), "", (320, 320), 0.6)
    return _YUNET


def detect_faces(bgr, conf=0.7):
    """Return list of (x, y, w, h) faces via YuNet DNN. [] if model missing."""
    fd = _yunet()
    if fd is None:
        return None  # model unavailable -> caller treats G14 as unmeasurable
    h, w = bgr.shape[:2]
    fd.setInputSize((w, h))
    _, faces = fd.detect(bgr)
    if faces is None:
        return []
    return [tuple(int(v) for v in f[:4]) for f in faces if f[-1] >= conf]


def laplacian_var(gray):
    if gray is None or gray.size == 0:
        return 0.0
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def background_velvet_stats(bgr, dilate_px=25):
    """Sample the background (outside the piece mask) for the G18 velvet check.
    Returns dict: bg_frac, sat, lum, gradient, texture, chan_spread.
      sat  = mean HSV saturation over bg (0-255); velvet ~ low.
      lum  = mean HSV value over bg (0-255); velvet ~ high.
      gradient = spread of block-luminance across the frame /255 (hard gradient / seamless sweep -> high).
      texture = std of the mid-frequency (band-pass) energy over bg; seamless paper ~ 0, velvet ~ moderate, props/edges ~ high.
      chan_spread = max-min of per-channel BGR means over bg /255 (coloured cast -> high).
    bg_frac < 0.15 -> not measurable (piece fills frame)."""
    h, w = bgr.shape[:2]
    mask = foreground_mask(bgr)
    k = max(3, int(dilate_px))
    dil = cv2.dilate(mask, np.ones((k, k), np.uint8))
    bg = dil == 0
    bg_frac = float(bg.mean())
    if bg_frac < 0.15:
        return {"bg_frac": bg_frac, "sat": None, "lum": None, "gradient": None,
                "texture": None, "chan_spread": None}
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    s, v = hsv[:, :, 1].astype(np.float64), hsv[:, :, 2].astype(np.float64)
    sat = float(s[bg].mean())
    lum = float(v[bg].mean())
    # per-channel colour cast
    b, g, r = bgr[:, :, 0].astype(np.float64), bgr[:, :, 1].astype(np.float64), bgr[:, :, 2].astype(np.float64)
    means = [b[bg].mean(), g[bg].mean(), r[bg].mean()]
    chan_spread = float((max(means) - min(means)) / 255.0)
    # frame-scale luminance gradient: block means over a grid, bg-only blocks
    gy, gx = 6, 6
    bh, bw = h // gy, w // gx
    blk = []
    for iy in range(gy):
        for ix in range(gx):
            sub_bg = bg[iy * bh:(iy + 1) * bh, ix * bw:(ix + 1) * bw]
            if sub_bg.mean() < 0.5:
                continue
            sub_v = v[iy * bh:(iy + 1) * bh, ix * bw:(ix + 1) * bw][sub_bg]
            blk.append(sub_v.mean())
    gradient = float((max(blk) - min(blk)) / 255.0) if len(blk) >= 2 else 0.0
    # mid-frequency (band-pass) texture: coarse-blur minus fine-blur, std over bg
    fine = cv2.GaussianBlur(v, (0, 0), 1.2)
    coarse = cv2.GaussianBlur(v, (0, 0), 6.0)
    band = fine - coarse
    texture = float(band[bg].std())
    return {"bg_frac": bg_frac, "sat": sat, "lum": lum, "gradient": gradient,
            "texture": texture, "chan_spread": chan_spread}


def skin_mask(bgr):
    ycrcb = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    cr, cb = ycrcb[:, :, 1], ycrcb[:, :, 2]
    ycc = (cr >= 135) & (cr <= 178) & (cb >= 90) & (cb <= 132)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    return ycc & (h <= 17) & (s >= 40) & (s <= 170) & (v >= 60) & (v <= 235)


def jewellery_region(bgr):
    """Bounding box of the brightest large cluster (stone/metal). (x,y,w,h) or None."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY)
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, _, stats, _ = cv2.connectedComponentsWithStats(th, 8)
    if n <= 1:
        return None
    i = 1 + int(np.argmax([stats[k, cv2.CC_STAT_AREA] for k in range(1, n)]))
    x, y, w, h = (stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP],
                  stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT])
    return (int(x), int(y), int(w), int(h))


def jewellery_area(bgr):
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return int((gray > 225).sum())


_HANDLM = None


def hand_landmarks(bgr, conf=0.3, max_hands=4):
    """MediaPipe Hands (Tasks API). Returns list of hands, each a list of 21
    (x,y) in FULL-RES pixels, or None if the model/asset is unavailable. Empty
    list = model ran, no hand found. Detection runs on multiple downscales
    (2048px renders overflow the model; ~512px is where a large hand locks in);
    normalized landmarks map straight back to full-res coordinates."""
    global _HANDLM
    from pathlib import Path
    m = Path(__file__).resolve().parent.parent / "models" / "hand_landmarker.task"
    if not m.exists():
        return None
    try:
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        if _HANDLM is None:
            _HANDLM = vision.HandLandmarker.create_from_options(vision.HandLandmarkerOptions(
                base_options=python.BaseOptions(model_asset_path=str(m)),
                num_hands=max_hands, min_hand_detection_confidence=conf,
                min_hand_presence_confidence=conf))
        h, w = bgr.shape[:2]
        for dw in (512, 640, 768, 384, 1024):
            small = cv2.resize(bgr, (dw, max(int(h * dw / w), 1)))
            rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
            res = _HANDLM.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
            if res.hand_landmarks:
                return [[(int(p.x * w), int(p.y * h)) for p in hand] for hand in res.hand_landmarks]
        return []
    except Exception:
        return None


def _gold_band_mask(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hh, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    gold = ((hh >= 12) & (hh <= 40) & (s >= 70) & (v >= 90)).astype(np.uint8) * 255
    white = (v > 235).astype(np.uint8) * 255              # stone
    band = cv2.morphologyEx(gold | white, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    return band


def band_spans_two_fingers(bgr):
    """MediaPipe-independent band-continuity / position check for ring-macro
    shots. A correctly worn ring sits on ONE finger: directly under the stone is
    continuous skin. Failure: an inter-finger GAP (non-skin wedge flanked by skin
    on both sides) sits under the stone / the band bridges it. Returns
    (verdict, detail): verdict in {'fail','pass','unmeasurable'}. Heuristic."""
    skin = skin_mask(bgr).astype(np.uint8)
    if skin.mean() < 0.03:
        return "unmeasurable", "no hand/skin present"
    band = _gold_band_mask(bgr)
    n, _, stats, cent = cv2.connectedComponentsWithStats(band, 8)
    if n <= 1:
        return "unmeasurable", "ring not segmented"
    i = 1 + int(np.argmax([stats[k, cv2.CC_STAT_AREA] for k in range(1, n)]))
    cx = int(cent[i][0]); by = stats[i, cv2.CC_STAT_TOP] + stats[i, cv2.CC_STAT_HEIGHT]
    bw = stats[i, cv2.CC_STAT_WIDTH]
    h, w = skin.shape
    # sample a strip just BELOW the ring (where band meets the finger)
    y0, y1 = min(by, h - 2), min(by + int(bw * 0.6), h - 1)
    x0, x1 = max(cx - bw // 2, 0), min(cx + bw // 2, w - 1)
    if y1 <= y0 or x1 <= x0:
        return "unmeasurable", "strip out of frame"
    gap_rows = 0
    for y in range(y0, y1):
        row = skin[y, x0:x1]
        if row.mean() < 0.15:
            continue
        idx = np.where(row > 0)[0]
        if idx.size < 3:
            continue
        # gap = a run of non-skin between two skin runs on the same row
        inner = row[idx.min():idx.max() + 1]
        gap = (inner == 0).sum()
        if gap >= 0.30 * inner.size:     # >=30% of the span under the ring is a gap
            gap_rows += 1
    frac = gap_rows / max(y1 - y0, 1)
    if frac >= 0.4:
        return "fail", f"inter-finger gap under ring in {frac:.0%} of rows (band spans two fingers)"
    return "pass", f"continuous finger under ring (gap rows {frac:.0%})"


def ring_on_one_finger(bgr):
    """G15 primary (MediaPipe): a ring encircles ONE finger. Detect hand
    landmarks, locate the ring, find the nearest finger, and verify (a) the ring
    centre sits between that finger's MCP and PIP knuckles, and (b) BOTH band
    arms map to the SAME finger. Returns (verdict, detail); verdict in
    {'fail','pass','unmeasurable'}. Unmeasurable when no hand is detected (tight
    macro) -> caller falls back to the band-gap heuristic."""
    lm = hand_landmarks(bgr)
    if lm is None:
        return "unmeasurable", "hand model unavailable"
    if not lm:
        return "unmeasurable", "no hand detected (macro crop)"
    if len(lm) >= 2:
        return "unmeasurable", "2+ overlapping hands; single-ring finger assignment unreliable (visual QC)"
    # locate the ring as the gold band WITHIN a hand's bounding box (not the
    # global brightest blob -- on a beach/sunset frame that is the sky).
    gold_all = _gold_band_mask(bgr)
    best = None
    for hand in lm:
        xs = [p[0] for p in hand]; ys = [p[1] for p in hand]
        x0, y0 = max(min(xs) - 40, 0), max(min(ys) - 40, 0)
        x1, y1 = min(max(xs) + 40, bgr.shape[1]), min(max(ys) + 40, bgr.shape[0])
        sub = np.zeros_like(gold_all); sub[y0:y1, x0:x1] = gold_all[y0:y1, x0:x1]
        ys2, xs2 = np.where(sub > 0)
        if xs2.size > 40 and (best is None or xs2.size > best[0]):
            best = (xs2.size, hand, int(np.mean(xs2)), int(np.mean(ys2)))
    if best is None:
        return "unmeasurable", "ring/band not found on any hand"
    _, hand, rx, ry = best
    fingers = {"index": (hand[5], hand[6]), "middle": (hand[9], hand[10]),
               "ring": (hand[13], hand[14]), "pinky": (hand[17], hand[18])}
    mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    nf = min(fingers, key=lambda f: (mid(*fingers[f])[0] - rx) ** 2 + (mid(*fingers[f])[1] - ry) ** 2)
    mcp, pip = fingers[nf]
    vx, vy = pip[0] - mcp[0], pip[1] - mcp[1]
    l2 = vx * vx + vy * vy or 1.0
    t = ((rx - mcp[0]) * vx + (ry - mcp[1]) * vy) / l2
    if not (-0.4 <= t <= 1.4):
        return "fail", f"ring not between {nf} knuckles (t={t:.2f}); over a knuckle or at the base/webbing"
    # perpendicular distance from ring centre to the finger axis: large => the
    # ring sits in an inter-finger gap (spans two fingers), not on the finger.
    px, py = mcp[0] + t * vx, mcp[1] + t * vy
    perp = ((rx - px) ** 2 + (ry - py) ** 2) ** 0.5
    mcps = sorted(fingers[f][0][0] for f in fingers)
    spacing = min((mcps[i + 1] - mcps[i]) for i in range(len(mcps) - 1)) if len(mcps) > 1 else 1e9
    if perp > 0.7 * spacing:
        return "fail", f"ring centre {int(perp)}px off the {nf} axis (>0.7x finger spacing {int(spacing)}) -- in an inter-finger gap / spans two fingers"
    return "pass", f"ring on the {nf} finger, between the knuckles (t={t:.2f}, off-axis {int(perp)}/{int(spacing)}px)"


def skin_hf_energy(bgr, hand):
    """High-frequency energy (Laplacian variance) over skin pixels in the hand's
    bounding box. Real skin (pores, creases, tendon shadows) is high; plastic/
    over-smoothed AI skin is low. Returns (energy or None)."""
    xs = [p[0] for p in hand]; ys = [p[1] for p in hand]
    x0, y0 = max(min(xs), 0), max(min(ys), 0)
    x1, y1 = min(max(xs), bgr.shape[1]), min(max(ys), bgr.shape[0])
    if x1 - x0 < 20 or y1 - y0 < 20:
        return None
    reg = np.zeros(bgr.shape[:2], bool); reg[y0:y1, x0:x1] = True
    m = reg & skin_mask(bgr)
    if m.sum() < 5000:
        return None
    lap = cv2.Laplacian(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float64), cv2.CV_64F)
    return float(lap[m].var())


def skin_hf_normalized(bgr):
    """Exposure-normalized skin high-frequency energy for G16 skin-realism.
    Laplacian variance over hand-skin pixels divided by mean-luma^2 (variance
    scales with contrast^2 ~ exposure^2), x1e4. Real skin ~90-135; waxy/plastic
    skin is lower. Returns value or None if not measurable. Uses the detected
    hand's bbox when available, else the whole skin mask."""
    lm = hand_landmarks(bgr)
    skin = skin_mask(bgr)
    if lm:
        h = max(lm, key=lambda H: (max(p[0] for p in H) - min(p[0] for p in H)) *
                (max(p[1] for p in H) - min(p[1] for p in H)))
        xs = [p[0] for p in h]; ys = [p[1] for p in h]
        reg = np.zeros(bgr.shape[:2], bool)
        reg[max(min(ys), 0):max(ys), max(min(xs), 0):max(xs)] = True
        m = reg & skin
    else:
        m = skin
    if m.sum() < 5000:
        return None
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float64)
    mean = gray[m].mean() or 1.0
    return float(cv2.Laplacian(gray, cv2.CV_64F)[m].var() / (mean * mean) * 1e4)


def stone_regions(bgr, min_area_frac=0.0009, max_area_frac=0.08):
    """Segment individual diamond/stone regions for the G24 clarity gate: bright,
    low-to-moderate-saturation specular blobs (diamonds read white/bright, not
    gold-saturated). Returns list of (bool_mask, (x,y,w,h)) per stone, largest
    first. Category-agnostic."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    v, s = hsv[:, :, 2], hsv[:, :, 1]
    bright = (v >= 165) & (s <= 95)                     # diamond facets: bright, low-sat
    bw = (bright * 255).astype(np.uint8)
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lbl, stats, _ = cv2.connectedComponentsWithStats(bw, 8)
    H, W = v.shape
    tot = H * W
    out = []
    for i in range(1, n):
        a = stats[i, cv2.CC_STAT_AREA]
        if a < tot * min_area_frac or a > tot * max_area_frac:
            continue
        x, y, w, h = (stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP],
                      stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT])
        out.append((lbl == i, (int(x), int(y), int(w), int(h)), int(a)))
    out.sort(key=lambda t: t[2], reverse=True)
    return [(m, box) for m, box, _ in out]


def stone_clarity_stats(bgr, rel_luma=0.45, speck_frac_max=0.004):
    """Per-stone clarity measurements for G24. For each resolved stone returns a
    dict: luma (mean grey), sharp (Laplacian var inside), cast (max per-channel
    mean spread / 255 = colour cast), speck (largest connected DARK blob area /
    stone area, dark = below rel_luma x stone-mean). Returns [] if <3 stones."""
    stones = stone_regions(bgr)
    if len(stones) < 3:
        return []
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float64)
    b, g, r = (bgr[:, :, 0].astype(np.float32), bgr[:, :, 1].astype(np.float32),
               bgr[:, :, 2].astype(np.float32))
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    out = []
    for m, (x, y, w, h) in stones:
        area = int(m.sum())
        if area < 60:
            continue
        vals = gray[m]
        mean = float(vals.mean())
        sharp = float(lap[m].var())
        means = [float(b[m].mean()), float(g[m].mean()), float(r[m].mean())]
        cast = (max(means) - min(means)) / 255.0
        # dark-speck: genuinely dark pixels WELL INSIDE the stone. Erode the stone
        # first so dark facet edges (a diamond's normal contrast) are excluded --
        # only an interior inclusion/dust blob should register.
        mu = m.astype(np.uint8)
        inner = cv2.erode(mu, np.ones((5, 5), np.uint8))
        speck = 0.0
        if inner.any():
            dark = ((inner > 0) & (gray < rel_luma * mean)).astype(np.uint8)
            if dark.any():
                nn, _, st, _ = cv2.connectedComponentsWithStats(dark, 8)
                if nn > 1:
                    biggest = max(st[k, cv2.CC_STAT_AREA] for k in range(1, nn))
                    speck = biggest / max(area, 1)
        out.append({"luma": mean, "sharp": sharp, "cast": cast, "speck": speck, "area": area})
    return out


def estimate_elevation(bgr):
    """Coarse elevation estimate from the silhouette aspect (top-down => wide,
    side => tall). Sanity flag only; azimuth from a single view is unreliable."""
    comps, _, stats, _ = large_components(foreground_mask(bgr), k=1, min_area_frac=0.02)
    if not comps:
        return None
    _, i = comps[0]
    ar = stats[i, cv2.CC_STAT_HEIGHT] / max(stats[i, cv2.CC_STAT_WIDTH], 1)
    return float(np.clip(90 - ar * 45, 0, 90))
