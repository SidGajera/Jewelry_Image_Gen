#!/usr/bin/env python3
"""Generate all slot prompts for a catalog from its machine-readable spec
(specs/<SKU>.json, category-agnostic schema) + the locked per-category angle
matrix (config/angle_matrix.json).

NO hand-written geometry text lives anywhere else. The spec JSON is the single
source of truth, so geometry cannot drift between slots or SKUs. Every prompt is
a pure function of (spec, slot). Fields that are null for a category are simply
omitted from the prompt (and their gates auto-skip). See docs/13 §6c, docs/22.

Usage:
    python scripts/build_prompts.py LR-0203 [-o out.json]
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# NOTE: the Higgsfield generation call is FROZEN (docs/22) — plain text-to-image,
# medias [pose/studio ref, SOURCE piece], no img2img / no denoise / no compositing.
# All enforcement is OUTSIDE the call (gates + retry). This builder only produces
# the spec-driven prompt text + negatives; it sets no generation params.

NEGATIVE = (
    "round brilliant primary stone, near-round primary, low length-to-width ratio, "
    "broad setting elements, split claws, double claws, flared prongs, fluted prong, extra prong, "
    "hidden halo, halo, accent stones under primary stone, basket pave, peekaboo diamonds, "
    "extra accent row, oversized accent stones, widely spaced accents, sparse accents, short accent run, "
    "channel set accents, raised rail, metal edge below accents, thick bead setting, accents stopping short, "
    "tapered structure, wider structure, flat structure, added filigree, "
    "second piece, extra piece, duplicate jewelry, ghost clasp, doubled link run, "
    "watermark, text, vendor mark, logo overlay, portrait format, landscape format, non-square crop, "
    "yellow gold, rose gold, rotated piece, asymmetric structure"
)


def _stone_phrase(s):
    bits = [f"{s.get('count', 1)}x {s['shape']} {s.get('cut', '')}".strip() + f" primary stone(s) id '{s['id']}'"]
    if s.get("orientation"):
        bits.append(f"oriented {s['orientation'].replace('_', '-')}")
    if s.get("lw_ratio"):
        bits.append(f"length-to-width ratio {s['lw_ratio']}:1 (must read at this ratio, not round/near-round)")
    if s.get("scale_ratio_to_structure"):
        bits.append(f"primary width about {s['scale_ratio_to_structure']}x the structure width -- do NOT enlarge it")
    return ", ".join(bits) + "."


def _setting_phrase(se):
    if not se or se.get("count") in (None, 0):
        return ""
    return (f"Exactly {se['count']} {se.get('form', '').replace('_', ' ')} {se['type']} setting elements, "
            f"{se.get('layout', '')}-set, thin, single. NO broad, split, double or flared elements, "
            f"no extra element.")


def _accent_phrase(runs, structure):
    if not runs:
        return "No accent stones anywhere."
    r = runs[0]  # runs share geometry; state once, note it applies to each
    ids = ", ".join(x["id"] for x in runs)
    return (f"Accent runs [{ids}]: each is {r['rows']} row, exactly {r['count']} MICRO stones "
            f"(each diameter about {r.get('stone_dia_ratio_to_structure', 0.1):.2f}x the structure width), "
            f"tightly packed, near-touching, uniform. Setting {r.get('setting', '').replace('_', ' ')} "
            f"-- flush, level with the surface, NO raised rail, NO channel, NO metal edge below the stones. "
            f"Coverage spans the front {int(r.get('coverage_fraction', 0.66) * 100)}% of the structure, "
            f"not stopping short.")


def _halo_phrase(spec):
    if spec.get("halo", "none") == "none":
        uh = spec.get("under_head", "plain")
        return f"NO halo of any kind, NO hidden halo, NO stones under the primary, plain polished {uh} under-head."
    return f"Halo: {spec['halo']}. Under-head: {spec.get('under_head')}."


def _structure_phrase(st):
    if not st:
        return ""
    bits = [f"Structure: {st.get('profile', '').replace('_', ' ')} profile"]
    if st.get("uniform_width"):
        bits.append("uniform width")
    bits.append("NO taper" if not st.get("taper") else "tapered")
    if st.get("link_count"):
        bits.append(f"{st['link_count']} {st.get('link_form', '')} links")
    return ", ".join(b for b in bits if b) + ", NO widening."


def build_prompt(spec, slot):
    grp = slot["group"]
    scene = spec["scene"][grp]
    geom = " ".join(p for p in [
        " ".join(_stone_phrase(s) for s in spec.get("primary_stones", [])),
        _setting_phrase(spec.get("setting_elements")),
        _halo_phrase(spec),
        _accent_phrase(spec.get("accent_runs", []), spec.get("structure", {})),
        _structure_phrase(spec.get("structure")),
        f"Metal: {spec.get('metal', '').replace('_', ' ')} {spec.get('finish', '').replace('_', ' ')}. "
        f"No yellow, no rose, no two-tone.",
    ] if p)
    cam = (f"CAMERA (numeric, obey exactly): {slot['name']} -- elevation {slot['elevation']} degrees "
           f"above the lay plane, azimuth {slot['azimuth']} degrees. Piece fills ~{int(slot['crop']*100)}% of frame.")
    prompt = (
        "GEOMETRY LOCK -- the SOURCE piece reference is the master CAD object; reproduce it with 100% fidelity. "
        "Do NOT redesign, beautify, add or remove anything. Same physical piece; only camera and scene change.\n\n"
        f"{cam}\n\n"
        f"PIECE ({spec['sku']}, category {spec['category']}, match structural reference exactly):\n{geom}\n\n"
        f"SCENE: {scene}. Realistic macro luxury jewellery product photography, tack-sharp on the piece, "
        f"shallow depth of field, sRGB, no watermark, no text. Format 1:1 square, 2048x2048.\n\n"
        f"NEGATIVE: {NEGATIVE}"
    )
    return {
        "slot": slot["slot"], "name": slot["name"], "group": grp,
        "azimuth": slot["azimuth"], "elevation": slot["elevation"], "crop": slot["crop"],
        "aspect_ratio": "1:1", "resolution": spec.get("resolution", "2k"),
        "model": spec.get("model", "seedream_v5_pro"),
        "prompt": prompt, "negative": NEGATIVE,
    }


def load_spec(sku):
    p = ROOT / "specs" / f"{sku}.json"
    if not p.exists():
        sys.exit(f"FAIL: spec not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def build_all(sku):
    spec = load_spec(sku)
    matrix = json.loads((ROOT / "config" / "angle_matrix.json").read_text(encoding="utf-8"))
    cat = spec["category"]
    if cat not in matrix["categories"]:
        sys.exit(f"FAIL: no angle matrix for category '{cat}'")
    return spec, [build_prompt(spec, slot) for slot in matrix["categories"][cat]["slots"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sku")
    ap.add_argument("-o", "--out")
    args = ap.parse_args()
    _, prompts = build_all(args.sku)
    out = json.dumps(prompts, indent=2)
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"wrote {len(prompts)} prompts -> {args.out}")
    else:
        print(out)


if __name__ == "__main__":
    main()
