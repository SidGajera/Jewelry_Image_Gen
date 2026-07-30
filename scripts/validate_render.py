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


def _g(gate, status, measured=None, expected=None, detail=""):
    return {"gate": gate, "status": status, "measured": measured, "expected": expected, "detail": detail}


def g1_format(path):
    im = Image.open(path)
    w, h = im.size
    if not (w == 2048 and h == 2048):
        return _g("G1_FORMAT", "fail", f"{w}x{h}", "2048x2048", "non-square/size -> discard before all else")
    if im.format != "PNG":
        return _g("G1_FORMAT", "fail", im.format, "PNG", "not PNG")
    return _g("G1_FORMAT", "pass", f"{w}x{h} {im.format}", "2048x2048 PNG")


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
    # (3) person area vs jewellery area -- gated on 2+ faces so an allowed solo
    # hand (hand = skin, always > jewellery) or a single soft-focus model is not
    # falsely failed; this rule targets a COUPLE/people dominating the frame.
    if len(faces) >= 2:
        person = int(cv.skin_mask(bgr).sum())
        jew = max(cv.jewellery_area(bgr), 1)
        if person > jew * 6:
            return [_g("G14_CONTENT", "fail", f"{len(faces)} faces, person {person} > 6x jewellery",
                       "<=6x", "couple/people are the subject")]
    return [_g("G14_CONTENT", "pass", f"faces={len(faces)}", "compliant")]


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
    res += g14_content(bgr, slot)
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
