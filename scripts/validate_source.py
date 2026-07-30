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
PHASH_MAX_DIST = 26  # loose: catches a grossly different second design only


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

    # ---- per-image checks ----
    hashes = []
    for p in imgs:
        bgr = cv.load_bgr(p)
        wm, det = cv.detect_watermark(bgr)
        if wm:
            return _fail("watermark", f"{p.name}: {det}")
        skin = cv.skin_fraction(bgr)
        if skin >= SKIN_MAX:
            return _fail("cad_only", f"{p.name}: skin fraction {skin:.1%} >= {SKIN_MAX:.0%} (worn/lifestyle photo, not CAD)")
        hashes.append((p.name, cv.focal_phash(bgr)))

    # ---- one design (coarse) ----
    maxd, pair = 0, None
    for i in range(len(hashes)):
        for j in range(i + 1, len(hashes)):
            d = hashes[i][1] - hashes[j][1]
            if d > maxd:
                maxd, pair = d, (hashes[i][0], hashes[j][0])
    if maxd > PHASH_MAX_DIST:
        return _fail("one_design",
                     f"focal pHash distance {maxd} > {PHASH_MAX_DIST} between {pair} (possible 2nd design)")

    return {"ok": True, "sku": sku, "category": cat, "views_present": len(imgs),
            "required": required, "max_focal_phash_dist": maxd}


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
              f"required {res['required']}, focal-hash dist {res['max_focal_phash_dist']}")
    sys.exit(0 if res["ok"] else 2)


if __name__ == "__main__":
    main()
