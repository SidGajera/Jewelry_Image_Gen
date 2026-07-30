# 24 — DELIVERABLES PER CATALOG (LOCKED, all catalogs, user-locked 2026-07-30)

Single authority for counts, format, angles, theme, realism. Every rule maps to a code gate (bottom).

## Two flags — SET
- **FORMAT = 1:1 SQUARE, 2048×2048.** The old deliverables note said PORTRAIT; that conflicts with G1, the FORMAT GATE (`prompts/07`), and the LR-0203 failure entries, which all lock 1:1. Resolved to **1:1** — the value already used everywhere in code. Must stay consistent with `config/angle_matrix.json`, `scripts/build_prompts.py`, gates, and QUALITY_MEMORY.
- **GEOMETRY vs CAMERA — working reading.** Every GEOMETRY element must trace to a source view. CAMERA POSITION may be new: lifestyle slots have no CAD equivalent and are generated from the confirmed geometry model, not a matching CAD angle. (The strict "no angle without a source view" reading would block all six lifestyle slots permanently; not used.)

## P0 SOURCE (blocking)
Read the source CAD FIRST, review + confirm every view, build the full geometry model before any prompt. AI redraw of the jewellery is DISABLED — geometry from source pixels only, never memory or category priors. Unclear/conflicting views = STOP and ask.

## P1 FORMAT
1:1 square 2048×2048, native (no upscale), tack-sharp on the jewellery, sRGB, neutral WB, no watermark/text/border.

## P2 MOTIVE
Every image is jewellery photography — the ring is the subject and the sharpest element in frame, studio and lifestyle alike. People, partner and scene are supporting context in shallow DoF; they never outweigh the jewellery.

## P3 COUNTS (exact, never 5/5)
Studio EXACTLY 4 (premium white velvet only). Lifestyle EXACTLY 6 (worn on hand, real setting). One image per angle, one per pose, no repeats. Lifestyle includes close-up macros, each at a different macro angle.

## P4 ANGLE VARIATION
Distinct camera angle AND composition per slot (incl. macros). Camera stated as NUMBERS per slot (azimuth, elevation, crop); filenames carry no geometry. Rotate: top-down, 45° three-quarter, 3/4 side (not flat profile), low angle, back three-quarter, tilted, macro. **`medias[0]` carries a DISTINCT per-slot reference from `refs/`** — a shared reference produces ten near-identical views regardless of prompt text; `refs/` is a prerequisite and `--stage prompts` hard-fails if any of the ten is missing.

## P5 THEME
One coherent theme within a catalog (palette, styling, mood, lighting); a different theme per catalog, rotated by SKU hash, so catalogs never look alike.

## P6 REALISM / ANTI-AI
Genuine photography: real hands, skin texture, fabric, light. Varied non-generic models and wardrobe. BANNED: beige/cream/oatmeal ribbed or chunky-knit sweater; neutral couch. Ring true-to-source scale on the finger. Etsy-compliant (docs/23): no kissing, faces in contact, embrace, suggestive posing, or any frame where the couple outweighs the ring.

## P7 MARKS
Any watermark, hallmark or engraved maker's mark in the source is a source artifact, not jewellery — exclude it. Inner shank stays plain polished. Removal must be lossless: geometry, band profile, pavé and lighting unchanged.

## P8 JEWELLERY
All geometry per `docs/13` (JEWELLERY PRESERVATION) + the catalog SOURCE_SPEC. Only setting and camera angle change; nothing else.

## GATE MAP (enforced in code)
P1 → G1 · P3 → slot manifest · P4 → G10 + refs/ preflight · P6 → G9 scale, G14 content · P7 → G12 · P8 → G2–G9. A catalog is COMPLETE only when all 10 render, all gates pass, images are downloaded, and the push succeeds (`run_catalog.py --stage finish`).

**Build status (honest):** enforced today — G1, G10 (within-group), G14, slot-count manifest, G2–G9 (heuristic/advisory on real renders). Not yet built — refs/ per-slot distinct `medias[0]` + `--stage prompts` hard-fail (P4), G12 mark-removal (P7), G9 true-to-source scale as blocking (P6).
