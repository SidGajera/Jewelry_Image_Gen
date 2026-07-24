# 11 — MASTER BACKGROUND STANDARD (PERMANENT)

The approved reference images (round solitaire on white cloth with the printed Lucent Carat Lab logo) define the ONLY approved studio background. They are the permanent canonical reference for every future generation unless the user explicitly replaces them.

## NEVER AI-INVENT THE CLOTH (user-locked 2026-07-11, P3)
The background cloth is NEVER to be freely generated/invented by AI. It must reproduce the approved **premium white cotton** cloth from the reference/asset — same material, same premium quality, same natural soft draping — every time. The AI's only job is to keep that approved cloth faithful under the ring; it must not substitute a new, cheaper, flat, or differently-colored fabric. Two locked failures to never repeat:
- **Yellowish cloth:** cloth rendered cream/warm/yellow instead of neutral premium white → fix locally with `whiten_cloth.py` (0 credits); never accept a warm cast.
- **Simple/flat cloth:** cloth rendered plain, cheap, or texture-less instead of premium cotton with natural soft draping → cloth must always read as premium white cotton with soft, believable folds and fine grain, never a flat blank sheet.

## CLOTH MATERIAL — VELVET ONLY (MANDATORY, user-locked 2026-07-24; supersedes the 2026-07-21 "velvet preferred" wording)
**Office/studio photoshoot backgrounds MUST use premium pure-white plush VELVET — and nothing else.** Luxury jewelry-box velvet: soft dense pile, gentle sheen, elegant soft folds (`docs/04 §0`).

**No other background material, surface, or texture is permitted for office photoshoot images.** Cotton is NO LONGER an acceptable alternate — the 2026-07-21 "cotton remains acceptable" clause is revoked. Also never: silk, satin, linen, marble, paper, leather, coarse visible-weave fabric, a flat plain sheet, or any other material.

**Enforcement (both gates are mandatory):**
1. **Prompt-build gate** — before submitting any office-photoshoot generation, confirm the prompt names velvet and names no other fabric. A prompt that says "cotton" (or any non-velvet material) must be corrected before submission, not after.
2. **Pre-delivery gate** — validate the rendered background reads as velvet. Any office photoshoot image with a non-velvet background is REJECTED and the rejection is recorded in Failure Memory (`config/QUALITY_MEMORY.json`).

> Recorded failure: `LR-0189` Image 1 (job `5f0e3049-bb0b-46c3-a849-77a947b0e3a0`, 2026-07-24) was built with "premium white cotton cloth" in the prompt and is rejected under this rule.

## PRIORITY — JEWELRY IS THE HERO (user-locked 2026-07-24, governs this whole file)
**The jewelry is always the clear focus and highlight of every image.** The logo is secondary branding and must NEVER hide, distract from, or compete with the jewelry. Where any rule in this file would make the logo more prominent, the jewelry wins and the logo yields.

## LOGO ON VELVET — NATURAL PRINT OR NO LOGO (user-locked 2026-07-24)
The logo must read as **naturally printed / embedded into the velvet**: metallic gold ink sitting in the pile, following folds, pile direction, perspective, lighting and shadow. It may be cropped or partly hidden behind the ring — that is normal for a real shoot.

**Never deliver a logo that looks like:** a sticker, an overlay, a floating or pasted graphic, a flat stamp on top of the fabric, or anything sitting in a white box / lighter patch.

**FALLBACK (mandatory, not optional):** if the logo cannot be made to print naturally on the velvet, deliver **PLAIN velvet with NO logo**. A missing logo is acceptable; an artificial or pasted-looking logo is not. This restates `docs/04` P0 "OMIT OVER APPROXIMATE" for the velvet background specifically.

**KEEP THE LOGO SUBTLE (user-locked 2026-07-24).** It is **acceptable and preferred that ~90% of the lockup is hidden** — buried under velvet folds or cropped away by the frame edge. That is what a real shoot looks like. **Never enlarge, centre, or emphasise the logo** in any way that reduces jewelry focus. Small, edge-biased, mostly-gone is the target; a fully legible centred lockup is a failure even when it prints naturally.

**Pre-delivery check — all three, in order:**
1. Jewelry is the clear highlight of the frame.
2. Background = velvet.
3. Any visible logo reads as naturally printed **and** stays subtle / partially hidden.

If (3) fails, remove the logo and deliver plain velvet rather than re-shipping an artificial or over-prominent version.

**Implementation.** Local composite `scripts/print_logo_on_cloth.py --fabric velvet` (0 credits, logo pixels never repainted). Velvet profile models nap absorption, pile sheen coupling, coarse fold displacement and pile-through texture. Defaults are subtle by design: `--scale 0.24`, `--pos edge-lower-right`, `--opacity 0.68` — roughly 80% of the lockup falls outside the frame before folds hide more. Automated gates: `scripts/validate_render.py` → `jewelry_hero`, `velvet`, `logo_natural`, `logo_subtle`.

## CLOTH COLOR — LOCKED NEUTRAL WHITE
The cloth must always be pure premium / neutral / bright luxury white.
NEVER allow: cream, ivory, beige, yellow, warm-white, off-white, gray, blue, pink, or any tint.
There must never be yellowish/creamish/warm lighting affecting the cloth. Maintain a consistent neutral white balance across every image.
If a render drifts warm/tinted → fix with `whiten_cloth.py` locally (0 credits). Never regenerate for color.

## CLOTH APPEARANCE — CONSISTENT
Always preserve the same: texture, softness, fabric grain, fold style, wrinkle character, premium appearance. Folds naturally draped and elegant, exactly like the references — not random folds or different fabric styles.

## LOGO ON THE BACKGROUND
The official logo must always appear as a realistic PRINT on the cloth (see docs/04). It must NOT look like a watermark, floating overlay, sticker, or digital stamp — it must look professionally printed onto the fabric before the product was photographed.
- Always use the locked asset; never redraw/recreate/regenerate.
- Preserve icon, typography, spacing, tagline, colors, proportions.
- The print follows cloth perspective, folds, texture, lighting, shadows.
- Acceptable: fully visible, slightly cropped, partially covered by the jewelry, or slightly interrupted by folds — like a real luxury photoshoot.

## CONSISTENCY (applies to EVERY catalog image)
Every image must look photographed on the same cloth, in the same studio, with the same lighting, the same camera, the same white balance, and the same printed logo. There should be no visible difference in cloth material, cloth color, logo color, lighting, or premium appearance between catalog images.

## LOCKED CLOTH ASSET — ASSET-ONLY, NEVER AI-GENERATED (user-locked 2026-07-11)
The premium white cotton cloth is a **preserved asset**, exactly like the logo — it is NEVER generated anew by AI. Reuse only the approved cloth asset (`assets/background/sample_studio_background_with_logo.png`, sha256 `4cc10d33…`, and the `Offie_photoshoot 1–5` Drive references that embody the same cloth). Preserve its material, texture, softness, weave, fine grain, and natural draping; keep neutral pure-white balance; cloth may be plain or naturally folded but must always look premium and physically realistic. The AI's only job is to keep this approved cloth faithful under the ring — never to invent a substitute fabric.

## FAILURE POLICY — REJECT THE IMAGE IF (user-locked 2026-07-11, applies to logo + cloth)
An image is INVALID and must be rejected/re-done if ANY of these is true:
- logo design differs from the preserved asset;
- logo looks AI-generated;
- logo does not merge naturally with the cloth (floating / pasted / flat on top);
- cloth material is anything other than premium white VELVET (velvet-only rule above) — including cotton;
- cloth becomes yellowish or non-white (any warm/color cast);
- cloth looks flat, cheap, artificial, or overly simple.
Remedy: omit the logo rather than ship an inaccurate one; re-composite the exact logo to merge naturally; fix warm casts with `whiten_cloth.py` (0 credits); **automatically regenerate until all requirements are satisfied. NEVER return a studio image with an AI-generated logo** — the preserved official logo is the only acceptable logo for office/studio photoshoots.

## CACHING (cross-device / cross-session)
Cache and reuse these locked assets (logo + premium cotton cloth) across devices and sessions. Caching is byte-preserving only — it MUST NEVER alter image quality or asset fidelity. Verify against the manifest `locked_asset_checksums` before use; if a cached copy's checksum differs, discard it and restore from the repo.

## REFERENCE IMAGES
The user-provided reference set (round solitaire + pavé-shoulder solitaires on white cloth with printed logo, 2026-07-10) is the master background reference. The studio pose references in Drive (`Offie_photoshoot 1–5`, folder `1A9UJJcnlVA1Tvohd6Wa8O57eenCb7sQ2`) embody this standard and are used as the cloth/lighting base for studio generations. `Offie_photoshoot (1)` also shows the correct printed-logo placement/scale.
