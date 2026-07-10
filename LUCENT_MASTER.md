# LUCENT CARAT LAB — MASTER IMAGE-GENERATION INSTRUCTIONS (COMPLETE)

Single source of truth. Merged from all prior docs + every instruction through 2026-07-09.
Operate ONLY as **lucentcaratlab@gmail.com** (never houseoflunivae@gmail.com).

Google Doc copy: https://docs.google.com/document/d/1iaLoRk9NmWgg5_DZ_eYuZFAvKJ9OITLjjv6y4wjQAf0/edit

---

## 0. PROJECT + TOP RULE
Take a product's SOURCE images and generate **12 marketing photos per product**, keeping the jewelry **100% IDENTICAL** to the source. Output 2K, photorealistic, images only.

**TOP RULE:** Ring must be 100% identical to SOURCE — design, shape, band, every stone, prongs, side settings, gallery, setting. Change NOTHING (not even 0.00000000000000001%) without permission. Always VIEW the source ring before generating. **Use the CORRECT source file — ignore stray/mislabeled images** (lesson: LR-0167 had strays "Copy of 7/4" from another ring; correct was "Copy of 14(1)"). If source can't be verified, don't generate.

## 1. TOOLS / ENVIRONMENT
- Higgsfield MCP, model **nano_banana_2**. 2K = **2 credits/image** (1K same cost). 4K costs more but is the only way to get crisp facets on very tiny pavé.
- Flow: `media_import_url` (Drive `uc?id=<ID>&export=download`) → media_ids in `medias[]` role "image" (SOURCE first, then pose reference) → `generate_image` count=1.
- Balance/transactions available; local image edits cost **0 credits**.
- Google Drive MCP: READ/SEARCH/CREATE only — **cannot edit or delete** existing files.
- Some CDNs / docs.google.com / Higgsfield CloudFront outputs are network-blocked to download; `download_file_content` (source study) and `media_import_url` (server-side fetch) work.

## 2. GOOGLE DRIVE MAP
- Parent "Lucent": `17fxsv1hJXoDm0vRgDOAm_YfNgG1xnLKv`
- Source parent (SKU subfolders): `1mKqVAi2iv_35zs12jn91UYaeX2vKGdyy`
- Studio/Office references: `1A9UJJcnlVA1Tvohd6Wa8O57eenCb7sQ2`
- Home Lifestyle references: `1GFwd4SHSPuCoaQj2WHYJWb7nTsvFUPzi`
- Output: `1NGoqWNTGX4SxPNyQkL_6ZU1jnuqpB5_2`
- Tracking sheet: `1Sburxb4cOdD52EnXWuNAX7Z3UF5-d_1RRWhP7-YHCM8`
- Auto log sheet: `1p2Qs5cs3D9NqjPnGp7EZvw9cPsIOBHK6it2aFXpXJ7k`

## 3. WHAT TO PRODUCE PER CATALOG (12 images)
- **5 STUDIO/OFFICE**: branded pure-white cloth + logo, 5 DIFFERENT angles (front top-down, macro close-up, side profile, cloth-held, three-quarter rest).
- **7 HOME-LIFESTYLE**: cozy US-home, one consistent theme, every shot different pose. Working split: **4 wider lifestyle + 3 macro close-ups**.
- Each image ONCE (count=1). **ALL images aspect 1:1 and 2K resolution — no exceptions, no quality compromise (updated 2026-07-10).**
- NEVER reuse a pose; vary pose references every catalog (natural, not templated).

## 4. JEWELRY FIDELITY (check before + after every image)
1. METAL: 18K NATURAL YELLOW GOLD — warm yellow. Never rose/white/silver/pale.
2. BAND width = source; keep THIN; never thicken.
3. BAND thickness UNIFORM all around (even hoop).
4. DIAMONDS uniform size = source (or exact graduated pattern).
5. RING TACK-SHARP every image incl. lifestyle; only background blurs.
6. EXACT stones: same number/shape/size/spacing/setting; no extra/center stone; row continuous & unbroken (every prong set).
7. BAND structure = source (twisted single-row; pavé single-row; half-eternity diamonds front, plain back).
8. NO extra metal under stones (open clean basket).
9. CENTER stone level/centered/square.
10. PRONGS/BASKET = source (count, shape, position).
11. SIDE/ACCENT settings = source exactly: halo (ROUND vs CUSHION — don't swap), three-stone, crescents, hidden halo.
12. PRESERVE every detail: halo rims, milgrain, beading, engraving, channel walls, gallery/trellis.
13. Edges/contours/silhouette clean at every angle.
14. Non-front angles scrutinised as hard as front.
15. Worn/bare-hand lifestyle = biggest drift point; scrutinise hardest.
16. HANDS: exactly five natural fingers, natural skin, neutral manicure.

## 5. DIAMOND RENDERING STANDARD (locked, updated 2026-07-08/09/10)
- **GOLD-STANDARD BENCHMARK (user-approved 2026-07-10) — RENDERING REFERENCE ONLY, NOT a design change:** LR-0156 studio shot on white cloth — center round brilliant with ONE clean facet pattern (crisp star/pinwheel radiating from a single table), natural mix of bright-white flashes + grey/black facet reflections, crystal clear, no doubling/ghosting/CGI symmetry; shoulder pavé = crisp individually faceted bead-set stones. **Apply this SAME diamond look to EVERY future catalog, consistently.** It governs how diamonds *render* — each ring still keeps its OWN source design/shape/count/size. All prior diamond + jewelry instructions remain unchanged; this only adds to them.
- EVERY diamond — center AND small halo/band pavé — looks like a REAL photographed brilliant-cut: sharp individually **visible facets** (star/pinwheel), as clear/faceted as the center just smaller; each small stone bead-set with crisp faceting. **No** glassy beads, flat white dots, plastic/opaque or blown-out stones.
- CONTRAST: natural mix of **bright white flashes AND dark grey/black facet reflections**. Colorless icy-white (top D), crystal-clear, spotless.
- LIGHT & SPARKLE **natural & realistic only**. No over-lighting, artificial light, exaggerated/over sparkle, CGI glow, starburst/lens flare, or rainbow fire. Real DSLR macro look.
- Governs rendering only — never shape/cut/count/size/scale.
- **CENTER STONE FACET PATTERN = SOURCE EXACTLY (added 2026-07-10).** Reproduce the source diamond's real round-brilliant facet layout (one table, star/kite/pavilion facets in their true positions). NO "duplicate/doubled/mirrored" diamond artifact — no second ghost facet pattern overlaid, no CGI kaleidoscope symmetry. Must read as ONE real photographed stone identical to the source, not an AI-invented facet mesh. Watch every worn/lifestyle angle where the center is largest — this is where the doubling appears.

## 6. STUDIO CLOTH + LOGO

### 6.0 BRAND LOGO PRESERVATION — ABSOLUTE PRIORITY (user-locked 2026-07-10, higher than EVERY other rule)
The official Lucent Carat Lab logo is a protected brand asset. It must NEVER be regenerated, redrawn, interpreted, enhanced, vectorized, recreated, OCR'd, or "fixed" by AI. Treat it as a LOCKED LAYER — pixel-identical to the uploaded original (`assets/logo/logo_official.png`).
- Preserve without ANY change: diamond-icon geometry, gold gradients, all typography (font family/weight, letter+line spacing, kerning, alignment), decorative lines, star symbols, the words LUCENT / CARAT / LAB / FUTURE OF FINE JEWELRY, colors, metallic finish, proportions.
- NEVER: rewrite text, replace fonts, generate similar letters, correct spelling, improve/simplify/stylize, hallucinate missing parts, or make a new version.
- The generative model CANNOT reproduce the logo (garbles it into fake logos e.g. "ELLYREID"). Therefore the logo is **NEVER rendered by nano_banana** — it is composited from the locked asset AFTER generation.

### 6.0a BACKGROUND LOGO POLICY — logo is a PRINTED-ON-CLOTH element, NOT removed, NOT a floating overlay (user-locked 2026-07-10)
The logo must ALWAYS appear on the studio cloth and must look **physically printed onto the fabric** (like a professionally printed jewelry pouch), never a watermark / sticker / floating overlay.
- Workflow: generate the ring on the locked clean white cloth WITHOUT a legible logo, then **composite the official logo onto the cloth locally so it looks printed** (0 credits, logo pixels identical). See `scripts/print_logo_on_cloth.py` and `docs/04_LOGO_WORKFLOW.md`.
- The printed logo follows the cloth's perspective, folds, surface deformation, lighting, shadows and highlights; fabric texture stays visible THROUGH the print (multiply-style blend), not a flat opaque patch.
- Realistic partial visibility is REQUIRED, not a defect: fine if slightly cropped by the frame, partly hidden behind the jewelry, or interrupted by a fold — ~60–90% visible.
- NEVER center the logo perfectly — natural off-center branding position (typically lower / lower-right). Jewelry may overlap it naturally.
- Colors: emblem + "LUCENT CARAT LAB" = GOLD; tagline "FUTURE OF FINE JEWELRY" = BLACK/dark. Use the locked asset's own pixels; never recolor.

### 6.1 MASTER BACKGROUND STANDARD — LOCKED CLOTH (user-locked 2026-07-10; full text in docs/11_BACKGROUND_STANDARD.md)
Every catalog image must look shot on the SAME cloth, studio, lighting, camera, white balance, printed logo.
- MATERIAL: exactly the reference pouch cloth (soft matte cotton-like, fine grain). LOCKED — never silk/satin/linen/generic-cotton/velvet/marble/paper/leather/visible-weave/other.
- COLOR: pure premium / neutral / bright luxury white always. NEVER cream/ivory/beige/yellow/warm-white/off-white/gray/blue/pink or any tint. No warm lighting on cloth. If a render drifts warm → fix with `whiten_cloth.py` locally (0 credits), never regenerate for color.
- APPEARANCE: same texture, softness, grain, fold style, wrinkle character, premium look; folds naturally draped, not random.

## 7. HOME-LIFESTYLE THEME
Cozy US-home; warm/natural/humane; consistent theme, different angle each; ring is the sharp hero, background may blur.

## 8. SOURCE PREP / FILES / NAMING
- Study ALL source images (any count) to understand piece in 3D.
- Remove watermark/hallmark/stray mark WITHOUT changing design — LOCALLY (PIL), 0 credits; cap ~2 attempts; if a mark on a fabric fold can't go fully clean, say so (perfect fix needs paid regen).
- Save to Output/`<ShortName>`; name `JewelryName_PoseAngle`; move source in.

## 9. RECORD KEEPING (one log sheet)
Log each success: #, Date, Product URL, Prompt, Source, Reference, Model, Size, Output file, Output folder link, Status, Notes. Append new learnings here (dated).

## 10. EFFICIENCY / COMMUNICATION
- NEVER use preview tools (no `show_generations`/`job_display`). User reviews in Higgsfield. (The generate result widget is unavoidable but free.)
- Short compact prompts (API echoes prompt back = main token cost). Few source views. Report count only; brief replies; permission once.
- Budget: 2 credits/image; target **~3–5k tokens per 12-image catalog**.

### 10a. TOKEN OPTIMIZATION RULES (HIGHEST PRIORITY, user-locked 2026-07-10)
Objective: minimize input+output tokens while producing IDENTICAL image quality & composition.
1. **Reuse all cached assets** — imported media_ids, preset_ids, pose_ids, source_ids. Never re-import/re-analyze unless the asset changed.
2. **Never repeat catalogs/images** — if a catalog/source/output was already processed, skip it. Detect dupes by file ID / media ID / hash / catalog ID.
3. **Never repeat prompts** — store reusable instructions as presets; send only the minimum params per generation.
4. **Never repeat URLs, schemas, metadata, or prior responses** — return only essential IDs + results.
5. **Never search/scan storage** if the asset already exists in cache.
6. **Batch operations** to avoid repeated tool calls.
7. **Cache intelligently** — cache only reusable resources (imports, presets, poses, verified sources); do NOT re-cache existing generated images; reuse cached refs.
8. **Output quality is #1** — optimization must NEVER reduce quality or change design/lighting/realism/materials/angle/composition. Result must be visually identical to the un-optimized output.
9. **If an optimization could change output in ANY way, do NOT apply it.** Preserve exact design, gem arrangement, proportions, metal finish, textures, reflections, realism.
10. **Before generating, check if an identical generation already exists** — if so reuse its generation ID; only generate when the requested output differs.
Goal: minimize tokens, avoid all duplicate work, maximize cache reuse, preserve 100% quality/consistency.

**CACHED ASSETS — LR-0156 (reuse, do NOT re-import):** source=`2d492e56-d640-468e-ac7a-6550de6e5cd6`; lifestyle L1=`a057c33d-59d9-49ca-8de5-85e66904500c` L2=`f717b869-4940-4de6-80e8-bf1547f32281` L3=`6178711f-220a-4c3a-84c3-dccd04c5dd2e` L4=`6545eae3-8181-4fea-8c65-e0b44ec24dfd`; closeups C1=`e9aa5f08-fa5c-4b1c-a503-a14601c2107b` C2=`8fabfc96-9b56-4a4a-a950-df6a13ea81e3` C3=`fe9f98cb-a13d-45af-a7e1-f2ff3e6f4fbd`. (media_ids may expire across sessions — only re-import if a call rejects them.)

## 11. LEAN WORKFLOW
1) 1 Drive search → 2) study ring (1–2 views), verify SKU → 3) 1–2 media_import_url → 4) fire 12 generate calls, compact prompts → 5) report count only. No polling/previews/base64.

## 12. COMPACT PROMPT TEMPLATES (prepend a short ANGLE tag)

**CANONICAL BASE PROMPT (user-locked 2026-07-10) — use verbatim as the core of every shot:**
> Preserve the exact ring design, stone shape, stone count, setting, prongs, band proportions and metal details from the source image.
> Use realistic VVS-quality lab-grown diamonds, accurate refraction, natural faceting, premium polished metal, luxury jewellery photography, sharp focus, clean background and commercial product-image quality.
> Do not redesign, simplify, add stones, remove stones, alter proportions, change the setting or modify the band.

Per shot, prepend the ANGLE/scene tag + (studio) "keep pure-white cloth + real printed logo unchanged, wordmark GOLD tagline BLACK" or (lifestyle/closeup) "cozy warm US-home, natural hand five fingers, no laptop/desk". Keep the §5 no-doubled-diamond clause. Everything 1:1, 2K.

---
Older templates (superseded by the canonical base above, kept for reference):
**STUDIO:** "[ANGLE]. Base = office reference image: keep pure-white cloth + printed logo EXACTLY, unchanged. Replace ONLY the ring with the SOURCE ring — design 100% identical (prongs, side settings/halo, band diamonds, gallery, all detail), 18K natural yellow gold. Every diamond incl. small pavé = real crisp visible facets, natural bright+dark reflections, no glassy dots, natural realistic light, no CGI/over-sparkle. Logo emblem+wordmark GOLD, tagline BLACK. Band thin/uniform; row continuous, every prong set. Ring tack-sharp. Photorealistic 2K."

**LIFESTYLE:** "[ANGLE]. Cozy warm US-home scene from reference; natural hand, five fingers, natural skin, wearing the SOURCE ring — design 100% identical, 18K natural yellow gold. Every diamond incl. small pavé = real crisp facets, natural bright+dark reflections, no glassy dots, natural realistic light, no CGI. Band thin/uniform; ring tack-sharp, only background blurs. Photorealistic 2K."

**ANGLE tags** — Studio: Front top-down / Macro close-up / Side profile / Held on cloth fold / Three-quarter rest. Lifestyle: Back of hand / On cozy knit / On marble / Side of finger / Held in fingertips / Raised near face / Close-up on ring finger.

## 13. REUSABLE POSE media_ids (re-import if expired)
Older studio set: front=`571574b8-...` closeup=`851a4134-...` side=`48504424-...` cloth-held=`b28febad-...` 3/4-rest=`b17f5283-...`. (media_ids expire across sessions — re-import from Drive reference folders.)

## 14. PRODUCT CODES / DESIGN NOTES
- LR-0190 Charlie (V-contour band) · LR-0191 Edie (marquise E-W, V-prong) · LR-0192 Julia (split-prong band)
- LR-0160 round solitaire, 4-prong plain band
- LR-0162 round center, CUSHION pavé halo, pavé band
- LR-0164 round solitaire, plain band, curved pavé crescent side accents
- LR-0165 round solitaire, cathedral open gallery, plain band
- LR-0166 round solitaire, single bead-set diamond row on shoulders
- LR-0167 round center, ROUND pavé halo, pavé band (source = "Copy of 14(1)", NOT stray "Copy of 7/4")
- LR-0168 THREE-STONE: round center + 2 round sides, plain band
- LR-0136 (BE1LCEM1110) THREE-STONE: OVAL diamond center (double-claw prongs) + 2 emerald-cut GREEN EMERALD sides (keep GREEN, not diamonds) + plain thin tapering yellow-gold band, open cathedral gallery. 3ct oval.
- LR-0137 (BE1D2289) THREE-STONE: OVAL diamond center (double-claw prongs) + 2 tapered BAGUETTE side diamonds (colorless, horizontal) + plain thin tapering yellow-gold band. 3ct oval. Studio shots generated logo-free on clean cloth; stamp official logo locally.

## PROGRESS
Done: LR-0160, LR-0162, LR-0164, LR-0165, LR-0166, LR-0167, LR-0168, LR-0156, LR-0136, LR-0137. Next: (add next SKU).

## MISTAKE LEARNINGS (2026-07-10) — never repeat
1. **Doubled/duplicate center diamond**: worn/lifestyle shot rendered a mirrored ghost facet mesh. Fix: reproduce source's single real brilliant-cut facet pattern (see §5 benchmark); scrutinise the largest worn angles.
2. **Invented logo on closeup**: model embossed a fake monogram on the cloth. Fix: closeups use the REAL preserved logo (rebase on branded studio reference; never AI-draw a logo) — §6.
3. **Wrong lifestyle theme (laptop/desk)**: picked a corporate desk reference instead of cozy home. Fix: lifestyle refs must be cozy warm US-home (knit/marble/window light) — NO desks/laptops/offices; confirm references before generating — §7.
4. **Wrong model/resolution coercion**: generate_image needs `params.model="nano_banana_2"` AND explicit `params.resolution="2k"` (default is 1k). Always set resolution.
5. **Don't burn credits on trial-and-error**: confirm correct source file + references with user BEFORE generating; fix input problems first.

## CHANGE LOG
- 2026-07-09: full re-merge; added natural-light/no-over-sparkle, small-pavé crisp facets, bright+dark contrast, use-correct-source, local mark-removal + cloth-whitening (0 credits), 4K note, per-SKU notes.
- 2026-07-06: lean workflow, compact prompts, logo colors, budget.
- 2026-07-03: uniform band/diamond, tack-sharp, thin band, logo full/uncut, white cloth, dynamic source count, diamond standard.

---

## CHAT TRANSFER — paste into a new chat
> Continuing Lucent Carat Lab image generation. Read the master spec (Google Doc link above / this file) and follow every rule. Account: lucentcaratlab@gmail.com. Tool: Higgsfield nano_banana_2, 2K, 2 credits/image. Source SKU parent `1mKqVAi2iv_35zs12jn91UYaeX2vKGdyy`; studio refs `1A9UJJcnlVA1Tvohd6Wa8O57eenCb7sQ2`; lifestyle refs `1GFwd4SHSPuCoaQj2WHYJWb7nTsvFUPzi`. 12 images = 5 office + 4 lifestyle + 3 close-ups. Hard rules: ring 100% identical to source (correct file, ignore strays); every diamond incl. small pavé = real sharp facets + bright/dark reflections, no glassy dots; natural light, no over-sparkle; 18K natural yellow gold; pure-white cloth + logo untouched (wordmark GOLD, tagline BLACK). No preview tools; short prompts. Done: LR-0160/0162/0164/0165/0166/0167/0168. Next SKU: ___. Re-import source + pose refs from Drive (media_ids expire). Confirm you've read it, then wait for the next SKU.
