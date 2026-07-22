# 11 — MASTER BACKGROUND STANDARD (PERMANENT)

The approved reference images (round solitaire on white cloth with the printed Lucent Carat Lab logo) define the ONLY approved studio background. They are the permanent canonical reference for every future generation unless the user explicitly replaces them.

## NEVER AI-INVENT THE CLOTH (user-locked 2026-07-11, P3)
The background cloth is NEVER to be freely generated/invented by AI. It must reproduce the approved **premium white cotton** cloth from the reference/asset — same material, same premium quality, same natural soft draping — every time. The AI's only job is to keep that approved cloth faithful under the ring; it must not substitute a new, cheaper, flat, or differently-colored fabric. Two locked failures to never repeat:
- **Yellowish cloth:** cloth rendered cream/warm/yellow instead of neutral premium white → fix locally with `whiten_cloth.py` (0 credits); never accept a warm cast.
- **Simple/flat cloth:** cloth rendered plain, cheap, or texture-less instead of premium cotton with natural soft draping → cloth must always read as premium white cotton with soft, believable folds and fine grain, never a flat blank sheet.

## CLOTH MATERIAL — LOCKED (velvet preferred, user-locked 2026-07-21)
**PREFERRED DEFAULT: premium pure-white plush VELVET** (luxury jewelry-box velvet — soft dense pile, gentle sheen, elegant soft folds), per `docs/04 §0`. It reads more premium than cotton and is the default studio cloth. **Premium soft white cotton** (fine even grain, natural soft draping) remains acceptable as the alternate. Either way the material is LOCKED to one of these two premium options.
Do NOT replace it with: silk, satin, linen, cheap/generic cotton, marble, paper, leather, coarse visible-weave fabric, a flat plain sheet, or any other material. Use premium white velvet (preferred) or premium white cotton consistently across a catalog.

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
- cloth material changes (not the approved premium white cotton);
- cloth becomes yellowish or non-white (any warm/color cast);
- cloth looks flat, cheap, artificial, or overly simple.
Remedy: omit the logo rather than ship an inaccurate one; re-composite the exact logo to merge naturally; fix warm casts with `whiten_cloth.py` (0 credits); **automatically regenerate until all requirements are satisfied. NEVER return a studio image with an AI-generated logo** — the preserved official logo is the only acceptable logo for office/studio photoshoots.

## CACHING (cross-device / cross-session)
Cache and reuse these locked assets (logo + premium cotton cloth) across devices and sessions. Caching is byte-preserving only — it MUST NEVER alter image quality or asset fidelity. Verify against the manifest `locked_asset_checksums` before use; if a cached copy's checksum differs, discard it and restore from the repo.

## REFERENCE IMAGES
The user-provided reference set (round solitaire + pavé-shoulder solitaires on white cloth with printed logo, 2026-07-10) is the master background reference. The studio pose references in Drive (`Offie_photoshoot 1–5`, folder `1A9UJJcnlVA1Tvohd6Wa8O57eenCb7sQ2`) embody this standard and are used as the cloth/lighting base for studio generations. `Offie_photoshoot (1)` also shows the correct printed-logo placement/scale.
