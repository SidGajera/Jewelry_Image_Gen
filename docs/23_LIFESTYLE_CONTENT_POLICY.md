# 23 — LIFESTYLE CONTENT POLICY (PERMANENT, all catalogs, user-locked 2026-07-30)

**MOTO: jewellery photoshoot only. The ring is the subject in every frame. People are set dressing, never the story.**

## BANNED (remove from refs/lifestyle/ and from every prompt)
kissing, mouth-to-mouth or mouth-to-skin contact, faces close together, embracing, intimate holding, romantic physical contact, suggestive posing, any frame where the couple occupies more area than the jewellery. **The rooftop-kiss reference is REMOVED — do not use it or anything like it.** This SUPERSEDES the kiss/embrace poses in the old romantic-pose library.

## ALLOWED
hands only · solo hand or solo model · a partner present but clearly secondary, small in frame and softly out of focus · real environments (rooftop, skyline, string lights, beach, cafe, kitchen, window light) · natural candid framing.

## SLOTS (config/angle_matrix.json ring lifestyle scenes — compliant, same locations/light)
05 low_hero — rooftop dusk, hand raised, skyline bokeh, no people · 06 back_three_quarter — rooftop, hand extended to camera, city lights behind · 07 hand_top_down — hand on a railing, skyline below, hand only · 08 hand_45_worn — string lights, solo model, hand raised, face soft/partial · 09 hand_side_macro — beach sunset, hand in profile, macro, no second person · 10 hand_tilted_pov — POV own hand tilted to lens, warm bokeh. **Studio unchanged: 4 white-velvet slots. COUNTS EXACT: 4 studio + 6 lifestyle.**

## PROMPT NEGATIVE (verbatim, appended to EVERY lifestyle slot — build_prompts.LIFESTYLE_NEGATIVE)
`kissing, couple kissing, faces touching, embracing, intimate pose, romantic contact, cheek to cheek, couple as the subject, people in focus, suggestive posing`

## GATE G14 — content compliance (BLOCKING, lifestyle slots; scripts/validate_render.g14_content)
1. Face detection (YuNet). **Two faces within one face-width of each other = FAIL** (couple/kiss).
2. **Any face sharper than the ring region** (Laplacian variance) = FAIL (a person is the subject).
3. Combined person area > jewellery area × 6 = FAIL "couple is the subject" — **gated on 2+ faces** so an allowed solo hand (hand = skin, always exceeds jewellery area) or a single soft-focus model is not falsely failed; the rule targets people dominating the frame.
Any fail → auto-regenerate with the negatives re-appended. G14 is in run_catalog ENFORCED_GATES (blocks completion).
