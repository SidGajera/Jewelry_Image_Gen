# 13 — JEWELRY PRESERVATION SPECIFICATION (single source for CAD-fidelity generation + QA)

> **SINGLE AUTHORITY — MASTER JEWELRY PRESERVATION POLICY (user-locked 2026-07-17).**
> This is the ONE file for jewelry preservation. Nothing else may define, restate or soften these rules.
> **MANDATORY: load this file before EVERY image generation** and check the output against it before delivery.
> Subordinate files that reference these rules but never redefine them: `docs/16` (zero invention — a subset of §MASTER),
> `docs/02` P1/P2 (priority order only), `docs/14` (regression checklist — enforcement, not definition),
> `prompts/07` (per-shot prompt text). On ANY conflict, THIS FILE WINS.

User-locked 2026-07-16, after three consecutive SKUs (twist-halo split-shank; round-halo twist-shank ×2) generated attractive but **redesigned** rings. The prompt rules reduce drift; this spec + the composite fallback are what actually guarantee fidelity. This is the one place that consolidates the geometry-lock requirement and the pre-accept QA checklist — the generation prompt (`prompts/07`) and the auto-QC (`config/QUALITY_MEMORY.json geometry-immutable-auto-fallback`) both point here.

## 1. PRINCIPLE
The source render/CAD is the **master, immutable object**. The AI's only job is to place that exact ring into a realistic scene. A catalog image is a *product visualization* of the SAME physical ring in a new setting — **never a reinterpreted design**. This applies equally to studio, lifestyle, and close-up shots.

## 2. WHAT MAY CHANGE (the entire allow-list — nothing else)
- Background / environment (locked premium white VELVET cloth for studio — cotton acceptable; docs/11, docs/04 §0)
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

## 3b. DIAMOND LENGTH-TO-WIDTH RATIO REFERENCE (user-locked 2026-07-21)

Standard L:W ranges per cut, for future image generation and QA. **The SOURCE CAD's actual measured ratio ALWAYS governs** — reproduce the source exactly. Use this table two ways: (1) when the source's own ratio is known/visible, match it; (2) as a sanity-check to CATCH SHAPE DRIFT (e.g. an oval rendered too round, an elongated hexagon rendered squat, a marquise not pointed enough). If a render's stone falls outside the source's shape/ratio, it is a geometry FAILURE → regenerate.

| Cut | L:W range | Ideal |
|---|---|---|
| Round | 1.00 | 1.00 (perfect circle) |
| Oval | 1.33–1.66 | 1.4–1.5 (elegant elongated) |
| Emerald | 1.30–1.60 | 1.4 (classic rectangular step-cut) |
| Pear (teardrop) | 1.45–1.75 | 1.5–1.6 |
| Marquise | 1.75–2.25 | 1.9–2.1 (sharp pointed ends) |
| Cushion (square) | 1.00–1.20 | — |
| Cushion (rectangular) | 1.15–1.30 | — |
| Princess | 1.00–1.05 | near-perfect square |
| Radiant (square) | 1.00–1.05 | — |
| Radiant (rectangular) | 1.20–1.40 | — |
| Asscher | 1.00–1.05 | octagonal square, emerald-like corners |
| Heart | 0.90–1.10 | 1.00 (symmetrical lobes) |

Note: elongated hexagon / elongated step-cuts follow their source's own ratio (e.g. LR-0193/0194 hexagons ≈ 2:1, ~13×6.5mm) — the source measurement wins over any generic range.

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

## PRE-GENERATION GATE (mandatory, user-locked 2026-07-17)

**This file is the ONLY authoritative policy for image generation. No generation may begin until it has been loaded and enforced.**

Before EVERY generation, in order:
1. Load and validate this policy.
2. Load all recorded Failure Memory (`config/QUALITY_MEMORY.json` → `failure_memory` + `fixes`).
3. Apply every applicable rule and corrective instruction **before** the request is sent.
4. Reject any generation that violates this policy — internally, before delivery.
5. Learn every approved/rejected result automatically: record it, increment repeat counts, never re-record duplicates, never repeat a known mistake.

Mandatory for **every image, every SKU, every session, every device.** Never bypass, ignore, replace or partially apply it. Partial application is a violation.

**Enforcement note.** Step 4 is not discretionary QC (which `docs/18` suspends) — it is policy enforcement, and it stays active. Step 3 constrains the *request*; it cannot constrain what the renderer returns. Where the model reconstructs geometry despite a compliant request, step 4 rejects the output — that is the gate working, and the reject is not a prompt defect to be re-tried indefinitely. See the recorded structural finding above.

## RULES 31–40 — REAR / SIDE / PER-ANGLE STRUCTURE (user-locked 2026-07-17)

Targets the failures still appearing in back and side views.

31. **Back/profile view must exactly match the source CAD. Never reconstruct the rear geometry.**
32. Preserve **basket height, gallery height and head proportions** exactly.
33. Preserve the **cathedral shoulder angle and thickness** exactly.
34. Preserve the **bridge geometry** exactly — never add, remove, thicken or simplify bridge supports.
35. Preserve the **under-gallery opening and spacing** exactly.
36. Preserve the **centre-stone seating height** exactly.
37. Preserve the **ring silhouette from every viewing angle** — front, side, back, 45°, top.
38. **Never mirror, symmetrize or "correct" the CAD geometry.**
39. **Every generated angle must be verified against the corresponding source view before delivery.**
40. If any structural detail differs from the source CAD: **automatically reject and regenerate** under this policy.

**Rule 38 and the LR-0151 45R shot.** `scripts/_recut_and_composite_0151.py` builds 45R by horizontally mirroring the 45L cut. For a symmetric round solitaire that preserves geometry, but it IS a mirror — rule 38 forbids it. Produce 45R from its own source view, not by flipping.

**Rule 31/39 and the source.** `97.png` carries four views. An angle with no corresponding source view cannot be verified under rule 39, and generating it would reconstruct rear geometry under rule 31. Where the catalog needs an angle the CAD does not cover, obtain that view (more CAD renders, or the 3D model — `97.3dm` / `97.stl` sit beside `97.png` in Drive) rather than letting the model invent it. A missing image is preferable to invented geometry.

**Rule 40 and the recorded evidence.** Rules 31–37 all constrain geometry the model *re-synthesises* on every render. `QUALITY_MEMORY` → `lr0151-inmodel-geometry-drift` (repeat_count 6) records seven prompt formulations producing seven different drifts, several of them exactly these items — head/gallery proportions, cathedral profile, under-gallery structure. Rule 40 therefore rejects every in-model render by construction; it is satisfiable only by compositing the source pixels.
