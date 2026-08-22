#!/usr/bin/env python3
"""RENDER GATES (blocking) — category-agnostic, one script for all categories.

Gates auto-skip when the relevant spec field is null. Each gate returns
{gate, status, measured, expected, detail}. status:
  pass  — measured within spec
  fail  — CONFIDENT violation -> reject the render
  skip  — spec field null / not applicable to this slot
  unmeasurable — could not measure reliably (e.g. shoulder occluded); never blocks

Only 'fail' rejects. Geometry gates are heuristic and calibrated against
tests/golden (tests/run_gates.py). Format, piece-count and text-overlay are
robust. Pairwise angle separation (G10) runs at the catalog level.
(The earlier cloth/white-balance QC lives in scripts/validate_render_legacy.py.)

Usage:
    python scripts/validate_render.py LR-0203 --image path.png --slot 02
    python scripts/validate_render.py LR-0203 --catalog dir/   # all slots + G10 pairwise
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import _cv_lib as cv  # noqa: E402

SEP_AZ, SEP_EL = 20, 15
GATES = json.loads((ROOT / "config" / "gates.json").read_text(encoding="utf-8"))["gates"]


def _g(gate, status, measured=None, expected=None, detail=""):
    return {"gate": gate, "status": status, "measured": measured, "expected": expected, "detail": detail}


def g1_format(path):
    """Delivered format comes from the LIVE pipeline profile (scripts/pipeline.py), never
    from a literal here — engine 1 delivers 2048x2048 native, engine 2 1536x1536."""
    import pipeline as pl
    fmt = pl.get_format()
    want = f"{fmt['width']}x{fmt['height']}"
    im = Image.open(path)
    w, h = im.size
    if not (w == fmt["width"] and h == fmt["height"]):
        return _g("G1_FORMAT", "fail", f"{w}x{h}", want, "non-square/size -> discard before all else")
    if im.format != "PNG":
        return _g("G1_FORMAT", "fail", im.format, "PNG", "not PNG")
    return _g("G1_FORMAT", "pass", f"{w}x{h} {im.format}", f"{want} PNG")


def _run_roi(run_id, rois):
    if run_id.endswith("left"):
        return rois["left"]
    if run_id.endswith("right"):
        return rois["right"]
    return rois["center_row"]


def g2_accent_count(bgr, spec):
    runs = spec.get("accent_runs") or []
    if not runs:
        return [_g("G2_ACCENT_COUNT", "skip", detail="no accent_runs in spec")]
    rois = cv.accent_rois(bgr)
    out = []
    for r in runs:
        n = cv.count_small_stones(_run_roi(r["id"], rois))
        exp, tol = r["count"], r.get("tolerance", 1)
        if not n:
            out.append(_g("G2_ACCENT_COUNT", "unmeasurable", n, f"{exp}+/-{tol}", f"{r['id']}: no stones resolved"))
        elif abs(n - exp) > tol:
            out.append(_g("G2_ACCENT_COUNT", "fail", n, f"{exp}+/-{tol}", f"{r['id']} count off"))
        else:
            out.append(_g("G2_ACCENT_COUNT", "pass", n, f"{exp}+/-{tol}", r["id"]))
    return out


def g3_accent_size(bgr, spec):
    runs = spec.get("accent_runs") or []
    if not runs or not runs[0].get("stone_dia_ratio_to_structure"):
        return [_g("G3_ACCENT_SIZE", "skip")]
    rois = cv.accent_rois(bgr)
    out = []
    for r in runs:
        roi = _run_roi(r["id"], rois)
        d = cv.small_stone_median_diam(roi)
        if d is None or roi.size == 0:
            out.append(_g("G3_ACCENT_SIZE", "unmeasurable", None, None, r["id"]))
            continue
        ratio = d / max(roi.shape[0], 1)          # ROI height ~ structure-width proxy
        exp = r["stone_dia_ratio_to_structure"]
        status = "fail" if ratio > exp * 2 else ("pass" if abs(ratio - exp) <= exp * r.get("size_tolerance", 0.15) + exp else "unmeasurable")
        out.append(_g("G3_ACCENT_SIZE", status, round(ratio, 3), f"{exp}", f"{r['id']} (fail only if grossly oversized)"))
    return out


def g4_accent_run(bgr, spec):
    runs = spec.get("accent_runs") or []
    if not runs or not runs[0].get("coverage_fraction"):
        return [_g("G4_ACCENT_RUN", "skip")]
    rois = cv.accent_rois(bgr)
    out = []
    for r in runs:
        ext = cv.stone_run_extent(_run_roi(r["id"], rois))
        exp = r["coverage_fraction"]
        if not ext:
            out.append(_g("G4_ACCENT_RUN", "unmeasurable", ext, f">={exp}", r["id"]))
        elif ext < exp * 0.8:
            out.append(_g("G4_ACCENT_RUN", "fail", round(ext, 2), f">={exp}", f"{r['id']} run too short"))
        else:
            out.append(_g("G4_ACCENT_RUN", "pass", round(ext, 2), f">={exp}", r["id"]))
    return out


def g5_setting_style(bgr, spec):
    flush = [r for r in (spec.get("accent_runs") or []) if str(r.get("setting", "")).startswith("flush")]
    if not flush:
        return [_g("G5_SETTING_STYLE", "skip")]
    rois = cv.accent_rois(bgr)
    for r in flush:
        rail, det = cv.detect_raised_rail(_run_roi(r["id"], rois))
        if rail:
            return [_g("G5_SETTING_STYLE", "fail", "raised_rail", "flush", f"{r['id']}: {det}")]
    return [_g("G5_SETTING_STYLE", "pass", "flush", "flush")]


def g6_stone_ratio(bgr, spec):
    stones = [s for s in spec.get("primary_stones", []) if s.get("lw_ratio")]
    if not stones:
        return [_g("G6_STONE_RATIO", "skip")]
    lws = cv.primary_ellipse_lw(bgr, expected_n=len(stones))
    if not lws:
        return [_g("G6_STONE_RATIO", "unmeasurable", None, None, "no primary stone resolved")]
    out = []
    for s, meas in zip(stones, lws):
        exp, tol = s["lw_ratio"], s.get("tolerance", 0.05)
        status = "pass" if abs(meas - exp) <= max(exp * tol, 0.15) else "fail"
        out.append(_g("G6_STONE_RATIO", status, round(meas, 2), f"{exp}+/-{tol}", f"{s['id']} L:W (shape drift)"))
    return out


def g7_setting_count(bgr, spec):
    se = spec.get("setting_elements")
    if not se or not se.get("count"):
        return [_g("G7_SETTING_COUNT", "skip")]
    gray = cv.cv2.cvtColor(bgr, cv.cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    roi = gray[int(h * 0.30):int(h * 0.62), int(w * 0.32):int(w * 0.68)]
    if roi.size == 0:
        return [_g("G7_SETTING_COUNT", "unmeasurable")]
    th = cv.cv2.morphologyEx(roi, cv.cv2.MORPH_TOPHAT, cv.cv2.getStructuringElement(cv.cv2.MORPH_ELLIPSE, (13, 13)))
    _, bw = cv.cv2.threshold(th, 0, 255, cv.cv2.THRESH_BINARY + cv.cv2.THRESH_OTSU)
    n, _, stats, _ = cv.cv2.connectedComponentsWithStats(bw, 8)
    ws = [stats[i, cv.cv2.CC_STAT_WIDTH] for i in range(1, n) if stats[i, cv.cv2.CC_STAT_AREA] >= 8]
    if not ws:
        return [_g("G7_SETTING_COUNT", "unmeasurable")]
    med = float(np.median(ws))
    broad = [x for x in ws if x > 1.6 * med]
    if broad:
        return [_g("G7_SETTING_COUNT", "fail", f"{len(broad)} broad", se["count"], "element >1.6x median width (split/broad/double)")]
    return [_g("G7_SETTING_COUNT", "unmeasurable", len(ws), se["count"], "width-uniformity ok; exact tip count heuristic")]


def g8_unauthorized(bgr, spec):
    if spec.get("halo", "none") != "none" or spec.get("under_head") != "plain":
        return [_g("G8_UNAUTHORIZED", "skip", detail="spec authorizes halo/under-head stones")]
    h, w = bgr.shape[:2]
    under = bgr[int(h * 0.52):int(h * 0.66), int(w * 0.30):int(w * 0.70)]
    n = cv.count_small_stones(under)
    if n and n >= 4:
        return [_g("G8_UNAUTHORIZED", "fail", n, 0, "stone cluster under primary (hidden halo / basket pave)")]
    return [_g("G8_UNAUTHORIZED", "pass", n or 0, 0)]


def g9_piece_count(bgr):
    n = cv.count_pieces(bgr)
    if n == 0:
        return [_g("G9_PIECE_COUNT", "unmeasurable", 0, 1, "no piece segmented")]
    if n > 1:
        return [_g("G9_PIECE_COUNT", "fail", n, 1, "duplicate/ghost piece in frame")]
    return [_g("G9_PIECE_COUNT", "pass", 1, 1)]


def g10_angle_single(bgr, slot):
    el = cv.estimate_elevation(bgr)
    if el is None:
        return _g("G10_ANGLE", "unmeasurable", None, slot["elevation"])
    status = "pass" if abs(el - slot["elevation"]) <= 25 else "fail"
    return _g("G10_ANGLE", status, round(el, 1), slot["elevation"], "elevation sanity vs declared")


def g11_logo(bgr, slot):
    if slot["group"] != "studio":
        return [_g("G11_LOGO", "skip", detail="lifestyle slot")]
    logo = next((ROOT / "assets" / f"logo.{e}" for e in ("png", "webp", "jpg") if (ROOT / "assets" / f"logo.{e}").exists()), None)
    wm, det = cv.detect_watermark(bgr)
    if wm and logo is None:
        return [_g("G11_LOGO", "fail", "text_overlay", "none", f"AI-drawn text/logo on studio render: {det}")]
    return [_g("G11_LOGO", "pass", detail="no unauthorized text" if logo is None else "locked logo asset present")]


def g18_background(bgr, slot):
    """G18 BACKGROUND_VELVET (studio slots only). The studio background must be
    plain pure-white velvet: low saturation, high luminance, fine mid-frequency
    fabric texture. Rejects coloured backgrounds, seamless paper, hard gradients,
    props. Thresholds from config/gates.json."""
    if slot.get("group") != "studio":
        return [_g("G18_BACKGROUND", "skip", detail="lifestyle slot")]
    import json as _json
    t = (_json.loads((ROOT / "config" / "gates.json").read_text(encoding="utf-8"))
         ["gates"]["G18_BACKGROUND"]["thresholds"])
    s = cv.background_velvet_stats(bgr)
    if s["sat"] is None or s["bg_frac"] < t["min_bg_frac"]:
        return [_g("G18_BACKGROUND", "unmeasurable", f"bg_frac={s['bg_frac']:.2f}",
                   detail="piece fills frame; too little background to sample")]
    fails = []
    if s["sat"] > t["sat_max"] or s["chan_spread"] > t["chan_spread_max"]:
        fails.append(f"coloured background (sat={s['sat']:.1f}, chan={s['chan_spread']:.3f})")
    if s["lum"] < t["lum_min"]:
        fails.append(f"not white/too dark (lum={s['lum']:.1f})")
    if s["gradient"] > t["gradient_max"]:
        fails.append(f"hard gradient/seamless sweep (grad={s['gradient']:.3f})")
    if s["texture"] < t["texture_min"]:
        fails.append(f"seamless paper, no fabric texture (tex={s['texture']:.2f})")
    elif s["texture"] > t["texture_max"]:
        fails.append(f"busy background/props (tex={s['texture']:.2f})")
    if fails:
        return [_g("G18_BACKGROUND", "fail", f"sat={s['sat']:.1f} lum={s['lum']:.1f} tex={s['texture']:.2f}",
                   "plain white velvet", "; ".join(fails))]
    return [_g("G18_BACKGROUND", "pass", f"sat={s['sat']:.1f} lum={s['lum']:.1f} tex={s['texture']:.2f}",
               "plain white velvet")]


def invent_block(sku, slot):
    """SOURCE_COVERAGE_REQUIRED (studio): returns (unmet_items, required_files, az_ok).
    A studio slot is blocked unless (a) every item in slot.reveals is established
    by a SUPPLIED source view (config/view_coverage.json x specs/<SKU>_views.json),
    AND (b) some source view is within 45deg azimuth. No inference / category priors."""
    import json as _json
    cov = _json.loads((ROOT / "config" / "view_coverage.json").read_text(encoding="utf-8"))
    est, reqf = cov["establishes"], cov["required_filename"]
    vp = ROOT / "specs" / f"{sku}_views.json"
    views = _json.loads(vp.read_text(encoding="utf-8")).get("views", []) if vp.exists() else []
    supplied_types = {v.get("type") for v in views if v.get("type")}
    supplied_est = set().union(*(set(est.get(t, [])) for t in supplied_types)) if supplied_types else set()
    unmet = [i for i in slot.get("reveals", []) if i not in supplied_est]
    req = set()
    for i in unmet:
        for t, items in est.items():
            if i in items:
                req.add(reqf.get(t, t))
    saz, sel = slot["azimuth"], slot["elevation"]
    az_ok = any(min(abs(v["azimuth"] - saz) % 360, 360 - abs(v["azimuth"] - saz) % 360) <= 45 for v in views)
    return unmet, sorted(req), az_ok


def g_invent(sku, slot):
    """G-INVENT (studio slots blocking). Lifestyle exempt (worn camera has no CAD
    equivalent; docs/00 geometry-vs-camera)."""
    if slot.get("group") != "studio":
        return [_g("G_INVENT", "skip", detail="lifestyle: worn camera has no CAD equivalent")]
    unmet, req, az_ok = invent_block(sku, slot)
    if unmet or not az_ok:
        why = (f"reveals {unmet} not established by any supplied view" if unmet
               else "no source view within 45deg azimuth")
        return [_g("G_INVENT", "fail", f"missing {req or 'source view'}", "source-established",
                   f"invention: {why}. Required: {req}")]
    return [_g("G_INVENT", "pass", "covered", "source-established", "every revealed item established by a supplied view")]


def g12_marks(bgr, slot):
    """MARKS (P7): no source watermark / vendor mark / engraved maker's mark
    carried into the render; inner shank stays plain. BLOCKING on a tiled/vendor
    watermark (robust). An isolated engraved glyph on the polished band is
    reported ADVISORY (subtle; false-positive prone) rather than blocking."""
    wm, det = cv.detect_watermark(bgr)
    if wm:
        return [_g("G12_MARKS", "fail", "watermark/vendor mark", "none", det)]
    # advisory: isolated small dark glyph on an otherwise smooth bright-metal band
    import numpy as np
    gray = cv.cv2.cvtColor(bgr, cv.cv2.COLOR_BGR2GRAY)
    metal = (gray > 150).astype("uint8")
    dark_on_metal = ((gray < 90).astype("uint8") &
                     cv.cv2.dilate(metal, np.ones((15, 15), np.uint8)))
    n, _, stats, _ = cv.cv2.connectedComponentsWithStats(dark_on_metal, 8)
    h, w = gray.shape
    glyphs = [i for i in range(1, n) if 20 <= stats[i, cv.cv2.CC_STAT_AREA] <= h * w * 0.0008]
    if glyphs:
        return [_g("G12_MARKS", "unmeasurable", f"{len(glyphs)} possible band marks", "0",
                   "advisory: verify inner shank is plain (no engraved mark)")]
    return [_g("G12_MARKS", "pass", "no watermark, band clean", "none")]


def g16_skin_realism(bgr, slot):
    """SKIN REALISM (lifestyle): exposure-normalized high-frequency energy in the
    hand region. Below threshold = plastic/over-smoothed skin = FAIL. Threshold
    from config/gates.json (provisional until locked on labelled goldens)."""
    if slot.get("group") != "lifestyle":
        return [_g("G16_SKIN_REALISM", "skip", detail="studio slot")]
    import json as _json
    thr = (_json.loads((ROOT / "config" / "gates.json").read_text(encoding="utf-8"))
           ["gates"].get("G16_SKIN_REALISM", {}).get("threshold", 70))
    e = cv.skin_hf_normalized(bgr)
    if e is None:
        return [_g("G16_SKIN_REALISM", "unmeasurable", None, thr, "no hand-skin region")]
    if e < thr:
        return [_g("G16_SKIN_REALISM", "fail", round(e, 1), f">={thr}", "plastic / over-smoothed skin")]
    return [_g("G16_SKIN_REALISM", "pass", round(e, 1), f">={thr}", "real skin texture")]


def g15_hand_anatomy(bgr, slot):
    """HAND ANATOMY (lifestyle): a ring encircles ONE finger. Checks (1) hand/
    finger plausibility via MediaPipe, (2) band continuity — both arms on the
    SAME finger (a band bridging an inter-finger gap = spans two fingers), (3)
    position between knuckles / not at the webbing. BLOCKING once calibrated on a
    FAIL golden; advisory until then. Returns unmeasurable when neither MediaPipe
    nor the band heuristic can assess (e.g. a tight macro with no gap resolvable)."""
    if slot.get("group") != "lifestyle":
        return [_g("G15_HAND_ANATOMY", "skip", detail="studio slot")]
    # PRIMARY: MediaPipe landmark band-arm trace (blocking-capable when a hand is detected)
    verdict, det = cv.ring_on_one_finger(bgr)
    if verdict == "fail":
        return [_g("G15_HAND_ANATOMY", "fail", "ring not on one finger", "one finger", det)]
    if verdict == "pass":
        return [_g("G15_HAND_ANATOMY", "pass", "ring on one finger", "one finger", det)]
    # FALLBACK: band-gap heuristic when MediaPipe cannot see the hand (macro crop)
    hv, hdet = cv.band_spans_two_fingers(bgr)
    if hv == "fail":
        return [_g("G15_HAND_ANATOMY", "fail", "band spans two fingers", "one finger", hdet)]
    return [_g("G15_HAND_ANATOMY", "unmeasurable", None, None, f"{det}; heuristic: {hdet}")]


def g14_content(bgr, slot):
    """CONTENT COMPLIANCE (lifestyle only): jewellery is the subject, people are
    set dressing. FAIL on (1) two faces within one face-width, (2) any face
    sharper than the ring region, (3) combined person area > jewellery area x6."""
    if slot.get("group") != "lifestyle":
        return [_g("G14_CONTENT", "skip", detail="studio slot")]
    faces = cv.detect_faces(bgr)
    if faces is None:
        return [_g("G14_CONTENT", "unmeasurable", None, None, "face model unavailable")]
    # (1) two faces close together
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            (x1, y1, w1, h1), (x2, y2, w2, h2) = faces[i], faces[j]
            c1 = (x1 + w1 / 2, y1 + h1 / 2)
            c2 = (x2 + w2 / 2, y2 + h2 / 2)
            dist = ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) ** 0.5
            if dist < max(w1, w2):
                return [_g("G14_CONTENT", "fail", "2 faces adjacent", "<=1 or spaced",
                           "two faces within one face-width (couple/kiss)")]
    # (2) any face sharper than the ring region
    ring = cv.jewellery_region(bgr)
    gray = cv.cv2.cvtColor(bgr, cv.cv2.COLOR_BGR2GRAY)
    if ring:
        x, y, w, h = ring
        ring_var = cv.laplacian_var(gray[y:y + h, x:x + w])
        for (fx, fy, fw, fh) in faces:
            fv = cv.laplacian_var(gray[max(fy, 0):fy + fh, max(fx, 0):fx + fw])
            if fv > ring_var:
                return [_g("G14_CONTENT", "fail", f"face sharper ({fv:.0f}>{ring_var:.0f})",
                           "ring sharpest", "a face is in sharper focus than the ring")]
    # (3) couple-as-subject: TWO PROMINENT faces (each large in frame). A single
    # allowed model, or an allowed SECONDARY partner (small / softly out of focus,
    # per the approved pose set), stays below the prominence bar and passes; rules
    # 1 and 2 still catch adjacency and any in-focus face.
    hh, ww = bgr.shape[:2]
    prominent = [f for f in faces if (f[2] * f[3]) >= 0.03 * hh * ww]
    if len(prominent) >= 2:
        return [_g("G14_CONTENT", "fail", f"{len(prominent)} prominent faces", "<=1 prominent",
                   "two people prominently framed (couple is the subject)")]
    return [_g("G14_CONTENT", "pass", f"faces={len(faces)} prominent={len(prominent)}", "compliant")]


def _palette_sig(bgr):
    hsv = cv.cv2.cvtColor(bgr, cv.cv2.COLOR_BGR2HSV)
    return float(np.median(hsv[:, :, 0])), float(hsv[:, :, 2].mean())


def g17_theme(sku):
    """THEME_PER_CATALOG (catalog-level, lifestyle). (a) CONSISTENCY: the six
    lifestyle renders cluster in hue+luminance (an outlier breaks the theme).
    (b) DISTINCTNESS: this catalog's mean palette differs from the last 6 catalogs
    (colour distance) -- else a theme collision. (c) banned wardrobe is prompt-
    enforced + advisory. Returns {gate,status,detail}."""
    import json as _json
    matrix = _json.loads((ROOT / "config" / "angle_matrix.json").read_text(encoding="utf-8"))
    spec = _json.loads((ROOT / "specs" / f"{sku}.json").read_text(encoding="utf-8"))
    life = [s["slot"] for s in matrix["categories"][spec["category"]]["slots"] if s["group"] == "lifestyle"]
    rdir = ROOT / "deliveries" / sku
    sigs = []
    for sl in life:
        hits = sorted(rdir.glob(f"{sl}_*.png"))
        if hits:
            sigs.append(_palette_sig(cv.load_bgr(hits[0])))
    if len(sigs) < 4:
        return _g("G17_THEME", "unmeasurable", None, None, "fewer than 4 lifestyle renders")
    hues = np.array([s[0] for s in sigs]); lums = np.array([s[1] for s in sigs])
    # (a) consistency: outlier if a render is >40 hue or >70 luma from the median
    hmed, lmed = np.median(hues), np.median(lums)
    out = [life[i] for i in range(len(sigs)) if abs(hues[i] - hmed) > 40 or abs(lums[i] - lmed) > 70]
    if out:
        return _g("G17_THEME", "fail", f"outliers {out}", "one cluster", f"slot(s) {out} break catalog theme")
    # (b) distinctness vs last 6 catalogs in the theme ledger
    led = _json.loads((ROOT / "memory" / "theme_ledger.json").read_text(encoding="utf-8")) if (ROOT / "memory" / "theme_ledger.json").exists() else []
    cat_sig = (float(hmed), float(lmed))
    for e in [x for x in led if x.get("sku") != sku][-6:]:
        if "sig" in e:
            d = ((cat_sig[0] - e["sig"][0]) ** 2 + (cat_sig[1] - e["sig"][1]) ** 2) ** 0.5
            if d < 12:
                return _g("G17_THEME", "fail", f"dist {d:.0f}", ">=12", f"theme collision with {e['sku']}")
    return _g("G17_THEME", "pass", f"hue~{hmed:.0f} lum~{lmed:.0f}", "clustered+distinct", "consistent + distinct")


def g20_min_subject_scale(bgr, slot):
    """MINIMUM SUBJECT SCALE (lifestyle, BLOCKING): the jewellery bounding box must
    be >= lifestyle_min of frame area (>= macro_min on the two macro lifestyle slots).
    Below threshold the model has no pixel budget to resolve the real geometry and
    substitutes a generic piece -> FAIL, regenerate with tighter framing."""
    if slot.get("group") != "lifestyle":
        return [_g("G20_MIN_SUBJECT_SCALE", "skip", detail="studio slot")]
    import cv2
    import numpy as _np
    import json as _json
    cfg = _json.loads((ROOT / "config" / "gates.json").read_text(encoding="utf-8"))["gates"].get("G20_MIN_SUBJECT_SCALE", {})
    lo = cfg.get("macro_min", 0.25) if slot.get("macro") else cfg.get("lifestyle_min", 0.12)
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    gold = ((H >= 13) & (H <= 45) & (S >= 55) & (V >= 70)).astype("uint8") * 255
    spark = ((V >= 235) & (S <= 60)).astype("uint8") * 255
    m = cv2.bitwise_or(gold, spark)
    m = cv2.dilate(m, _np.ones((9, 9), "uint8"), iterations=2)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, _np.ones((25, 25), "uint8"))
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return [_g("G20_MIN_SUBJECT_SCALE", "unmeasurable", None, f">={lo:.0%}", "no jewellery region isolated")]
    x, y, bw, bh = cv2.boundingRect(max(cnts, key=cv2.contourArea))
    frac = (bw * bh) / float(h * w)
    if frac < lo:
        return [_g("G20_MIN_SUBJECT_SCALE", "fail", f"{frac:.1%}", f">={lo:.0%}", "ring too small in frame; tighten to macro framing")]
    return [_g("G20_MIN_SUBJECT_SCALE", "pass", f"{frac:.1%}", f">={lo:.0%}", "subject large enough")]


def g21_stone_ratio(bgr, spec, slot):
    """STONE RATIO (BLOCKING): resolve the bright diamond blobs, compare the
    centre:flanker size ratio to spec.stone_equality within +/-ratio_tol, and assert
    the distinct-stone count is not short of spec (the generic-substitute failure).
    Unmeasurable when stones cannot be resolved (small lifestyle crops -> G20 gates first)."""
    se = spec.get("stone_equality")
    if not se:
        return [_g("G21_STONE_RATIO", "skip", detail="no stone_equality in spec")]
    import cv2
    import numpy as _np
    import statistics as _st
    tol = se.get("ratio_tol", 0.10)
    want = se.get("centre_flanker_ratio")
    total = se.get("total_stones") or 0
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    S, V = hsv[..., 1], hsv[..., 2]
    stones = (((V >= 170) & (S <= 70)).astype("uint8")) * 255
    stones = cv2.morphologyEx(stones, cv2.MORPH_OPEN, _np.ones((3, 3), "uint8"))
    cnts, _ = cv2.findContours(stones, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    minA = 0.00003 * h * w
    areas = sorted((cv2.contourArea(c) for c in cnts if cv2.contourArea(c) >= minA), reverse=True)
    if len(areas) < 2:
        return [_g("G21_STONE_RATIO", "unmeasurable", None, None, "stones not resolvable (check G20 scale)")]
    n = len(areas)
    if total and n < total - 2:
        return [_g("G21_STONE_RATIO", "fail", f"{n} stones", f"{total}", "too few distinct stones; generic substitute")]
    flank = _st.median(areas[1:min(len(areas), 4)])
    ratio = (areas[0] / flank) ** 0.5 if flank > 0 else 0.0
    if want and abs(ratio - want) / want > tol:
        return [_g("G21_STONE_RATIO", "fail", f"{ratio:.2f}", f"{want}+/-{tol:.0%}", "centre:flanker size ratio out of range")]
    return [_g("G21_STONE_RATIO", "pass", f"ratio {ratio:.2f}, {n} stones", f"{want}+/-{tol:.0%}, {total}", "stone ratios ok")]


def g22_stone_within_finger(bgr, slot, spec=None):
    """RING SCALE ON HAND (lifestyle, BLOCKING): the centre stone must sit WITHIN
    the finger's width — never wider than the finger. Detect the centre-stone blob
    width and the skin (finger) width at the stone's row; FAIL if stone is wider
    than the finger (× tol). Reject 'cocktail-huge' diamonds.

    Defined for CENTRE-STONE pieces only. A band with NO centre stone (empty
    primary_stones — e.g. an east-west marquise / eternity half-band) has no
    single centre stone to measure; the brightest blob is the whole accent ROW,
    which legitimately spans the finger top, so the blob detector false-positives.
    For such specs G22 is not applicable (skip); band scale is verified by the
    accent-size gates (G3) and documented visual QC instead."""
    if slot.get("group") != "lifestyle":
        return [_g("G22_STONE_WITHIN_FINGER", "skip", detail="studio slot")]
    if spec is not None and not (spec.get("primary_stones") or []):
        return [_g("G22_STONE_WITHIN_FINGER", "skip", detail="no centre stone (band); G22 measures a centre stone — N/A, scale via G3 + visual QC")]
    import cv2
    import numpy as _np
    import json as _json
    tol = _json.loads((ROOT / "config" / "gates.json").read_text(encoding="utf-8"))["gates"].get("G22_STONE_WITHIN_FINGER", {}).get("tol", 1.05)
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV); S, V = hsv[..., 1], hsv[..., 2]
    stone = (((V >= 190) & (S <= 55)).astype("uint8")) * 255
    stone = cv2.morphologyEx(stone, cv2.MORPH_OPEN, _np.ones((5, 5), "uint8"))
    cnts, _ = cv2.findContours(stone, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = [c for c in cnts if cv2.contourArea(c) >= 0.0005 * h * w]
    if not cnts:
        return [_g("G22_STONE_WITHIN_FINGER", "unmeasurable", None, None, "no centre stone resolved")]
    sx, sy, sw, sh = cv2.boundingRect(max(cnts, key=cv2.contourArea))
    ycr = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    Y, Cr, Cb = ycr[..., 0], ycr[..., 1], ycr[..., 2]
    skin = ((Cr >= 135) & (Cr <= 180) & (Cb >= 85) & (Cb <= 135) & (Y >= 40)).astype("uint8")
    band = skin[max(0, sy + sh):min(h, sy + sh + max(8, sh // 2)), :]  # skin just below the stone
    if band.size == 0 or band.sum() < 50:
        return [_g("G22_STONE_WITHIN_FINGER", "unmeasurable", None, None, "no finger skin resolved under stone")]
    col = band.sum(axis=0); xc = sx + sw // 2
    left = xc
    while left > 0 and col[left] > 0:
        left -= 1
    right = xc
    while right < w - 1 and col[right] > 0:
        right += 1
    finger_w = max(1, right - left)
    ratio = sw / float(finger_w)
    if ratio > tol:
        return [_g("G22_STONE_WITHIN_FINGER", "fail", f"{ratio:.2f}", f"<={tol}", "centre stone wider than the finger; oversized on hand")]
    return [_g("G22_STONE_WITHIN_FINGER", "pass", f"{ratio:.2f}", f"<={tol}", "stone within finger width")]


def g24_clarity(bgr, slot):
    """CLARITY_CHECK (blocking): every stone crystal/water-clear. Measures per
    stone (a) luminance, (b) facet sharpness, (c) colour neutrality, (d) DARK
    SPECK (inclusion/dust) blobs, (e) consistency. Confident fail = reject.
    Unmeasurable (<3 stones resolve) never blocks."""
    cfg = GATES.get("G24_CLARITY_CHECK", {})
    rel = float(cfg.get("dark_speck_rel_luma", 0.45))
    speck_max = float(cfg.get("dark_speck_max_frac", 0.004))
    stats = cv.stone_clarity_stats(bgr, rel_luma=rel, speck_frac_max=speck_max)
    if len(stats) < 3:
        return [_g("G24_CLARITY_CHECK", "unmeasurable", len(stats), ">=3 stones",
                   "too few stones resolved to judge clarity")]
    lumas = np.array([s["luma"] for s in stats])
    specks = np.array([s["speck"] for s in stats])
    casts = np.array([s["cast"] for s in stats])
    # (d) dark-speck / inclusion-or-dust: any stone with a dark blob over the max fraction
    speck_hits = int((specks > speck_max).sum())
    if speck_hits >= 1:
        worst = float(specks.max())
        return [_g("G24_CLARITY_CHECK", "fail", f"{worst:.3%}", f"<={speck_max:.2%}",
                   f"dark speck/inclusion or dust inside {speck_hits} stone(s) (blob {worst:.2%} of stone)")]
    # (a) luminance floor: a materially dark (milky/shadowed) stone vs the set
    med = float(np.median(lumas))
    dark_stone = float(lumas.min())
    if med >= 120 and dark_stone < 0.55 * med:
        return [_g("G24_CLARITY_CHECK", "fail", f"{dark_stone:.0f}", f">={0.55*med:.0f}",
                   "a stone reads materially duller/milkier than its neighbours (in shadow or hazy)")]
    # (c) colour cast: only an EXTREME cast fails — warm golden-hour lifestyle light
    # legitimately pushes clean stones to ~0.24, so this is a loose guard, not the
    # primary check (speck + luminance do the real work). Calibrated FP=0.
    if float(np.median(casts)) > 0.34:
        return [_g("G24_CLARITY_CHECK", "fail", f"{float(np.median(casts)):.2f}", "<=0.34",
                   "stones carry an extreme colour cast (not colourless)")]
    return [_g("G24_CLARITY_CHECK", "pass", f"{len(stats)} stones",
               f"speck<={speck_max:.2%}", "stones read clean and bright")]


def g25_gold_check(bgr, spec, slot):
    """GOLD_CHECK (blocking): rendered metal is GOLD of the spec's locked colour.
    Karat (18K) is not visually measurable -> audited vs the Etsy listing, not here.
    Conservative: cross-family colour fails only on neutral-lit STUDIO slots (warm
    lifestyle light legitimately shifts hue); a white-gold spec reading strongly
    coloured fails on any slot. Unmeasurable never blocks."""
    metal = (spec.get("metal") or "yellow_gold")
    want_white = ("white" in metal) or ("platinum" in metal) or ("silver" in metal)
    hue = cv.metal_hue_peak(bgr)   # None => low-saturation neutral (white metal)
    studio = slot.get("group") != "lifestyle"
    if hue is None:
        if want_white:
            return [_g("G25_GOLD_CHECK", "pass", "low-sat", "white/neutral", "neutral white metal")]
        return [_g("G25_GOLD_CHECK", "unmeasurable", "low-sat", metal,
                   "metal low-saturation under this light; gold colour not confidently measured")]
    if want_white:
        return [_g("G25_GOLD_CHECK", "fail", f"hue {hue}", "neutral/low-sat",
                   "spec is white gold/platinum but metal reads strongly coloured (yellow/rose)")]
    is_rose = hue <= 12
    is_yellow = 15 <= hue <= 45
    if studio and "rose" in metal and is_yellow:
        return [_g("G25_GOLD_CHECK", "fail", f"hue {hue}", "rose ~3-12",
                   "spec is rose gold but metal reads yellow")]
    if studio and "yellow" in metal and is_rose:
        return [_g("G25_GOLD_CHECK", "fail", f"hue {hue}", "yellow ~15-40",
                   "spec is yellow gold but metal reads rose")]
    return [_g("G25_GOLD_CHECK", "pass", f"hue {hue}", metal, "metal reads as the spec gold colour")]


def _circle_fit(xs, ys):
    """Kasa algebraic circle fit. Returns (cx, cy) or None."""
    A = np.c_[xs, ys, np.ones(len(xs))]
    b = xs ** 2 + ys ** 2
    try:
        sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    except Exception:
        return None
    return sol[0] / 2.0, sol[1] / 2.0


def _rect_long_axis_deg(rect):
    """Angle (deg, 0..180) of a minAreaRect's LONG side in image coords."""
    (_c, (w, h), ang) = rect
    if w < h:
        ang = ang + 90.0
    return ang % 180.0


def g27_orientation(bgr, spec, slot):
    """G27 ORIENTATION_CHECK (BLOCKING). Each stone's long axis must match the
    spec's orientation RELATIVE TO THE LOCAL SHANK TANGENT:
      parallel  (east-west)  -> long-axis vs tangent diff <= 15 deg
      perpendicular(north-south) -> diff in 75..105 deg
    Also asserts coverage: a spec-declared PARTIAL band must show a plain-metal
    gap in the stone ring; a full-eternity render (no gap) FAILS.
    Method: segment bright low-sat stones -> minAreaRect long axis; fit a circle
    to the stone centroids -> local tangent = radial + 90 deg. Needs >=5 stones,
    else 'unmeasurable' (never blocks — small/oblique lifestyle crops)."""
    cfg = spec.get("g27")
    if not cfg or not cfg.get("axis"):
        return [_g("G27_ORIENTATION_CHECK", "skip", detail="no g27 axis in spec")]
    import cv2
    axis = cfg["axis"]                       # "parallel" | "perpendicular"
    coverage = cfg.get("coverage", "partial")  # "partial" | "full"
    tol_par = float(cfg.get("parallel_tol_deg", 15))
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    S, V = hsv[..., 1], hsv[..., 2]
    m = (((V >= 165) & (S <= 75)).astype("uint8")) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), "uint8"))
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lo, hi = 0.00006 * h * w, 0.02 * h * w
    stones = []  # (cx, cy, long_axis_deg)
    for c in cnts:
        a = cv2.contourArea(c)
        if a < lo or a > hi or len(c) < 5:
            continue
        rect = cv2.minAreaRect(c)
        (cx, cy), (rw, rh), _ = rect
        if min(rw, rh) < 2 or max(rw, rh) / max(min(rw, rh), 1) < 1.15:
            continue  # too round to have a reliable long axis
        stones.append((cx, cy, _rect_long_axis_deg(rect)))
    if len(stones) < 5:
        return [_g("G27_ORIENTATION_CHECK", "unmeasurable", len(stones), ">=5 stones",
                   "too few stones resolved to fit the arc (oblique/occluded crop)")]
    xs = np.array([s[0] for s in stones]); ys = np.array([s[1] for s in stones])
    ctr = _circle_fit(xs, ys)
    if ctr is None:
        return [_g("G27_ORIENTATION_CHECK", "unmeasurable", None, None, "circle fit failed")]
    cx, cy = ctr
    offenders, diffs = 0, []
    for (x, y, la) in stones:
        rad = np.degrees(np.arctan2(y - cy, x - cx))
        tan = (rad + 90.0) % 180.0
        d = abs(la - tan) % 180.0
        d = min(d, 180.0 - d)                # fold to 0..90
        diffs.append(d)
    # d is folded to 0..90: parallel -> d near 0 (<=tol); perpendicular -> d near 90 (>=75)
    if axis == "perpendicular":
        offenders = sum(1 for d in diffs if d < 75.0)
    else:
        offenders = sum(1 for d in diffs if d > tol_par)
    # coverage: angular span covered by stones; a PARTIAL band must leave a gap
    angs = np.sort(np.degrees(np.arctan2(ys - cy, xs - cx)) % 360.0)
    gaps = np.diff(np.r_[angs, angs[0] + 360.0])
    max_gap = float(gaps.max())
    frac_off = offenders / float(len(stones))
    fails = []
    if frac_off > 0.15 and offenders >= 2:
        want = "long axis PARALLEL to shank (east-west)" if axis == "parallel" else "long axis PERPENDICULAR to shank (north-south)"
        fails.append(f"{offenders}/{len(stones)} stones misoriented (want {want}; median diff {np.median(diffs):.0f} deg)")
    if coverage == "partial" and max_gap < 25.0:
        fails.append(f"no plain-shank gap (max angular gap {max_gap:.0f} deg) -> looks like a FULL eternity, spec says partial")
    if coverage == "full" and max_gap > 60.0:
        fails.append(f"stone row broken (gap {max_gap:.0f} deg) -> spec says full eternity")
    if fails:
        return [_g("G27_ORIENTATION_CHECK", "fail", f"off={offenders}/{len(stones)} gap={max_gap:.0f}",
                   f"{axis}, {coverage}", "; ".join(fails))]
    return [_g("G27_ORIENTATION_CHECK", "pass", f"off={offenders}/{len(stones)} gap={max_gap:.0f}",
               f"{axis}, {coverage}", "orientation + coverage match source")]


def validate_image(sku, image_path, slot):
    spec = json.loads((ROOT / "specs" / f"{sku}.json").read_text(encoding="utf-8"))
    res = [g1_format(image_path)]
    if res[0]["status"] == "fail":
        return res
    bgr = cv.load_bgr(image_path)
    res += g2_accent_count(bgr, spec)
    res += g3_accent_size(bgr, spec)
    res += g4_accent_run(bgr, spec)
    res += g5_setting_style(bgr, spec)
    res += g6_stone_ratio(bgr, spec)
    res += g7_setting_count(bgr, spec)
    res += g8_unauthorized(bgr, spec)
    res += g9_piece_count(bgr)
    res.append(g10_angle_single(bgr, slot))
    res += g11_logo(bgr, slot)
    res += g_invent(sku, slot)
    res += g12_marks(bgr, slot)
    res += g14_content(bgr, slot)
    res += g15_hand_anatomy(bgr, slot)
    res += g16_skin_realism(bgr, slot)
    res += g18_background(bgr, slot)
    res += g20_min_subject_scale(bgr, slot)
    res += g21_stone_ratio(bgr, spec, slot)
    res += g22_stone_within_finger(bgr, slot, spec)
    res += g24_clarity(bgr, slot)
    res += g25_gold_check(bgr, spec, slot)
    res += g27_orientation(bgr, spec, slot)
    return res


def pairwise_angles(slots):
    """Reject the later slot if two slots IN THE SAME GROUP are within SEP_AZ AND
    SEP_EL. Studio (velvet) and lifestyle (worn) shots at a similar camera angle
    are different scenes, so separation applies within a group, not across."""
    viol = []
    for i in range(len(slots)):
        for j in range(i + 1, len(slots)):
            a, b = slots[i], slots[j]
            if a.get("group") != b.get("group"):
                continue
            daz = abs(a["azimuth"] - b["azimuth"]) % 360
            daz = min(daz, 360 - daz)
            dele = abs(a["elevation"] - b["elevation"])
            if daz < SEP_AZ and dele < SEP_EL:
                viol.append({"reject_slot": b["slot"], "vs": a["slot"], "d_azimuth": daz, "d_elevation": dele})
    return viol


def failed(res):
    return [r for r in res if r["status"] == "fail"]


def _fmt(slot, res):
    tag = {"pass": "OK", "fail": "FAIL", "skip": "--", "unmeasurable": "??"}
    parts = [f"{r['gate']}:{tag[r['status']]}" + (f"({r['measured']})" if r["measured"] is not None else "") for r in res]
    return f"slot {slot}: {'REJECT' if failed(res) else 'pass'} | " + " ".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sku")
    ap.add_argument("--image")
    ap.add_argument("--slot")
    ap.add_argument("--catalog")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    matrix = json.loads((ROOT / "config" / "angle_matrix.json").read_text(encoding="utf-8"))
    spec = json.loads((ROOT / "specs" / f"{args.sku}.json").read_text(encoding="utf-8"))
    slots = {s["slot"]: s for s in matrix["categories"][spec["category"]]["slots"]}

    if args.image and args.slot:
        res = validate_image(args.sku, args.image, slots[args.slot])
        print(json.dumps(res, indent=2) if args.json else _fmt(args.slot, res))
        sys.exit(1 if failed(res) else 0)

    if args.catalog:
        cdir = Path(args.catalog)
        allfail = 0
        for slot in slots.values():
            hits = sorted(cdir.glob(f"{slot['slot']}_*"))
            if not hits:
                print(f"slot {slot['slot']}: MISSING render"); allfail += 1; continue
            res = validate_image(args.sku, hits[0], slot)
            allfail += bool(failed(res))
            print(_fmt(slot["slot"], res))
        pv = pairwise_angles(list(slots.values()))
        print(f"G10 pairwise separation violations: {pv}" if pv else "G10 pairwise separation: all distinct")
        allfail += len(pv)
        sys.exit(1 if allfail else 0)

    ap.error("give --image+--slot or --catalog")


if __name__ == "__main__":
    main()
