# 04 — LOGO WORKFLOW (locked asset + printed-on-cloth compositing)

The single most important workflow in the project. Priority **P0** — overrides everything.

> **METHOD LOCK (user-locked 2026-07-21, LATEST — supersedes the earlier same-day in-model override): LOGO IS PRINTED BY THE LOCAL COMPOSITE `scripts/print_logo_on_cloth.py` FROM THE LOCKED PRESERVED ASSET — pixel-exact.** This is the approved method: it produces the clean textile-print look in the user's approved sample images. **In-model Higgsfield logo is NOT used** — it repeatedly produced oversized / duplicated / emblem-as-background-wireframe / flat-overlay logos across LR-0180/0181 (`config/QUALITY_MEMORY.json#lr0180-inmodel-logo-overlay-and-duplicate`). WORKFLOW: Higgsfield renders the ring on **CLEAN premium-white cloth (NO logo)**; then the composite prints the ONE exact logo (`assets/logo/logo_official_transparent.png`, derived from `assets/logo/logo_official.png`) into the cloth with the approved params `--scale 0.28-0.34 --pos lower-right/lower-centre --opacity 0.45-0.6 --displace 6-8 --soften 1.0 --grain 0.06`. The logo asset is a LOCKED preserved asset — reproduced pixel-identical, never recreated/redrawn/modified; tagline stays BLACK; jewelry the hero. ENVIRONMENT: the composite runs where the Higgsfield render is downloadable; a session whose egress policy blocks the Higgsfield CDN / Drive (e.g. this web sandbox, 403) generates the clean-cloth base only and hands off the composite step to the desktop/operator. This supersedes the "AI must NEVER render the logo" wording only in that the composite (not AI) draws it — everything else about the logo's exact appearance below is the QC target.

## 0. PREMIUM CLOTH LOGO PRINT STANDARD (MANDATORY, user-locked 2026-07-21)
**Preserved asset.** `assets/logo/logo_official.png` ("Copy of Lucent Carat Lab Logo(1).png") is the ONE and ONLY approved logo — a LOCKED visual asset. Pass this exact file as the logo reference and **reproduce it pixel-faithfully**; treat it like an existing product photo. Never recreate / redraw / vectorize / reinterpret / simplify / restyle / recolor / modify any element.

**Approved look (benchmark).** Match the user's approved sample studio images (2026-07-21): the complete logo lockup printed naturally into premium white cotton in the lower area, jewelry the sharp hero, logo soft and secondary. That natural screen-print look is the target for every studio/office image.

**Print method.** The logo must look exactly like **premium textile ink screen-printed directly into luxury white cotton** — ink sitting INSIDE the weave, the cloth texture visible THROUGH the ink, the weave continuing under every letter. NEVER an overlay · watermark · sticker · decal · floating/projected graphic · emboss · engrave · metallic foil · CGI texture · fake displacement · AI re-creation · white box · glow · independent shadow.

**Fabric integration + textile physics.** The logo is physically printed BEFORE the photo, so it follows every fold, wrinkle, deformation, perspective change and depth-of-field transition, and receives the IDENTICAL lighting, shadows, highlights and texture as the cloth. No independent lighting/reflections/sharpness. No visible separation between logo and cloth.

**Color + tagline + completeness lock.** Never modify the diamond emblem, LUCENT, CARAT, LAB, decorative stars, horizontal lines, tagline, letter-spacing, kerning, font, stroke, layout, alignment, color, opacity or size ratio. The tagline **FUTURE OF FINE JEWELRY stays BLACK** — never recolor/bold/thin/sharpen/blur-independently/rewrite. **Exactly ONE complete logo** — no multiple/partial/cropped/ghost logos, no duplicate emblem or repeated text; the whole lockup (emblem + LUCENT + CARAT + LAB + tagline + decorative elements) stays visible.

**Focus.** Jewelry is always the hero (critically sharp). The logo is secondary and softens **uniformly with the cloth** only via natural camera depth of field — never blur only the letters, never change any logo detail when softening.

**Cloth.** Premium luxury white cotton only — fine natural weave, high thread count, soft daylight, natural folds, neutral white, soft sheen. Never cheap/canvas/linen/synthetic/paper-texture/flat cloth, never cream/yellow/gray/blue/pink/colored/tinted.

**Failure policy (zero tolerance).** If ANY logo property differs from the preserved asset, or the print looks pasted/overlaid rather than screen-printed into the weave → reject internally and regenerate on Higgsfield; never deliver.

### STRICT PRINT-ON-CLOTH ENFORCEMENT (ZERO TOLERANCE, user-locked 2026-07-21)
**Appearance target:** the logo must look as if it was professionally printed on the premium white cotton **BEFORE** the jewelry photo — the camera captures cloth + printed logo as ONE physical object, with **no visible separation** between logo and cloth. It must never look added-after / overlaid / watermarked / floating / embossed.
**Method reconciliation:** "not composited later / not an overlay" describes the **required look, not a ban on the local composite.** `print_logo_on_cloth.py` is engineered to achieve exactly this printed-before-the-shoot appearance (ink penetrates the fibres, weave shows through, follows every fold/wrinkle/stretch/compression + lighting/shadow/highlight + DoF). In-model generation is NOT used (it fails pixel-fidelity). So: local composite is the METHOD; this standard is the APPEARANCE the output must pass.
**Ink/textile integration:** ink penetrates the cotton fibres; the weave stays visible through the ink; the ink follows every fibre, thread, fold, wrinkle, stretch, compression, lighting change, shadow, highlight and DoF transition. Both cloth and logo behave as one physical object; the logo softens/sharpens ONLY with the cloth via camera DoF, never independently.
**Preserve exactly** (LOCKED asset — never recreate/redraw/vectorize/stylize/regenerate/approximate): emblem · typography · kerning · spacing · proportions · line thickness · alignment · decorative elements · tagline (BLACK) · original colours. Exactly ONE complete logo — no duplicate/partial/cropped/missing/extra-emblem/repeated-text/second-watermark. Jewelry always primary, logo secondary. Premium luxury white cotton only (high thread count, natural weave, subtle sheen, neutral pure white) — never synthetic/canvas/linen/silk/satin/paper/plastic/cheap/flat/repetitive-AI/cream/ivory/yellow/grey/blue/pink.
**Pre-delivery validation (reject + regenerate on ANY fail):** ✓ logo identical to the preserved asset ✓ physically printed into the cloth ✓ cloth texture continues through the ink ✓ follows every fold ✓ no overlay/watermark/emboss appearance ✓ premium white cotton ✓ exactly one complete logo.

## 1. WHY
the Higgsfield production model has struggled to reproduce the fine logo typography (observed: "ELLYREID" with a crown, garbled tagline), which is why the logo was historically composited locally. **[SUPERSEDED 2026-07-21 — see the METHOD OVERRIDE at the top of this file: the logo is now rendered IN-MODEL by Higgsfield only; `print_logo_on_cloth.py` is retired.]** The original rationale below is retained for context; the in-model logo is held exact by strong prompting + QC + regenerate.

## 2. LOCKED ASSET POLICY
- Source of truth: `assets/logo/logo_official.png` (repo root) — byte-for-byte copy of the user's official upload (1,079,081 bytes). Drive origin: `Lucent Carat Lab Logo.png`, file id `1QZgjplaFWenZHt048tzQntk-L-Ezy_qH`.
- NEVER AI-generate, AI-recreate, AI-redraw, AI-interpret, AI-complete, AI-repair, AI-restyle, AI-enhance, AI-approximate, AI-regenerate, redraw, verify-by-reading, vectorize, OCR, "fix", improve, simplify, stylize, or hallucinate any part of it. (Full forbidden-AI verb list — none are permitted, ever.)
- Preserve exactly: diamond-icon geometry, gold gradients, typography (font family/weight, letter+line spacing, kerning, alignment), decorative lines, star symbols, the words LUCENT / CARAT / LAB / FUTURE OF FINE JEWELRY, colors, metallic finish, proportions.
- Colors on the master: emblem + "LUCENT CARAT LAB" = GOLD; "FUTURE OF FINE JEWELRY" = BLACK/dark. Use the asset's own pixels; never recolor.
- Never ask the user to verify the logo.

## 3. TRANSPARENT LOGO GENERATION (mechanical, non-destructive)
`assets/logo/logo_official_transparent.png` is derived from `assets/logo/logo_official.png` by keying **only the pure-white background** to transparent; every logo ink pixel is preserved unchanged.
- Method: alpha = 0 where a pixel is very bright AND near-neutral (`min(R,G,B) ≥ 244` AND `max-min ≤ 8`); alpha = 255 everywhere else. No logo pixel is modified.
- Regenerate it any time from the original with `scripts/print_logo_on_cloth.py --make-transparent` (or the inline snippet in that script).
- This is a background key, NOT a redraw — compliant with the locked-asset policy.

## 4. PRINTED-ON-CLOTH COMPOSITE (the new default, user-locked 2026-07-10)
The logo must look **physically printed onto the fabric**, not a floating overlay/sticker/watermark. Use `scripts/print_logo_on_cloth.py`.

**SIX-POINT FABRIC-PRINT REALISM STANDARD (locked 2026-07-12).** A logo that fails ANY of these reads as a flat floating sticker and is INVALID. The composite must satisfy all six, and `scripts/print_logo_on_cloth.py` now enforces them:
1. **FABRIC INTERACTION** — the print follows the cloth folds; displacement warps the ink along the fold map so lines bend over folds instead of ignoring them. Never a rigid flat patch.
2. **SOFT EDGES** — no razor-crisp line; the ink alpha is slightly blurred because a real print softens where ink meets the fabric texture.
3. **WEAVE-THROUGH** — the cloth's high-frequency weave is added back ON TOP of the ink, so the fabric grain visibly runs through the gold lines; the gold is never flat.
4. **EDGE INK ABSORPTION** — a *tiny darken-only* halo where foil meets fibre so the print reads as settled IN the weave. This is NOT relief: no bright bevel, no raised edge — see the FLAT-FOIL rule below.
5. **MATCHED LIGHTING** — the ink is modulated by local cloth brightness AND clamped so a printed pixel is never brighter than the cloth beneath it; the logo shares the cloth's own highlights, shadows and curvature and never carries its own independent lighting.
6. **INK DIFFUSION** — subtle deterministic per-pixel grain + soft edges reproduce the tiny imperfections/edge bleed of real fabric printing.

**FLAT HOT-FOIL FINISH (locked 2026-07-12).** The result must look like a flat metallic **gold-foil** print **professionally hot-foil stamped** into premium fabric — the foil is integrated into the textile, not a flat graphic sitting on it. The foil follows every fold, wrinkle and curvature (via displacement, macro deformation) but stays **FLAT**: explicitly **NO** floating/sticker effect, **NO** embossing, **NO** 3D extrusion, **NO** bevel or raised relief, **NO** independent light source on the logo. Point 4's edge treatment is darken-only ink absorption and must never become a 3D emboss.

Plus placement rules: natural and OFF-CENTER (typically lower / lower-center / lower-right), never perfectly centered; partial visibility preferred (~60–90 % — cropped by frame, hidden behind the jewelry, or interrupted by a fold); and logo pixels remain identical (only blended into the cloth lighting, never repainted).

**USER MANDATE (2026-07-12) — LOGO IS A REQUIRED PART OF THE SCENE.** Every studio shot MUST contain the Lucent Carat Lab logo physically printed on the white fabric beneath the ring. Never remove, fade, blur, crop or replace it. A clean-cloth-only studio shot is INVALID. If the logo cannot be reproduced correctly, **reject the generation** — never remove or alter it.

**PRIMARY method (mandated): generate the logo IN-SCENE.** Feed the model the official logo artwork (`assets/logo/logo_official.png`) *and* a branded-cloth reference as media inputs, and instruct it to reproduce the EXACT logo as premium metallic gold **hot-foil stamping printed into** the fabric, satisfying all six points above plus the flat-foil rule, at reference scale/position with exact typography. Then **verify every render vs the official artwork** and **reject + regenerate** any where the logo drifts, floats, embosses, or is missing.

**FALLBACK (only if in-model cannot reproduce the exact logo after retries):** generate on clean cloth and composite the locked logo locally via `scripts/print_logo_on_cloth.py` (pixel-exact, enforces the same six points). Use this when nano_banana garbles the fine typography — the composite guarantees exact letterforms. Either path must end with the exact logo permanently printed into the fabric; neither may ship a missing or approximated logo.

### Script usage (run locally by the user, 0 credits)
```
pip install pillow numpy
python scripts/print_logo_on_cloth.py \
    --image  studio_shot.png \
    --logo   assets/logo/logo_official_transparent.png \
    --scale  0.42 \
    --pos    lower-right \
    --opacity 0.9 \
    --displace 6 \
    --soften 1.0 \
    --grain  0.06
# outputs PRINTED_studio_shot.png
```
Parameters: `--scale` logo width as fraction of image; `--pos` one of lower-right/lower-center/lower-left (or `x,y` fraction); `--opacity` ink strength; `--displace` fold-warp strength (px, point 1); `--soften` ink-edge blur radius in px (points 2 & 6); `--grain` ink-diffusion imperfection 0..1 (point 6). The script warps the ink along the fold map, multiplies it into the cloth modulated by local brightness, clamps it so it never out-brightens the cloth, adds the weave back over the ink, and rings the edges with a faint embed shadow — satisfying all six realism points.

## 5. RULES THAT PREVENT AI FROM RECREATING LOGOS
- Studio generation prompts explicitly say: "plain pure-white cloth, absolutely NO logo/emblem/text/watermark anywhere — clean fabric only" so the model leaves the cloth clean.
- The logo is added ONLY by the local composite step from the locked asset.
- If a generated studio image contains ANY logo that differs from `assets/logo/logo_official.png`, the generation is FAILED — discard that logo region and composite the real one.
- Never treat a model-drawn logo as acceptable, even if it looks close.

## 6. WHY LOCAL (not Higgsfield)
- 0 credits, pixel-identical, deterministic, repeatable.
- Higgsfield CloudFront outputs are network-blocked for us to download (verified: proxy returns 403 on the CDN), so the composite is run by the USER on their downloaded outputs (same pattern as `whiten_cloth.py`). Claude cannot fetch the output bytes to stamp them here.

## 7. LOGO PRESENT = ABSOLUTE DELIVERY REQUIREMENT (user-locked 2026-07-10)
Every STUDIO photograph MUST contain the official logo, printed on the cloth. **An image without the logo is INVALID and must never be delivered.**
- A clean-cloth Higgsfield render is an **intermediate**, NOT a deliverable. It becomes valid ONLY after `scripts/print_logo_on_cloth.py` stamps the locked logo onto it.
- Delivery checklist (verify before any studio image is considered final):
  ✓ Logo exists ✓ it is the official preserved asset (`assets/logo/logo_official.png`, unmodified) ✓ physically printed on the cloth (multiply-blend, texture shows through) ✓ follows cloth folds/perspective ✓ naturally positioned (off-center; partial crop/occlusion OK) ✓ not redrawn or recolored.
- If any check fails → re-run the composite (adjust `--pos/--scale/--opacity/--displace`); if the underlying render is unusable, regenerate the render, then composite. Never ship without the logo.
- **Pipeline boundary:** because Claude cannot download the CDN outputs, the composite (and therefore the validity gate) executes on the user's machine. The generation step delivers clean-cloth intermediates + the exact stamp command; the user's composite produces the valid, logo-bearing finals.

## 8. PIXEL-IDENTICAL LOGO POLICY (locked 2026-07-10, part of P0)
The preserved `assets/logo/logo_official.png` is the ONLY source of truth. The visible logo must be IDENTICAL to it: diamond-icon geometry, typography, character/word/line spacing, decorative stars, horizontal lines, tagline, relative proportions, GOLD print color, stroke thickness, overall layout. The ONLY permitted changes are those a photographed cloth causes: perspective, folds, curvature, lighting, shadows, partial crop, partial occlusion by folds. Never gray/black text, different font/icon/spacing, simplified artwork, or missing elements. If the logo drifts → discard and regenerate against the preserved reference; never AI-repair a wrong logo.

## 9. LOGO AS METALLIC INK PRINTED INTO THE CLOTH (locked 2026-07-10)
The whole frame is one continuous physical scene: the logo exists as metallic gold ink permanently printed into the cloth BEFORE folding and BEFORE the ring is placed. Therefore it follows the cloth weave, bends with folds, compresses where the cloth compresses, stretches only with cloth deformation — never floats, never looks digitally overlaid. Logo visibility may be full / partially cropped / partly hidden by folds / entirely out of frame — all acceptable if natural. The logo is never the hero; the jewelry is.

## 10. LOGO-AS-GENERATION-REFERENCE (in-model path, when CDN composite unavailable)
When the local composite cannot run (render not downloadable), pass the official logo as an extra generation reference so the model copies the exact artwork instead of re-inventing it. Studio medias order: [branded-cloth reference, SOURCE ring, OFFICIAL logo]. Prompt: keep cloth+ring; print the logo to MATCH the official reference exactly (metallic gold, all elements). Discard and re-fire any render whose logo drifts. Official logo Higgsfield import is session-ephemeral — re-import from Drive `1QZgjplaFWenZHt048tzQntk-L-Ezy_qH` each session.

## 11. GOVERNING RULE — OMIT OVER APPROXIMATE (user-locked 2026-07-10, supersedes §10 in-model path)
The AI must NEVER recreate, redraw, infer or approximate the logo. Priority:
1. If the exact preserved asset can be applied (local composite `print_logo_on_cloth.py`, or a render whose in-model logo is provably pixel-identical to `assets/logo/logo_official.png`), use it unchanged.
2. If the exact asset cannot be applied, OMIT the logo entirely — generate on clean cloth.
**A MISSING logo is ACCEPTABLE. An INCORRECT / AI-approximated logo is UNACCEPTABLE.** Under no circumstance may AI-generated text/branding replace the official logo.
- Practical default here (CDN download blocked): studio shots are generated on CLEAN white cloth with NO logo; the exact logo is added by the local composite from the preserved asset, or left absent. The §10 "logo-as-generation-reference" path is allowed ONLY when the rendered logo is verified pixel-identical; if it drifts (gray/wrong font/missing elements), discard and fall back to clean cloth (omit) — never ship the approximation.

## 12. NEVER AI-GENERATE THE LOGO OR THE CLOTH; LOGO MUST MERGE NATURALLY (user-locked 2026-07-11)
Two brand surfaces are NEVER freely generated by AI: the **logo** AND the **background cloth**. Reported failures being locked out:
1. **AI-generated / inaccurate logo:** some images had a logo the AI drew or altered, not the preserved asset. FORBIDDEN. The visible logo must be the exact preserved `assets/logo/logo_official.png`, applied by the local composite (`scripts/print_logo_on_cloth.py`) — or OMITTED. Never let the model draw, alter, or "improve" it.
2. **Logo not merging with the cloth:** the logo looked pasted/floating instead of printed. It must read as **metallic ink printed INTO the fabric** — following weave, folds, curvature, lighting and shadows (multiply/linear-burn blend, texture shows through; tune `--displace/--opacity/--scale/--pos`). A logo that sits flat on top of the cloth is a FAIL → re-composite until it blends naturally.
3. **AI-invented cloth:** the cloth is not to be freely generated either — it must stay the approved **premium white cotton with natural soft draping**, never a new AI fabric, never yellowish, never flat/simple (see docs/11). Fix warm casts locally with `whiten_cloth.py`.
Rule of thumb: AI renders the *ring on faithful approved cloth*; the *logo and the cloth identity* come from the locked assets/standard, never from the model's imagination.

**Scope + remedy (user-locked 2026-07-11):** this applies to EVERY office/studio photoshoot, permanently. The only transformations the logo may show are those the cloth naturally causes (perspective, folds, curvature, lighting, shadows, partial crop, partial occlusion). If a studio image has an AI-generated/altered logo, a floating/pasted logo, a logo differing from the preserved artwork, or a replaced/recolored cloth → **reject and automatically regenerate until all requirements are satisfied. NEVER return a studio image with an AI-generated logo.** The preserved official logo is the ONLY acceptable logo for office/studio photoshoots.

## 14. HARD RULE — LOGO MUST NEVER APPEAR AS A DIGITAL OVERLAY (user-locked 2026-07-16)
Observed failure (LR studio render, prior session): the logo was unnaturally sharp while the cloth was softer; gold lines sat on top of the weave with no fabric-grain showing through; no fold deformation (stayed flat); no ink sink into fibres; uniform self-lighting instead of the cloth's light direction; not partly hidden by highlights/valleys. Net read = clean digital overlay / watermark. This is INVALID and must be rejected — it is the exact opposite of §4's six-point standard and §9 (metallic ink printed INTO the cloth).

**LOGO MUST NEVER APPEAR AS A DIGITAL OVERLAY.** The Lucent Carat Lab logo must be physically printed on the cloth *before* the photograph is taken.

Forbidden (any one of these = reject the image):
- No background plate · no white patch · no shadow behind the logo · no glow · no outline
- No opacity tricks · no compositing look · no watermark appearance · no post-production placement look

The logo MUST:
- Follow the cloth weave.
- Warp with every fold.
- Stretch naturally with the fabric.
- Receive identical lighting as the cloth (same direction/intensity — no independent brightness).
- Lose sharpness according to camera focus / depth of field (never sharper than the surrounding cloth).
- Be partially hidden by folds / highlights / valleys if applicable.
- Behave exactly like real metallic fabric printing (ink slightly sinks into the fibres).

**If the logo looks digitally placed, reject the image** — regenerate in-scene or fall back to the local composite (§4 fallback / `scripts/print_logo_on_cloth.py`). Never ship an overlay-looking logo. Consistent with §4, §7, §9, §12: physically printed on cloth, no shadow behind, no white background behind, never a watermark/AI overlay.

## 13. FAILURE POLICY & ASSET CACHING (user-locked 2026-07-11)
**Reject the image** if the logo design differs from the preserved asset, the logo looks AI-generated, the logo does not merge naturally (floating/pasted/flat), the cloth material changes, the cloth becomes yellowish/non-white, or the cloth looks flat/cheap/artificial/overly simple. Full policy + remedies in `docs/11_BACKGROUND_STANDARD.md` (FAILURE POLICY). **Caching:** cache and reuse the locked logo + premium cotton cloth assets across devices/sessions; caching is byte-preserving only and must never alter image quality or asset fidelity — verify against `config/project_manifest.json` `locked_asset_checksums` before use.

## 8. COMPOSITING IS A MANDATORY, RETRYABLE STAGE — THE RENDER IS IMMUTABLE (user-locked 2026-07-16)

**Higgsfield returning a clean-cloth render is SUCCESS, not failure.** The studio render is a logo-free intermediate by design (§4, `CLAUDE_SETUP.md` §72). A render with no logo has not failed — it has not yet been composited.

Post-render sequence, every studio/office image:
1. Detect the white cloth.
2. Print the preserved logo physically onto it (`scripts/print_logo_on_cloth.py`).
3. Preserve the original logo asset exactly — pixel-identical.
4. Never redraw or regenerate the logo with AI (P0).
5. Never overlay it as a watermark.
6. **Never finish the pipeline until compositing succeeds.**

**If the composite step fails or the result fails the §7 gate:**
- Retry automatically.
- Repair the compositing script if needed.
- **Resume from the failed step only.**
- **Do NOT regenerate the Higgsfield image. Do NOT ask the user to regenerate it.**

**The Higgsfield render is IMMUTABLE.** Only the compositing stage is retried. A logo fault is never grounds for spending credits on a new render — the fault is downstream of generation, and re-rendering also risks fresh geometry drift under the `legacy` production pipeline (`docs/15` §0).

**Never mark the job complete until the final image contains the preserved printed logo on the cloth.** Compositing is not optional post-processing; it is a production stage, and the deliverable does not exist until it has run.

**Known composite failure modes and their fixes** (all resolved by parameters, never by re-rendering):
- *White box / patch behind the logo* → the opaque `logo_official.png` was used. Use `logo_official_transparent.png`.
- *Ink dissolves, tagline vanishes* → `--soften` too high and/or `--opacity` too low. The script's documented defaults (`--scale 0.42 --opacity 0.9 --displace 6 --soften 1.0 --grain 0.06`) are tuned; deviate deliberately, not by habit.
- *Bright halo / emboss ring around strokes* → `--soften` above ~2. Reduce it.
- *Logo cropped by the frame* → reduce `--scale` or move `--pos` so `x+lw <= W` and `y+lh <= H`. Partial crop is permitted by §7 but never accidental.

## 9. APPROVED LOGO TREATMENT — REFERENCE STANDARD (user-approved 2026-07-17)

The user approved this treatment from an existing catalog (emerald-cut eternity band, white metal, white cotton). **This is the benchmark every studio/office logo must match.** Observed properties:

- **Scale:** the lockup spans roughly a quarter to a third of the frame width. Present and legible, never the subject.
- **Placement:** lower area of the frame, offset from centre, clear of the ring. The ring occupies the upper/middle; the logo sits below and behind it in the visual hierarchy.
- **Completeness:** the full lockup is readable — diamond icon, LUCENT / CARAT / LAB, both stars, both decorative rules, FUTURE OF FINE JEWELRY tagline. Not cropped, not truncated.
- **Tone:** soft muted gold, tone-on-tone against the white cloth. Clearly visible but never bright, never competing with the metal or the diamonds. It reads as ink, not as foil.
- **Integration:** the ink follows the fold contours; the cloth's own soft shading passes across it; it shares the scene's depth of field rather than being uniformly sharp against a soft background.
- **Hierarchy:** jewelry first, cloth second, logo last. In a close-crop the logo may be the only element visible and that is still acceptable — the rule is that it never *competes* when the ring is in frame.

**Contrast with what was rejected (2026-07-16/17):** oversized and centred, ring overlapping it unnaturally, icon distorted, flat and uniformly sharp over the fabric, brighter than the cloth around it. See `QUALITY_MEMORY` → `lr0151-inmodel-logo-flat-overlay`.

**Local composite parameters that reproduce this standard:** `--scale 0.28-0.34`, `--pos` lower-right or lower-centre, `--opacity 0.45-0.6`, `--displace 6-8`, `--soften 1.0`, `--grain 0.06`. (20% opacity was too faint and read as a ghost; 90% too assertive.)

## 10. OFFICIAL LOGO PRINTING POLICY (mandatory, user-locked 2026-07-17)

Print the official preserved logo as a **real physical print on premium plain white cotton** — never a digital overlay, watermark, sticker, emboss, engraving, projection or AI recreation.

**The logo remains 100% identical to the official asset.** Never modify: shape · typography · diamond icon · colors · metallic gold finish · gradient · stroke thickness · letter spacing · alignment · opacity · texture. Print it exactly as a professional textile printer would onto white fabric.

It must follow the cloth's folds, wrinkles, weave, perspective, lighting, shadows and depth naturally, without looking artificial. The print appears slightly **absorbed into the cotton fibres** with realistic ink interaction, while staying crisp and fully legible.

Do not increase brightness, saturation, contrast, sharpness, metallic effect or gloss beyond the original asset. The cloth stays pure white. **Only the cloth may deform — the logo artwork itself is never redesigned or distorted.**

> **STOP CONDITION (binding): if the logo cannot be reproduced pixel-identically, STOP GENERATION rather than approximate it.**

### WHAT "ONLY THE CLOTH MAY DEFORM" MEANS
The artwork is never *redesigned* — no re-lettering, no redrawn icon, no restyled strokes. It does *displace* with the substrate it is printed on, exactly as real ink on real fabric does. Warping along the fold map is the cloth deforming and carrying the ink with it; redrawing the letterforms is not. `scripts/print_logo_on_cloth.py` implements precisely this distinction: the asset's pixels are never repainted, only displaced, blended and modulated by the cloth beneath them.

### THE STOP CONDITION IS ACTIVE FOR IN-MODEL GENERATION (recorded 2026-07-17)
A generative model **cannot** reproduce the logo pixel-identically — it re-synthesises the artwork. Verified twice this session: the icon overlapped the wordmark and the layout changed; then the icon was distorted and the print sat flat on the fabric. `docs/04` §1 records the same failure from before ("ELLYREID" with a crown). `QUALITY_MEMORY` → `lr0151-inmodel-logo-flat-overlay`, repeat_count 3.

**[SUPERSEDED 2026-07-21 — see the METHOD OVERRIDE at the top of this file: the logo is now rendered IN-MODEL by Higgsfield only; the composite is retired, so the paragraph below no longer applies as current policy and is kept for historical context.]** Therefore, under the previous policy, generating the logo in-model was a stop condition, not a retry condition; pixel-identity came from exactly one source: the preserved asset, composited (§4, §8, §9).
