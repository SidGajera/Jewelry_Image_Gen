# 07 — PROMPTS (reusable, export)

All prompts run on `nano_banana_2`, `resolution:"2k"`, `aspect_ratio:"1:1"`, `count:1`, medias `[reference, SOURCE]`. The logo is NEVER prompted to be drawn — studio prompts force clean cloth; the logo is composited locally afterward.

## CANONICAL BASE PROMPT (user-locked 2026-07-10) — core of every shot
> Preserve the exact ring design, stone shape, stone count, setting, prongs, band proportions and metal details from the source image.
> Use realistic VVS-quality lab-grown diamonds, accurate refraction, natural faceting, premium polished metal, luxury jewellery photography, sharp focus, clean background and commercial product-image quality.
> Do not redesign, simplify, add stones, remove stones, alter proportions, change the setting or modify the band.

Per shot, prepend an ANGLE/scene tag and append the group wrapper + the DESIGN string for the specific SKU. Keep the no-doubled-diamond clause. Everything 1:1, 2K.

## DESIGN STRING (fill per SKU — examples)
- **Generic three-stone:** "three-stone ring: [CENTER cut] diamond center held by [prong desc]; TWO [side stone] side stones ([color/cut, exact size/position]); [band] 18K yellow-gold band."
- **LR-0136:** "OVAL brilliant diamond center with double-claw prongs; TWO emerald-cut GREEN EMERALD side stones (keep GREEN, step cut, exact size/position, NOT diamonds); plain thin tapering 18K yellow-gold band, open cathedral gallery."
- **LR-0137:** "OVAL brilliant diamond center with double-claw prongs; TWO tapered BAGUETTE side diamonds (colorless, step-cut, horizontal, exact size/position); plain thin tapering 18K yellow-gold band."
Always add: "Preserve exact design, stone shape/count, setting, prongs, band proportions and metal; do not add/remove stones or alter proportions. Center diamond one natural facet pattern, no doubled/mirrored/CGI facets; every small stone crisp real facets, natural realistic light, no over-sparkle. Design 100% identical to source."

## STUDIO WRAPPER (clean cloth, NO logo — logo composited locally later)
> [ANGLE] studio product shot on plain pure-white cotton cloth, soft draping. IMPORTANT: absolutely NO logo, emblem, monogram, text or watermark anywhere on the cloth — clean plain white fabric only. Use the first image only for cloth and lighting; replace the ring with the second reference. [DESIGN STRING] PHYSICS: ring rests on real contact points under natural gravity — no floating/hovering/clipping/impossible balance; cloth folds have believable causes and compress only slightly under the ring's light weight; contact shadows exactly beneath the true contact points; ring rigid and undeformed. Identical lighting, exposure, reflections and neutral white balance across all studio shots. Ring tack-sharp, clean neutral-white background. 2K.

**Studio ANGLE tags — the 5 REQUIRED (see docs/12_STUDIO_ANGLES_STANDARD.md):** 1) Hero front straight-on view · 2) 45° left front view (center-stone depth, side stones, gallery, band, setting height) · 3) 45° right front view (other side of setting, band profile, craftsmanship) · 4) True side profile (basket, gallery, prongs, under-gallery, cathedral/hidden-halo if present, side-stone setting) · 5) Three-quarter perspective (top + side together, full architecture).

## LIFESTYLE WRAPPER (wider, worn)
> [ANGLE]. Cozy warm US-home scene from reference, natural hand five fingers natural skin wearing the ring. NO laptop, desk or office; NO logo or watermark anywhere; soft blurred home background. Replace the ring with the second reference. [DESIGN STRING] Ring tack-sharp, only background blurs. 2K.

**Lifestyle ANGLE tags:** Back of hand · On a cozy cream knit · On a light marble surface · Hand raised softly near face · Side of finger.

## CLOSE-UP WRAPPER (macro, cozy home)
> Macro close-up [angle], cozy warm US-home setting, soft blurred home background. NO logo, emblem or watermark; plain home setting. Replace the ring with the second reference. [DESIGN STRING] Ring tack-sharp. 2K.

**Close-up ANGLE tags:** Top-down detail · From the side of the finger · Held in fingertips.

## MEDIAS ORDER
`medias: [ { value: <pose/studio reference media_id>, role: "image" }, { value: <SOURCE ring media_id>, role: "image" } ]`
Prompt phrasing "Use the first image for cloth/scene; replace the ring with the second reference" matches this order.

## HARD DON'TS IN EVERY PROMPT
- Never instruct the model to render/keep/redraw the logo.
- Never allow laptop/desk/office in lifestyle.
- Never allow doubled/CGI/over-sparkle diamonds.
- Never change stone color/count/cut/setting from source.

## STUDIO WRAPPER v2 — LOGO PRESERVED ON CLOTH (in-model path, medias [branded-cloth, SOURCE, OFFICIAL-logo])
> [ANGLE] studio product view. Base = first image: KEEP the premium pure-white cloth AND the printed 'LUCENT CARAT LAB / FUTURE OF FINE JEWELRY' logo exactly — the logo is metallic gold ink printed INTO the fabric, following weave, folds, curvature, lighting and perspective (may be partially cropped or partly behind the ring; never floating/overlaid). Match the logo PIXEL-IDENTICAL to the THIRD reference (official logo): gold, exact icon/typography/spacing/stars/lines/tagline. Replace ONLY the ring with the second reference. [DESIGN STRING] Diamonds naturally bright, facets clearly visible, no blown-out white / no CGI glow. PHYSICS: ring stable on real contact points under gravity, cloth supports/compresses naturally, contact shadows beneath true contact points; no floating/clipping/impossible balance. Match reference camera height/distance/lens/FOV/exposure/white balance; do not brighten/darken. Ring tack-sharp. 1:1, 2K.

## LOGO-CORRECTION EDIT PROMPT (fix a drifted logo on an existing render; medias [render, OFFICIAL-logo])
> Keep the FIRST image exactly as-is (same ring, pose, cloth, folds, lighting, composition). ONLY correct the printed brand logo so it is PIXEL-IDENTICAL to the SECOND reference (official Lucent Carat Lab logo): metallic gold, exact icon/typography/stars/lines/tagline/spacing — nothing missing, no gray/black text, no font/icon changes. Logo is metallic gold ink printed INTO the cloth (follows folds/perspective/light; may be partly cropped/hidden; never floats). Neutral white balance. 2K.
