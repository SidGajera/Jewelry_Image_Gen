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

### 3.1 MASTER DIAMOND PRESERVATION (CRITICAL — user-locked 2026-07-17)
Every diamond on the jewelry is a **locked asset**. The centre diamond is NOT the only reference — every diamond, regardless of position, preserves the same premium natural appearance.

**Applies equally to ALL diamonds:** centre · halo · shoulder · pavé · band · gallery · hidden halo · bridge · accent · prong-set · basket-set · every other diamond on the ring. **No diamond category may receive lower rendering quality.**

**Uniform diamond quality — every diamond preserves:** natural transparency · natural brilliance · natural scintillation · natural fire · natural facet definition · natural crown · natural table · natural girdle visibility · natural pavilion behaviour · correct optical depth · real diamond reflections. Every diamond must look like a real premium-cut laboratory-grown diamond photographed with a professional camera.

**Strictly prohibited — reject immediately if ANY secondary diamond appears:** flat · white dot · plastic · painted · milky · cloudy · overexposed · underexposed · blurry · low resolution · missing facets · artificial sparkle · different optical quality than the centre diamond · different material appearance. **Secondary diamonds must never look inferior to the centre stone.**

**Consistency:** all diamonds must appear to belong to the same ring and the same quality grade — consistent optical realism · brightness · contrast · facet sharpness · light return · reflection behaviour · diamond material response.

**DIAMOND OPTICAL REALISM (MANDATORY — user-locked 2026-07-17).** Every diamond must behave like a real natural or lab-grown diamond under the given camera angle.
**Never generate:** soft facets · milky appearance · plastic look · glass look · overexposed table · flat reflections · uniform sparkle · artificial white glow.
**Always generate:** sharp table · crisp crown facets · visible pavilion depth · high micro-contrast · natural brilliance · natural scintillation · physically correct light return · accurate optical symmetry · clean facet edges · real diamond transparency.
Brilliance and fire must be **angle-dependent**, never uniform; facet boundaries stay crisp; internal depth stays visible.

**On failure:** reject internally → record the failure in QUALITY_MEMORY (`07`) → regenerate.

**MASTER RULE:** a customer examining the image at 100% zoom must perceive EVERY visible diamond — centre, halo, shoulder, pavé, gallery, bridge or band — as a genuine premium-quality lab-grown diamond with the same natural realism and craftsmanship. **No diamond on the jewelry may appear to be a lower-quality AI approximation.**

## 4. GENERATION REQUIREMENT
Every prompt LEADS with the `CRITICAL REQUIREMENT — GEOMETRY LOCK` header (`prompts/07` canonical base prompt) — it goes first, before the angle/scene tag, because the model weights the prompt opening most. Source images are fed FIRST at max weight, medias `[reference, SOURCE]`. If any feature cannot be held exactly, do NOT invent/redesign — preserve the original geometry even at the cost of less dramatic lighting.

## 3.2 PRONG PRESERVATION (ZERO TOLERANCE — user-locked 2026-07-17)
The source CAD is the only authority. **Prong count is ABSOLUTELY LOCKED.**

**Never:** add extra prongs · remove prongs · split prongs · merge prongs · duplicate claw tips · create hidden support claws · create optical fake prongs · invent structural supports · change prong spacing · change prong height · change prong thickness · change claw shape · change claw orientation · change claw curvature · change claw angle · change prong seating · change diamond contact points.

**The render MUST contain EXACTLY the same number of prongs as the CAD.** CAD has 4 prongs → render exactly 4 · 6 prongs → exactly 6 · double prongs → exactly double prongs · V prongs → exactly V prongs. **Never reinterpret the setting. Changing prongs is a COMPLETE DESIGN FAILURE → reject and regenerate immediately.**

**Also preserved exactly:** prong positions · prong spacing · prong height · prong thickness · claw shape · claw orientation · basket geometry · gallery · head structure. **Never hide prongs due to an incorrect angle · merge two prongs into one · split one prong into two · invent additional claw tips · change the head geometry · modify the basket · reposition the prongs.**

**PRONG VALIDATION (before approving any render):** (1) count CAD prongs · (2) count rendered prongs · (3) counts must be identical · (4) verify every CAD prong is present in its correct location · (5) verify **no additional claw tips appear from perspective** (the classic side-view hallucination) · (6) verify the head and basket match the CAD exactly. **Any prong missing, added, merged or repositioned → REJECT · REGENERATE.**

**CAD AUTHORITY: the CAD always overrides previous renders, prompts or assumptions.**

## 4.1 D2D (DESIGN-TO-DESIGN) ACCURACY MODE (user-locked 2026-07-17 — mandatory before AND after every generation)
The source CAD is the ONLY MASTER; the generated jewelry must be an **exact geometric replica**. **Do not compare only visually — compare every structural component independently.**

**STEP 1 — BUILD MASTER DESIGN PROFILE (extract and lock):** overall silhouette · ring proportions · ring height · ring width · ring thickness · ring profile · band profile · band taper · shoulder geometry · shoulder crossover · infinity shape · open spaces · halo diameter · halo thickness · halo height · halo side profile · halo tilt · halo diamond count · halo diamond spacing · halo diamond size · halo diamond setting · head geometry · gallery geometry · basket geometry · bridge geometry · cathedral geometry · prongs (count · height · thickness · angle · tip shape) · centre diamond · centre diamond diameter · crown · pavilion · table · girdle · stone seating depth · pavilion visibility · side diamonds · shoulder diamonds · pavé diamonds · diamond count · diamond spacing · diamond alignment · diamond setting style. **Lock everything.**

**WHEN D2D RUNS:** analyse the source **pixel-by-pixel BEFORE** generation · compare the rendered jewelry against the source **CONTINUOUSLY DURING** generation · compare again **AFTER** generation before approval. **A generation is approved ONLY if the jewelry matches the source at D2D accuracy.** The task is never to generate a *similar* ring — it is to photograph the EXACT SAME manufactured ring.

**STEP 2 — GENERATE: render ONLY.** Never redesign · never beautify · never reinterpret · never optimise · never invent geometry · never reconstruct · never approximate. Treat the CAD as a manufactured ring; only create a realistic photograph of it.

**FULL LOCK LISTS (preserve EXACTLY):**
- **Geometry:** overall ring proportions · overall silhouette · ring profile · head height/width/depth · halo height/thickness/diameter/profile/curvature · centre diamond size/position/height/orientation/seating depth · pavilion visibility · crown visibility · table orientation · girdle visibility · basket · gallery · cathedral · bridge · shoulder geometry/thickness/curvature/taper/openings · split-shank geometry · infinity crossover geometry · shank thickness/width/profile · ring taper · metal flow.
- **Diamonds:** count · size · spacing · alignment · position · orientation · pavé path · pavé start point · pavé end point · pavé curvature · halo layout · shoulder layout · gallery layout · band layout · prong-set position. **Never** add or remove diamonds · increase or reduce size · change spacing · change pavé flow · change the setting style.
- **Prongs:** count · thickness · length · shape · angle · position · curvature · tip.
- **Metal:** gold volume · thickness · width · edges · curvature · transitions · polish.

**ABSOLUTELY FORBIDDEN:** beautify the CAD · improve proportions · smooth geometry · rebuild the head · reconstruct the halo · simplify the basket · change the shoulder flow · modify the infinity crossover · adjust metal thickness · reinterpret any structural feature · hallucinate geometry · replace CAD detail with AI assumptions · **slim or thicken the band · move the centre stone · raise or lower the head · smooth the cathedral · modify gallery proportions · change diamond spacing · stylise the faceting.**

**ADDITIONAL LOCKS (user-locked 2026-07-17, from the LR-0154 D2D pass):** band width · band thickness · cathedral height · cathedral curvature · gallery triangle geometry (corner sharpness + width) · gallery dimensions · head height · head position · basket geometry · centre diamond position and depth in the head · pavilion visibility · crown height · table orientation · prong count/thickness/positions/curvature · pavé start and end positions · pavé spacing · pavé count · pavé size · **pavé brightness** (never finer, more numerous or brighter than the CAD) · metal thickness · metal transitions.

**THE ONLY ALLOWED CHANGE IS THE CAMERA ANGLE** (plus lighting/background/environment/composition per the MASTER RULE below). **Jewelry accuracy outranks rendering quality.** If any CAD measurement differs visually from the source → reject the render internally and regenerate until the jewelry is visually indistinguishable from the CAD.

**FINAL CAD MATCH MODE — the last-mile drifts (user-locked 2026-07-17, from LR-0154 at 9.9/10).** Renders that pass a coarse check still fail here; check each explicitly: **shoulder thickness + shoulder taper** (AI leaves the cathedral shoulders fuller — they must taper more before reaching the head) · **gallery thickness** (the V-gallery beneath the centre stone renders thicker than the CAD line) · **prong profile** (renders rounder and heavier than the CAD) · **centre diamond seating depth** (renders a fraction high) · **pavé shared metal** (the CAD stones sit more RECESSED with more VISIBLE SHARED METAL). **Micro pavé must read as real flush-set diamonds with natural variation and visible shared metal — never enlarged, brightened, artificially enhanced or uniformly white.** Use physically accurate metal reflections only. Also locked per image: bridge geometry · head dimensions · basket dimensions · every curve and transition.

**STEP 3 — D2D COMPARISON (component-by-component against the CAD):**
- **Overall:** silhouette · proportions · height · width · thickness
- **Head:** head height · head width · head profile · head transition
- **Halo:** diameter · thickness · height · tilt · profile · diamond count · spacing · size
- **Centre stone:** diameter · shape · orientation · seating depth · pavilion visibility · crown · table · girdle
- **Prongs:** count · thickness · shape · position · contact points · angle
- **Shoulders:** width · curvature · flow · infinity geometry · crossover geometry · opening size · connection to halo
- **Pavé:** count · size · spacing · alignment · start position · end position · setting style
- **Band:** width · thickness · curvature · profile · taper
- **Gallery:** height · shape · curvature · basket · bridge · cathedral

**STEP 4 — TOLERANCE: 100% design match. Not 95%, not 98%, not 99% — 100%. Even the smallest structural deviation is unacceptable.**

**AUTOMATIC REJECTION if any of these change:** head height · halo thickness · halo diameter · shoulder geometry · infinity geometry · shoulder openings · shoulder curvature · pavilion visibility · stone seating · prongs · basket · gallery · cathedral · bridge · pavé path · pavé count · pavé spacing · band profile · band width · band thickness · ring proportions.

**D2D VALIDATION (compare the render directly with the source before approval):**
- [ ] same overall silhouette · [ ] same head assembly · [ ] same halo profile · [ ] same basket · [ ] same gallery · [ ] same bridge · [ ] same shoulder geometry · [ ] same infinity crossover · [ ] same split shank · [ ] same prongs · [ ] same centre stone · [ ] same pavilion visibility · [ ] same diamond count · [ ] same diamond size · [ ] same diamond spacing · [ ] same pavé layout · [ ] same metal thickness · [ ] same proportions

**Any structural difference → reject immediately · record the EXACT deviation in `07_QUALITY_MEMORY` · STRENGTHEN the prevention rule · regenerate.**

**FINAL VALIDATION — before delivery ask: "Is every visible structural element geometrically identical to the CAD?"** If NO → reject · update `07_QUALITY_MEMORY` · regenerate. **Repeat until every component matches the CAD exactly.**

**MASTER RULE:** treat the uploaded CAD as a **finished manufactured product**. The renderer is **not creating a new ring** and is **not allowed to redesign it** — it produces a photorealistic photograph of an already manufactured ring. The renderer may change ONLY: camera angle · camera distance · camera height · camera focal length · lighting · background · environment · composition. Everything else stays identical to the source. **Target: 100% D2D accuracy with zero geometric deviation.**

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
- [ ] MASTER DIAMOND PRESERVATION (§3.1) — centre natural · halo natural · shoulder natural · pavé natural · band natural · gallery natural · hidden-halo natural · every visible diamond has realistic facets · realistic brilliance · consistent optical quality with the centre stone (no flat/white-dot/plastic/milky/blown-out secondary stones)
- [ ] Gallery/basket/metal thickness match
- [ ] NO invented components (docs/16 detector): diamond_count, diamond_locations, gallery_structure, prong_count, hidden_halo_presence, pave_bridge_presence, metal_silhouette all match source — no added pavé bridge / hidden halo / gallery diamonds / extra prongs
- [ ] D2D ACCURACY MODE (§4.1) run component-by-component at 100% tolerance — overall / head / halo / centre stone / prongs / shoulders / pavé / band / gallery all geometrically identical to the CAD
- [ ] Only background/lighting/camera/focus/shadows/reflections changed — nothing structural
- [ ] Cloth = locked neutral-white cotton; logo (studio) physically printed, not an overlay
- [ ] 1:1, 2K

## 6. FAILURE → AUTO-FALLBACK (never ship a redesign)
Pure generation cannot guarantee 99.9% CAD fidelity — `nano_banana` biases toward the reference but re-synthesizes geometry. On ANY ✗, do not deliver and switch automatically (never ask which method), per `config/QUALITY_MEMORY.json geometry-immutable-auto-fallback`:
1. **FALLBACK 1** — composite the real source-ring pixels into the AI scene: `scripts/composite_ring_into_scene.py` (matches lighting/shadows/reflections/perspective/DoF). Pixel-exact geometry, 0 credits.
2. **FALLBACK 2** — if the requested camera angle is unreachable by compositing, render the exact geometry at that angle from the CAD file (when available), then composite onto cloth.

The composite runs where the render is downloadable (the user's machine / the `tool/` backend) — that is the point of the tool: it unblocks downloads so this fallback is automatic rather than manual.

## 7. RELATED
`docs/03 §A` (Design Preservation + Geometry Lock allow-list) · `prompts/07` (GEOMETRY LOCK header) · `config/QUALITY_MEMORY.json` (`geometry-immutable-auto-fallback`) · `docs/12_STUDIO_ANGLES_STANDARD.md` (angle rotation) · `scripts/composite_ring_into_scene.py`.
