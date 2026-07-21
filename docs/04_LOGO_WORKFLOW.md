# 04 — LOGO WORKFLOW (locked asset + printed-on-cloth compositing)

The single most important workflow in the project. Priority **P0** — overrides everything.

## 0. LUXURY CLOTH & EMBLEM INTEGRATION POLICY (P0, user-locked 2026-07-21)
The official Lucent Carat Lab logo is a PRESERVED MASTER ASSET (`assets/logo/logo_official.png`) — the complete lockup (diamond emblem + typography + decorative lines + BLACK tagline). It must **NEVER** appear as digital artwork placed over the image; it must exist **as part of the physical cloth itself**, permanently printed into the premium white cloth *before* the photo is taken.

**Emblem printing (like luxury textile ink):** penetrates the fibres · follows every thread · bends with every fold · stretches with fabric deformation · compresses where cloth compresses · disappears slightly into the weave · stays physically attached to the cloth. Never render the logo independently of the cloth — it must look impossible to separate from it.

**No digital look — reject:** vector artwork · watermark · overlay · pasted/floating/hovering logo · emboss · glossy logo · AI-generated typography · isolated emblem.

**Focus priority:** 1 Jewelry · 2 Diamond · 3 Metal · 4 Cloth · 5 Logo. Jewelry always the hero with perfect focus; if logo and jewelry share depth, the logo is physically correct but naturally softer ONLY from optical DoF — never blur/sharpen the logo independently.

**Premium white cloth:** pure neutral white, elegant folds, realistic micro-texture, premium definition. Never flat/plastic/CGI/synthetic/repeating-weave cloth, never coloured/cream/grey/blue. **VELVET IS THE PREFERRED PREMIUM CLOTH (user-locked 2026-07-21, LR-0183):** premium pure-white plush jewelry-box VELVET — soft dense pile, gentle natural sheen, elegant soft folds, rich/expensive look — reads more premium than cotton and is the default studio cloth; the logo prints as matte foil/ink pressed INTO the velvet pile (following the nap), never glossy/sticker/overlay. Fine cotton remains acceptable, but prefer velvet for the premium look. The whole logo must sit fully visible on the cloth with the ring NOT overlapping the emblem (see §4 COMPLETE & READABLE lock).

**Colour + typography LOCK:** the preserved logo colours/gradient/metallic appearance/typography/emblem/spacing/decorative lines/tagline are LOCKED — never recreate/recolour/brighten/darken/modify anything. Use the preserved asset exactly.

**Single logo:** exactly ONE complete logo — never duplicate/partially-duplicate/crop/add-extra-emblem/add-typography.

**Camera realism:** the result must read as *"a photographer placed a real ring on an expensive branded cloth and photographed it,"* never *"an AI generated a ring and added a logo afterwards."* Nothing may reveal AI generation; cloth + logo + jewelry are one physically consistent scene.

**FINAL VALIDATION — reject immediately if:** logo looks pasted / too sharp / floats / doesn't follow folds · cloth looks AI-generated or not premium white · jewelry not dominant · logo competes with jewelry · multiple/partial logo · wrong colours/typography/emblem/tagline · any part of the preserved logo modified.

**COLOUR & PRINT LOCK (user-locked 2026-07-21 — explicit reinforcement, merged here).** The supplied logo is the SINGLE MASTER LOGO and a LOCKED asset: never recreate/redraw/reinterpret/restyle any part.
- **Gold lock:** match the preserved gold EXACTLY — hue, brightness, saturation, gradient, opacity, metallic appearance. Never brighten, darken, boost saturation, or shift it toward orange / yellow / bronze; never make it glossy or shiny.
- **Tagline lock:** "FUTURE OF FINE JEWELRY" stays BLACK exactly as supplied — never gold, never grey, never faded; font/spacing/thickness/opacity unchanged. Black decorative elements stay black.
- **Material lock (refines the §4 foil framing):** the print is **matte textile ink absorbed into the fibres** — never glossy, reflective, metallic-coating, laminate, embossed, sticker, or vector overlay. Where §4 says "hot-foil," it means flat/matte-into-the-weave, never a shiny raised foil.
- **Texture lock:** the cloth weave/fibre/thread pattern must continue visibly THROUGH the logo; the print is never smoother than the cloth around it.
- **Consistency lock:** every catalog image uses the IDENTICAL logo — same colour, typography, emblem, spacing, tagline, decorative lines, proportions. No per-image variation.
- **Instruction wording (reduces model redraw tendency):** never ask the model to "generate the logo." State: *"The attached preserved logo is the only valid logo. Use it unchanged. Do not recreate or reinterpret any part of it. Treat it as an existing physical textile print already embedded into the premium white cloth."* In practice this is guaranteed only by the local composite (below) or by omitting the logo on the render — an AI-drawn logo recolours the two-tone lockup to single-tone gold every time (see `config/QUALITY_MEMORY.json#logo-tagline-color-drift`).

**PERMANENT LOGO PRINTING POLICY (P0, user-locked 2026-07-21 — merged, overrides every prompt/style/preference).** The uploaded Lucent Carat Lab logo is the ONLY approved logo and a LOCKED MASTER ASSET. NEVER recreate / redraw / vectorize / regenerate / stylize / approximate / replace typography or the diamond emblem / modify spacing, kerning, proportions, line thickness, colours, the black tagline or the gold tone / crop / partially hide / generate a similar logo. **The uploaded logo ITSELF must be transferred onto the cloth** (i.e. the preserved PNG's own pixels), so the ONLY compliant method is the local composite — the AI never draws it. The print must read as real luxury textile printing: ink absorbed into the velvet fibres, following every fold/wrinkle/compression/stretch/angle and the scene lighting, inheriting the cloth texture, with the tiny imperfections of premium textile printing — NEVER perfectly-smooth edges, digital sharpness, glowing edges, floating/detached/sticker/overlay/watermark/decal/emboss/fake-metallic look. **Cloth:** premium pure-white plush VELVET only (soft dense pile, neutral white — never grey/cream/yellow/blue, never cotton weave/linen/paper/synthetic). **Focus:** jewelry always the critically-sharp hero; the logo may soften ONLY from optical depth of field, never lose its shape/typography/emblem/tagline. **Reject + regenerate** if: logo recreated/redrawn, wrong emblem/typography/spacing/kerning/gold tone, tagline changed, partial/cropped/multiple/floating logo, sticker/overlay look, logo not following the velvet folds or not embedded, cloth not premium white velvet or texture artificial, or jewelry loses focus to the logo. Done ONLY when the logo is visually indistinguishable from a real logo physically printed into premium white velvet. Reference benchmark: §9 VELVET BENCHMARK (the user's "exactly like this" image).

*Method note:* pixel-exact printed-into-cloth is achieved by the local composite `scripts/print_logo_on_cloth.py` from the preserved asset (runs where the render is downloadable). This §0 defines the appearance every studio/office image must satisfy.

## 1. WHY
the Higgsfield production model CANNOT reproduce the fine logo typography. Whenever it tries, it hallucinates a fake logo (observed: "ELLYREID" with a crown, garbled tagline). Therefore the AI must NEVER render the logo. The logo is a **locked graphic asset** that is **composited locally** after generation, so it stays pixel-identical.

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

Plus placement rules: natural, lower area of the frame (lower-centre / lower-right), never dead-centre under the ring. **NATURAL PHOTOGRAPHY LOGO VISIBILITY (user-locked 2026-07-21 — supersedes the interim "complete & readable, never cropped" note):** the goal is a real luxury-jewelry studio photograph, NOT showing the whole logo in every frame. The logo is composited as ONE complete physical print onto the cloth FIRST; then it is completely natural — and preferred for authenticity — for it to be partially hidden by cloth folds, jewelry placement, camera composition, depth of field, image crop, perspective or framing. Acceptable: the ring covers part of it, a fold hides part, the crop cuts part away, only the emblem or only part of the wordmark/tagline shows, one side exits the frame. The hidden portion still exists physically beneath the fold / outside the frame — it is NEVER AI-reconstructed, re-drawn, or altered. NEVER allowed (unchanged): regenerating/reconstructing any part of the logo, changing emblem geometry/typography/kerning/spacing/proportions/gold tone/black tagline, AI-replacement logo, overlay/sticker/watermark/floating/digital-looking/embossed-fake logo, or multiple logos. Never compose the shot just to fit the whole logo; prioritise the natural photograph. Jewelry is always the hero; the logo is supporting branding. Logo pixels remain identical to the master (only blended into the cloth lighting and naturally occluded, never repainted).

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

**VELVET BENCHMARK (user-locked 2026-07-21, "exactly like this", LR-0194):** the user supplied a definitive reference of the preserved logo printed on premium white plush VELVET — gold emblem line-art and gold LUCENT CARAT LAB wordmark with the BLACK tagline, the velvet pile/fibres visibly crossing the gold strokes, matte (no foil-shine), the emblem's fine lines softly absorbed into the nap, sitting in the lower frame below/behind the ring. This embedded-into-velvet look is the PERMANENT standard for every office/studio shot. **It is produced by the local composite (`print_logo_on_cloth.py`) stamping the preserved PNG onto a clean velvet plate — that is what the reference itself is.** An in-model (AI-drawn) logo only ever approximates it and must not be treated as matching this benchmark. Production flow for office/velvet shots: render a CLEAN velvet plate (ring upper, clean velvet lower half) → composite the preserved logo locally (velvet-tuned: `--pos lower-centre --scale ~0.4-0.5 --opacity ~0.5 --displace 9 --soften 1.2 --grain 0.08`). The composite runs where the render is downloadable (desktop, or pull the plate via Google Drive).

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

Therefore, **under this policy, generating the logo in-model is a stop condition, not a retry condition.** Pixel-identity is available from exactly one source: the preserved asset, composited (§4, §8, §9). The stop condition does not forbid delivering images — it forbids asking the model to draw the logo.
