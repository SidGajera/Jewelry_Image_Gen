# 04 — LOGO WORKFLOW (locked asset + printed-on-cloth compositing)

The single most important workflow in the project. Priority **P0** — overrides everything.

## 1. WHY
Higgsfield `nano_banana_2` CANNOT reproduce the fine logo typography. Whenever it tries, it hallucinates a fake logo (observed: "ELLYREID" with a crown, garbled tagline). Therefore the AI must NEVER render the logo. The logo is a **locked graphic asset** that is **composited locally** after generation, so it stays pixel-identical.

## 2. LOCKED ASSET POLICY
- Source of truth: `assets/logo/logo_official.png` (repo root) — byte-for-byte copy of the user's official upload (1,079,081 bytes). Drive origin: `Lucent Carat Lab Logo.png`, file id `1QZgjplaFWenZHt048tzQntk-L-Ezy_qH`.
- NEVER regenerate, redraw, interpret, verify-by-reading, enhance, vectorize, recreate, OCR, "fix", improve, simplify, stylize, or hallucinate any part of it.
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

Requirements the composite must satisfy:
1. Fabric texture shows THROUGH the print (use multiply / linear-burn style blend for the gold+dark ink, so the weave and grain remain visible). Not a flat opaque patch.
2. The print follows the cloth's perspective and subtle surface deformation (optional light displacement by the cloth's own luminance/fold map).
3. It sits under the fabric's shadows and highlights (folds and shadows pass over it).
4. Placement is natural and OFF-CENTER (typically lower / lower-right), never perfectly centered.
5. Partial visibility is acceptable and preferred: slightly cropped by the frame, partly hidden behind the jewelry, or interrupted by a fold — ~60–90 % visible.
6. Logo pixels remain identical (only blended into the cloth lighting; never repainted).

### Script usage (run locally by the user, 0 credits)
```
pip install pillow numpy
python scripts/print_logo_on_cloth.py \
    --image  studio_shot.png \
    --logo   assets/logo/logo_official_transparent.png \
    --scale  0.42 \
    --pos    lower-right \
    --opacity 0.9 \
    --displace 6
# outputs PRINTED_studio_shot.png
```
Parameters: `--scale` logo width as fraction of image; `--pos` one of lower-right/lower-center/lower-left (or `x,y` fraction); `--opacity` ink strength; `--displace` fold-warp strength (px). The script multiplies the ink into the cloth and modulates it by the cloth's local brightness so it reads as printed.

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
