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

def build_negative(spec):
    """Emit the negative list FROM the spec so we never negate the real geometry
    (e.g. LR-0206's double claws / scattered clusters are the design, not defects)."""
    negs = ["duplicate jewelry, second piece, extra piece, ghost clasp, doubled link run",
            "watermark, text, vendor mark, logo overlay",
            "portrait format, landscape format, non-square crop, rotated piece, asymmetric structure",
            # inner-shank clean-metal lock (all catalogs)
            "engraved mark on the band, maker's mark, hallmark, stamp on the inner shank, "
            "initials engraved in metal, karat stamp, serial number, logo cut into metal, "
            "engraving on the shank interior, etched glyph, chisel mark"]
    # metal colour: forbid the colours the spec is NOT
    metal = spec.get("metal", "")
    if "yellow" not in metal:
        negs.append("yellow gold")
    if "rose" not in metal:
        negs.append("rose gold")
    # primary shape drift
    for s in spec.get("primary_stones", []):
        if s.get("lw_ratio", 1) >= 1.25:
            negs.append("round primary stone, near-round primary, low length-to-width ratio")
    # setting form: only forbid split/double/broad when the design is plain single
    form = (spec.get("setting_elements") or {}).get("form", "")
    if form == "plain_slender":
        negs.append("broad setting elements, split claws, double claws, flared prongs, fluted prong, extra prong")
    else:
        negs.append("extra prong, wrong prong count")
    # halo / under-head
    if spec.get("halo", "none") == "none":
        negs.append("hidden halo, halo, accent stones under primary stone, basket pave, peekaboo diamonds")
    elif spec.get("halo") == "hidden":
        negs.append("visible surface halo, halo on top of the crown, halo ring around the stone seen from above, double halo, cluster halo, accents on the top face")
    # accent runs: forbid spacing/size drift only where the run is a uniform micro row
    runs = spec.get("accent_runs") or []
    if runs:
        arrangement = runs[0].get("arrangement", "uniform_row")
        negs.append("extra accent row, oversized accent stones, short accent run")
        if arrangement == "vine_scroll_shoulder":
            # symmetric scroll/vine shoulders with a few small round accents (the scrollwork IS the design)
            negs.append("pave shoulders, packed pave row, channel set accents, halo, extra accent stones, "
                        "baguette accents, plain shoulders with no scrollwork, missing vine scroll, "
                        "asymmetric shoulders, oversized side stones, three stone ring")
        elif arrangement == "bar_set_baguette":
            # bar-set east-west baguette band: the gold bars/spacing ARE the design
            negs.append("round accents, princess-cut accents, tapered baguettes, pave band, "
                        "channel set, bezel set row, prong-set stones, center solitaire stone, "
                        "large centre gemstone, halo, second row of stones, full eternity band, "
                        "stones on the lower shank, stones wrapping fully around the band, "
                        "few large baguettes, oversized baguettes, chunky baguettes, only 5 or 6 stones, "
                        "wide gaps between stones, thick gold bars, sparse row")
        elif arrangement != "scattered_cluster_mixed_size":
            negs.append("widely spaced accents, sparse accents")
        settings = {r.get("setting", "") for r in runs}
        if any(str(s).startswith("flush") for s in settings):
            negs.append("channel set accents, raised rail, metal edge below accents, thick bead setting, accents stopping short")
    else:
        # plain unaccented band: forbid any shoulder/shank stones
        negs.append("pave band, accented band, stones on the shank, side stones on the band, shoulder accents, three stone ring")
    # structure
    st = spec.get("structure") or {}
    if not st.get("taper"):
        negs.append("tapered structure")
    if st.get("uniform_width"):
        negs.append("wider structure, flat structure")
    return ", ".join(negs)

# Positive inner-shank clause appended to every prompt's PIECE section.
INNER_SHANK = ("INNER SHANK: plain polished metal, smooth, unmarked, uninterrupted "
               "(no engraving, hallmark, stamp or maker's mark).")


def _stone_phrase(s):
    bits = [f"{s.get('count', 1)}x {s['shape']} {s.get('cut', '')}".strip() + f" primary stone(s) id '{s['id']}'"]
    if s.get("orientation"):
        bits.append(f"oriented {s['orientation'].replace('_', '-')}")
    if s.get("lw_ratio"):
        if s["lw_ratio"] >= 1.25:
            bits.append(f"length-to-width ratio {s['lw_ratio']}:1 (must read elongated at this ratio, not round/near-round)")
        else:
            bits.append("round outline, a true circle (equal length and width, 1:1)")
    if s.get("scale_ratio_to_structure"):
        bits.append(f"primary width about {s['scale_ratio_to_structure']}x the structure width -- do NOT enlarge it")
    return ", ".join(bits) + "."


def _setting_phrase(se):
    if not se or se.get("count") in (None, 0):
        return ""
    form = se.get("form", "")
    layout = se.get("layout", "").replace("_", " ")
    if form == "plain_slender":
        return (f"Exactly {se['count']} plain slender {se['type']} setting elements, {layout}-set, "
                f"thin and single -- NO broad, split, double or flared elements, no extra element.")
    # non-plain forms (double/split) are the intended design; state them, do not forbid them
    return (f"Exactly {se['count']} {form.replace('_', ' ')} {se['type']} setting elements, {layout} "
            f"(the {form.replace('_',' ')} form is intentional and must be preserved); no extra or missing element.")


def _accent_phrase(runs, spec):
    if not runs:
        return "No accents on the shoulders; the band is plain and unaccented (any accents are the hidden halo only)."
    r = runs[0]
    ids = ", ".join(x["id"] for x in runs)
    cov = int(r.get("coverage_fraction", 0.66) * 100)
    if r.get("arrangement") == "bar_set_baguette":
        metal = spec.get("metal", "yellow_gold").replace("_", " ")
        return (f"Accent run [{ids}]: a single straight HALF-ETERNITY row of {r['count']} SMALL step-cut "
                f"BAGUETTE diamonds (small elongated rectangles, straight clean step-cut edges, NOT round, NOT "
                f"tapered), set EAST-WEST -- each baguette's long axis lying across the band, packed CLOSE-SET "
                f"edge-to-edge in one continuous line along the TOP of the shank. The stones are SMALL and MANY: "
                f"each baguette is only slightly longer than the band is wide, and there are about {r['count']} of "
                f"them filling the front -- do NOT enlarge the baguettes and do NOT reduce their number (a few big "
                f"baguettes is WRONG). BAR-SET: a thin polished {metal} bar between every adjacent pair of baguettes "
                f"and one bar at each end (shared vertical bars only -- NOT channel walls, NOT prongs, NOT bezel, "
                f"NOT flush pave). All baguettes identical small size, level, evenly and tightly spaced. The row "
                f"spans about {cov}% of the band (front/top only); the rest of the shank is plain polished {metal}. "
                f"Single row, no stones on the lower half, no centre stone, no halo.")
    if r.get("arrangement") == "vine_scroll_shoulder":
        metal = spec.get("metal", "yellow_gold").replace("_", " ")
        per = r["count"]
        return (f"SHOULDER ACCENTS [{ids}]: the band does NOT run plain into the head -- each of the TWO shoulders "
                f"is a small decorative {metal} SCROLL / VINE (an S-curl of polished gold) flanking the centre "
                f"stone, and each scroll holds exactly {per} tiny ROUND brilliant accent diamonds (total {2 * per} "
                f"accents, {per} per side, left and right MIRRORED). The accents are SMALL (each roughly one-fifth "
                f"the centre stone), bead/prong-set into the scrollwork, spaced apart within the curls -- NOT a "
                f"packed pave row, NOT channel, NOT a halo. Keep the vine scroll symmetric and delicate; do NOT add "
                f"extra accents, do NOT turn the shoulders into pave, do NOT omit the scrollwork.")
    if r.get("arrangement") == "scattered_cluster_mixed_size":
        return (f"Accent runs [{ids}]: each a SCATTERED CLUSTER of about {r['count']} round accents of "
                f"MIXED sizes, {r.get('setting', '').replace('_', ' ')}, trailing naturally along the shoulder "
                f"with irregular organic spacing (NOT a uniform row, NOT evenly spaced), spanning about {cov}% "
                f"of the shoulder. Preserve the mixed sizes and scattered layout exactly.")
    return (f"Accent runs [{ids}]: each is {r['rows']} row, exactly {r['count']} MICRO stones "
            f"(each diameter about {r.get('stone_dia_ratio_to_structure', 0.1):.2f}x the structure width), "
            f"tightly packed, near-touching, uniform. Setting {r.get('setting', '').replace('_', ' ')} "
            f"-- flush, level with the surface, NO raised rail, NO channel, NO metal edge below the stones. "
            f"Coverage spans the front {cov}% of the structure, not stopping short.")


def _halo_phrase(spec):
    halo = spec.get("halo", "none")
    if halo == "none":
        if not spec.get("primary_stones"):
            return ""   # band with no head/centre stone: no halo/under-head language at all
        uh = spec.get("under_head", "plain")
        return f"NO halo of any kind, NO hidden halo, NO stones under the primary, plain polished {uh} under-head."
    if halo == "hidden":
        n = spec.get("halo_count")
        cnt = f"about {n} " if n else ""
        return (f"HIDDEN HALO: a single row of {cnt}tiny round accents encircling the primary directly under "
                f"the girdle, set into the {spec.get('under_head', 'basket')} under-head, visible ONLY from the "
                f"side and rear -- NOT on the top face. From directly above, the piece reads as a clean solitaire "
                f"with no surface halo.")
    return f"Halo: {halo}. Under-head: {spec.get('under_head')}."


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


# Verbatim content-policy negative, appended to EVERY lifestyle slot (all catalogs).
LIFESTYLE_NEGATIVE = ("kissing, couple kissing, faces touching, embracing, intimate pose, "
                      "romantic contact, cheek to cheek, couple as the subject, people in focus, "
                      "suggestive posing")

# Realism / anti-AI, appended to EVERY lifestyle slot (all catalogs). Verbatim per user 2026-07-30.
REALISM_POSITIVE = ("Photographed on a full-frame camera, 85mm, f/2.0, natural available light. "
                    "Real human skin: visible pores, fine vellus hair, knuckle creases, tendon shadows "
                    "across the back of the hand, faint blue veins, subtle redness at the joints, uneven "
                    "skin tone. Natural nails with real cuticles and slight ridging. Hand anatomy correct: "
                    "five fingers, natural spacing, believable joint angles. Ring worn on the ring finger, "
                    "band fully encircling that single finger, seated between the knuckles. Unretouched "
                    "skin. Candid, imperfect, honest colour. This slot uses a DISTINCT model, wardrobe and "
                    "location from every other lifestyle slot (rotate skin tone and age within the theme).")
REALISM_NEGATIVE = ("plastic skin, waxy skin, poreless, airbrushed, smoothed skin, mannequin hand, "
                    "doll hand, rubber texture, uniform skin tone, glossy CGI highlight, HDR glow, "
                    "beauty filter, retouched, symmetrical hand, ring between two fingers, band crossing "
                    "the gap between fingers, ring at the webbing, fused fingers, extra fingers, malformed hand")


# Hand-anatomy lock, appended to EVERY lifestyle slot (G15). Verbatim per user 2026-07-30.
ANATOMY_POSITIVE = ("Ring worn on the ring finger, band fully encircling that single finger, seated "
                    "between the knuckles, both sides of the band on the same finger, anatomically "
                    "correct hand, five fingers, natural spacing.")
ANATOMY_NEGATIVE = ("ring between two fingers, ring spanning two fingers, band crossing the gap between "
                    "fingers, ring at the webbing, ring over a knuckle, floating ring, ring not "
                    "encircling a finger, fused fingers, extra fingers, six fingers, missing finger, "
                    "malformed hand")


def build_prompt(spec, slot, theme=None):
    grp = slot["group"]
    scene = slot.get("scene") or spec["scene"][grp]   # per-slot compliant scene wins
    neg = build_negative(spec)
    if grp == "lifestyle":
        if theme:
            # one theme per catalog (all 6 lifestyle slots share it); studio stays velvet
            scene = (f"THEME '{theme['id']}' -- ALL lifestyle slots in this catalog share this SET: "
                     f"location {theme['location']}; palette {theme['palette']}; light {theme['light']}; "
                     f"wardrobe {theme['wardrobe']}; mood {theme['mood']}. This theme location/palette/light "
                     f"REPLACES any other location; keep ONLY the hand pose and framing from: [{scene}]. "
                     f"Vary the model, skin tone, age, wardrobe piece and time-within-window per slot.")
        scene = scene + ". " + REALISM_POSITIVE   # includes anatomy + ring placement
        neg = neg + ", " + LIFESTYLE_NEGATIVE + ", " + REALISM_NEGATIVE   # includes skin + anatomy
    geom = " ".join(p for p in [
        " ".join(_stone_phrase(s) for s in spec.get("primary_stones", [])),
        _setting_phrase(spec.get("setting_elements")),
        _halo_phrase(spec),
        _accent_phrase(spec.get("accent_runs", []), spec),
        _structure_phrase(spec.get("structure")),
        f"Metal: {spec.get('metal', '').replace('_', ' ')} {spec.get('finish', '').replace('_', ' ')}, "
        f"single tone (no two-tone).",
        INNER_SHANK,
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
        f"NEGATIVE: {neg}"
    )
    return {
        "slot": slot["slot"], "name": slot["name"], "group": grp,
        "azimuth": slot["azimuth"], "elevation": slot["elevation"], "crop": slot["crop"],
        "aspect_ratio": "1:1", "resolution": spec.get("resolution", "2k"),
        "model": spec.get("model", "seedream_v5_pro"),
        "prompt": prompt, "negative": neg,
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
    theme = None
    try:
        import theme as _theme
        theme = _theme.assign(sku)
    except Exception:
        pass
    return spec, [build_prompt(spec, slot, theme) for slot in matrix["categories"][cat]["slots"]]


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
