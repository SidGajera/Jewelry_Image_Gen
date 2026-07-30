#!/usr/bin/env python3
"""SOURCE INTAKE GATE (blocking) — category-agnostic.

Refuse to start a catalog unless, for the SKU's category:
  - the required source views are present (config/view_requirements.json)
  - zero watermark / vendor overlay on any view
  - all views are the SAME design (coarse focal pHash agreement)
  - every view is a CAD render, not a worn/lifestyle photo (skin < 5%)
  - exactly ONE design in the set

Exit non-zero naming the failed item. Never fall through to generation.

Usage:
    python scripts/validate_source.py LR-0203 [--source-dir DIR] [--json]

View-type coverage: if specs/<SKU>_views.json exists it maps
{view_name: filename} and each required view is checked by name; otherwise the
gate requires at least len(required) distinct source images and reports the
view names as asserted-by-count (still blocks when too few images exist).
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import _cv_lib as cv  # noqa: E402

IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
SKIN_MAX = 0.05
HUE_MAX_UNITS = 4  # OpenCV hue units; 1 unit = 2 deg, so 4 = 8 deg (spec)


def _fail(item, detail):
    print(f"SOURCE GATE FAIL [{item}]: {detail}")
    return {"ok": False, "item": item, "detail": detail}


def validate(sku, source_dir=None):
    spec_p = ROOT / "specs" / f"{sku}.json"
    if not spec_p.exists():
        return _fail("spec", f"specs/{sku}.json not found")
    spec = json.loads(spec_p.read_text(encoding="utf-8"))
    cat = spec.get("category")
    reqs = json.loads((ROOT / "config" / "view_requirements.json").read_text(encoding="utf-8"))
    if cat not in reqs:
        return _fail("category", f"no view_requirements for category '{cat}'")
    required = reqs[cat]

    sdir = Path(source_dir) if source_dir else ROOT / "workspace" / "golden" / sku / "source"
    if not sdir.exists():
        return _fail("source_dir", f"{sdir} does not exist")
    imgs = sorted(p for p in sdir.iterdir() if p.suffix.lower() in IMG_EXT)
    if not imgs:
        return _fail("views", f"no source images in {sdir}")

    # ---- view coverage ----
    vmap_p = ROOT / "specs" / f"{sku}_views.json"
    if vmap_p.exists():
        vmap = json.loads(vmap_p.read_text(encoding="utf-8"))
        missing = [v for v in required if v not in vmap or not (sdir / vmap[v]).exists()]
        if missing:
            return _fail("views", f"missing required {cat} views: {missing}")
    else:
        if len(imgs) < len(required):
            return _fail("views",
                         f"{cat} needs {len(required)} views {required}; only {len(imgs)} image(s) present")

    # ---- per-image checks + angle-invariant identity signals ----
    sig = []  # (name, metal_hue, stone_count, accent_present)
    for p in imgs:
        bgr = cv.load_bgr(p)
        wm, det = cv.detect_watermark(bgr)
        if wm:
            return _fail("watermark", f"{p.name}: {det}")
        skin = cv.skin_fraction(bgr)
        if skin >= SKIN_MAX:
            return _fail("cad_only", f"{p.name}: skin fraction {skin:.1%} >= {SKIN_MAX:.0%} (worn/lifestyle photo, not CAD)")
        sig.append((p.name, cv.metal_hue_peak(bgr), cv.primary_stone_count(bgr), cv.accent_present(bgr)))

    # ONE design via angle-invariant signals (pHash removed — it cannot separate
    # angle-diverse views of one design from two designs at one angle).
    # (1) dominant metal hue within 8 deg (handles hue wrap; None = white metal bucket)
    hues = [(nm, h) for nm, h, _, _ in sig]
    whites = [nm for nm, h in hues if h is None]
    golds = [(nm, h) for nm, h in hues if h is not None]
    if whites and golds:
        return _fail("one_design", f"metal mismatch: white-metal {whites} vs coloured-metal views (two designs?)")
    if golds:
        hv = [h for _, h in golds]
        span = max(hv) - min(hv)
        span = min(span, 180 - span)  # hue wrap
        if span > HUE_MAX_UNITS:
            return _fail("one_design", f"metal hue span {span*2} deg > 8 deg across views (two designs?)")
    # (2) primary stone count: consensus across measurable views. Exact count can
    # flicker by one on an edge-on view of an elongated stone, so require a strict
    # MAJORITY to agree; no consensus => genuinely mixed designs => STOP.
    counts = [c for _, _, c, _ in sig if c is not None]
    if counts:
        from collections import Counter
        mode, hits = Counter(counts).most_common(1)[0]
        if hits * 2 <= len(counts):
            return _fail("one_design", f"no primary-stone-count consensus across views {sorted(counts)} (mixed designs?)")
    # (3) accent-run present/absent identical across measurable views
    accents = {a for _, _, _, a in sig if a is not None}
    if len(accents) > 1:
        return _fail("one_design", "accent-run present in some views, absent in others (two designs?)")

    return {"ok": True, "sku": sku, "category": cat, "views_present": len(imgs), "required": required}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sku")
    ap.add_argument("--source-dir")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    res = validate(args.sku, args.source_dir)
    if args.json:
        print(json.dumps(res, indent=2))
    elif res["ok"]:
        print(f"SOURCE GATE PASS: {args.sku} ({res['category']}) — {res['views_present']} views, "
              f"required {res['required']}")
    sys.exit(0 if res["ok"] else 2)


if __name__ == "__main__":
    main()
