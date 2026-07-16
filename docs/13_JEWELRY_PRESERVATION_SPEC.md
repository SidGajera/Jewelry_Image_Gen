# 13 — JEWELRY PRESERVATION SPECIFICATION (single source for CAD-fidelity generation + QA)

User-locked 2026-07-16, after three consecutive SKUs (twist-halo split-shank; round-halo twist-shank ×2) generated attractive but **redesigned** rings. The prompt rules reduce drift; this spec + the composite fallback are what actually guarantee fidelity. This is the one place that consolidates the geometry-lock requirement and the pre-accept QA checklist — the generation prompt (`prompts/07`) and the auto-QC (`config/QUALITY_MEMORY.json geometry-immutable-auto-fallback`) both point here.

## 1. PRINCIPLE
The source render/CAD is the **master, immutable object**. The AI's only job is to place that exact ring into a realistic scene. A catalog image is a *product visualization* of the SAME physical ring in a new setting — **never a reinterpreted design**. This applies equally to studio, lifestyle, and close-up shots.

## 2. WHAT MAY CHANGE (the entire allow-list — nothing else)
- Background / environment (locked premium white cotton cloth for studio)
- Lighting
- Camera angle + position
- Focus / depth of field
- Shadows
- Reflections

## 3. WHAT MUST STAY 100% IDENTICAL (CAD-level fidelity; target 99.9%)
- Overall silhouette + ring proportions + left/right symmetry
- Center halo geometry — exact halo **shape** (a round halo stays perfectly circular; never cushion / rounded-square) + halo **diameter** + halo **thickness** + halo **stone count**
- Center-stone diameter + crown/table proportions + orientation
- Prong count + shape + positions
- Band width + thickness + cross-section
- Infinity/twist/crossover side-loop geometry + the open **negative-space** openings between strands
- Shoulder curvature + shoulder→halo transition
- Pavé layout + spacing + stone size + start/end positions
- Stone count · stone size · stone orientation (every stone: center, halo, side, pavé)
- Gallery / basket / cathedral profile
- Metal thickness everywhere
- Full diamond cut anatomy per stone (see `docs/03 §L` GEOMETRY LOCK): L:W ratio, table, crown, pavilion, girdle, culet, facet layout/count, symmetry — same physical stone from every angle.

## 4. GENERATION REQUIREMENT
Every prompt LEADS with the `CRITICAL REQUIREMENT — GEOMETRY LOCK` header (`prompts/07` canonical base prompt) — it goes first, before the angle/scene tag, because the model weights the prompt opening most. Source images are fed FIRST at max weight, medias `[reference, SOURCE]`. If any feature cannot be held exactly, do NOT invent/redesign — preserve the original geometry even at the cost of less dramatic lighting.

## 5. PRE-ACCEPT QA CHECKLIST (run every image against the source BEFORE accepting)
Compare the render to the source, feature by feature. Any ✗ = FAIL → do not deliver → auto-fallback (§6).
- [ ] Overall silhouette + proportions match (not wider/thicker/heavier)
- [ ] Halo shape identical (round stays round) + halo diameter + thickness + stone count match
- [ ] Center stone: same size relative to halo, same crown/table balance, same orientation
- [ ] Prongs: same count, shape, thickness, positions
- [ ] Band: same width + thickness
- [ ] Twist/infinity loops: same curve, same negative-space openings, same symmetry
- [ ] Shoulder→halo transition matches
- [ ] Pavé: same count, size, spacing, start/end positions
- [ ] Every stone: count/size/orientation match; diamonds are real-optics VVS/IF (no CGI/doubling/over-whitening)
- [ ] Gallery/basket/metal thickness match
- [ ] NO invented components (docs/16 detector): diamond_count, diamond_locations, gallery_structure, prong_count, hidden_halo_presence, pave_bridge_presence, metal_silhouette all match source — no added pavé bridge / hidden halo / gallery diamonds / extra prongs
- [ ] Only background/lighting/camera/focus/shadows/reflections changed — nothing structural
- [ ] Cloth = locked neutral-white cotton; logo (studio) physically printed, not an overlay
- [ ] 1:1, 2K

## 6. FAILURE → AUTO-FALLBACK (never ship a redesign)
Pure generation cannot guarantee 99.9% CAD fidelity — the production model biases toward the reference but re-synthesizes geometry. On ANY ✗, do not deliver and switch automatically (never ask which method), per `config/QUALITY_MEMORY.json geometry-immutable-auto-fallback`:
1. **FALLBACK 1** — composite the real source-ring pixels into the AI scene: `scripts/composite_ring_into_scene.py` (matches lighting/shadows/reflections/perspective/DoF). Pixel-exact geometry, 0 credits.
2. **FALLBACK 2** — if the requested camera angle is unreachable by compositing, render the exact geometry at that angle from the CAD file (when available), then composite onto cloth.

The composite runs where the render is downloadable (the user's machine / the `tool/` backend) — that is the point of the tool: it unblocks downloads so this fallback is automatic rather than manual.

## 7. RELATED
`docs/03 §A` (Design Preservation + Geometry Lock allow-list) · `prompts/07` (GEOMETRY LOCK header) · `config/QUALITY_MEMORY.json` (`geometry-immutable-auto-fallback`) · `docs/12_STUDIO_ANGLES_STANDARD.md` (angle rotation) · `scripts/composite_ring_into_scene.py`.

## MASTER JEWELRY PRESERVATION POLICY (P0 — HIGHEST PRIORITY, user-locked 2026-07-17)

**The source jewelry is the ONLY source of truth. The mission is NOT to generate a new ring — it is to faithfully reproduce the existing ring in a different scene.**

**ZERO GEOMETRY MODIFICATION.** AI may never redesign, reconstruct, infer, repair, optimize, enhance or approximate any part of the jewelry. The source is a LOCKED OBJECT.

No changes to: centre stone · side stones · diamond count/size/spacing/orientation/position · prongs (count/thickness/angle/position) · head · gallery · basket · cathedral · bridge · halo · hidden halo · under-gallery · setting · band · shank · shoulders · pavé · metal thickness · ring proportions · silhouette · profile · every visible component. **Even a tiny change is a FAILURE.**

Only these may change: camera angle · camera distance · camera rotation · lighting · background · cloth · scene · environment.

**SOURCE FIRST.** Study the source before generating. Never guess, never fill missing details, never invent geometry. If uncertain: COPY THE SOURCE.

**QUALITY RULE.** Accuracy over realism. Geometry over aesthetics. Source fidelity over creativity. On any conflict, **THE SOURCE IMAGE ALWAYS WINS.**

**This policy overrides every prompt, workflow, model behavior, optimization and generation strategy.**

### WHAT THIS MEANS IN PRACTICE (recorded 2026-07-17)
"Reconstruct" is what a diffusion model *does*. Asked to render the ring, it re-synthesises it — that is the mechanism, not a tuning error. Verified on LR-0151: **seven prompt formulations, seven different drifts** (gallery/head, cathedral profile, prong thickness and angle, centre-stone proportions, pavé spacing and count, band thickness, overall proportions). See `config/QUALITY_MEMORY.json` → `lr0151-inmodel-geometry-drift`, repeat_count 6+.

Therefore **this policy cannot be satisfied by any pipeline in which the model draws the ring.** "Reproduce the existing ring in a different scene" has exactly one implementation: the source-CAD pixels are **composited** into a generated scene (`composite-v1`, `scripts/composite_ring_into_scene.py`), where geometry is identical *by construction* rather than by instruction.

Because this policy overrides workflow, it and `active: legacy` (`docs/15` §0) are incompatible. Resolving that requires the explicit authorization sentence in `docs/21` §1a — this file does not switch the pipeline by itself, but it makes clear that the current pipeline cannot honour it.
