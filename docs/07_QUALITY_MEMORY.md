# 07 — QUALITY MEMORY

> **AUTHORITATIVE OWNER (see `00` POLICY INDEX):** this doc + `config/QUALITY_MEMORY.json` own ALL Failure Memory and Quality Memory (every rejection + prevention rule). `14` no-regression routes here. Append new failures here; never start a parallel memory.

Dedicated memory layer for continuous improvement. Machine-readable store: [`config/QUALITY_MEMORY.json`](../config/QUALITY_MEMORY.json) — this file is its structure and rules. Loaded before EVERY generation (docs/03 generation order, step 2).

## Catalog 0152 — COMPLETE REJECTION · FAILURE MEMORY 001–010 (2026-07-17)
**Not an image-quality problem — a geometry-preservation problem.** Logo printing, cloth, lighting and realism all passed; **CAD preservation failed, and that alone is a zero-tolerance rejection.**

| Category | Result |
|---|---|
| CAD preservation | ❌ Fail |
| Geometry preservation | ❌ Fail |
| Camera accuracy | ❌ Fail |
| Side-angle accuracy | ❌ Fail |
| Head preservation | ❌ Fail |
| Diamond preservation | ⚠ Partial |
| Lifestyle | ⚠ Acceptable, geometry still altered |
| Logo printing | ✅ Good |
| Cloth | ✅ Good |

**Observed:** ring rebuilt (shoulders thicker/thinner, curvature changed, head wider and taller, shank profile changed, drifting cathedral, head transition changed) · **every** side angle reconstructed rather than rotated · rear view changed gallery, negative spaces, gallery/head thickness and prong merge points · prongs drifted in thickness, claw profile, tip size, curvature and merge position · the diamond moved (higher/lower, more/less crown and pavilion exposure) · the head was made "prettier" instead of preserved · **the camera rotated correctly but the jewelry changed too — two different things** · lifestyle rings not always identical to CAD · band thickness, shoulder width and metal volume varied.

**Root cause:** the workflow still treats the CAD as a **reference image**. It must treat the CAD as the **master object**. Mental model for every render: *"The jewelry already exists. My only job is to move the camera, lighting, background and environment. I have zero permission to modify even one vertex of the jewelry."*

**FAILURE MEMORY (locked):**
- **001 Geometry reconstruction** — never reconstruct any portion of the ring; preserve exact CAD geometry.
- **002 Side-view hallucination** — never invent hidden geometry for side/rear views; use only geometry proven by the source CAD.
- **003 Head drift** — head geometry is locked: height, width, curvature, transition.
- **004 Prong drift** — prong count, spacing, curvature, thickness, merge points and tip shape are immutable.
- **005 Band drift** — band width, thickness, curvature and silhouette identical.
- **006 Diamond drift** — never move, resize, rotate, expose or reposition the centre stone.
- **007 Gallery drift** — gallery openings, bridges, baskets and negative spaces are locked.
- **008 Camera-only rule** — changing viewpoint must never change the jewelry; only the virtual camera moves.
- **009 CAD authority** — the CAD is the single source of truth; studio renders, previous outputs and AI assumptions never override it.
- **010 Product-photographer mode** — behave as a photographer, not a designer; if preserving the CAD exactly is impossible for a requested angle, reject and shoot the nearest valid angle instead of inventing geometry.

## COMPLETED CATALOGS — CONSOLIDATED LEARNING (2026-07-17)
**Done:** LR-0151 · LR-0149 · LR-0154 · LR-0155 · LR-0156. **Parked:** LR-0150 (see its section below).

**What made these catalogs pass — reuse it:**
1. **Photograph, never rebuild.** Every prompt leads with FINAL CAD MATCH MODE: the CAD is an already-manufactured object; only camera, lighting, environment and composition may change. Concept-level similarity is a rejection (`13 §4.1`).
2. **Component-by-component D2D, not a visual glance.** Build the master design profile, render, then compare overall / head / halo / centre stone / prongs / shoulders / pavé / band / gallery at **100% tolerance**. The last-mile drifts repeat on every SKU: shoulders left fuller, gallery lines thickened, prongs rounded and heavied, centre stone lifted, pavé rendered finer and brighter with the shared metal lost.
3. **Prong count is the single most-broken lock** (`13 §3.2`). LR-0155 dropped 6→4 on the front view; side views hallucinate extra claw tips. Count them in the CAD, count them in the render, every image.
4. **One approval per catalog works.** Iterate Image 1 until approved, lock it as the master theme, then auto-batch the rest against it — cloth, printed logo, lighting, white balance, exposure and 18K gold tone all inherited.
5. **Cloth + logo are assets, not renders.** The master cotton persists across the whole catalog; the logo is small secondary branding printed INTO the weave (`04 §14.1`, `§14.2` benchmark, `11` OFFICE PHOTOSHOOT PRIORITY). Over-correcting the print into ragged edges is worse than a slightly clean one.
6. **Realism is the acceptance bar, not a style** (`03` PHOTOREALISM POLICY): angle-dependent diamond optics with crisp facets and visible pavilion depth (`13 §3.1`), real cloth compression and ambient occlusion under the ring, real-world imperfections.
7. **Lifestyle = one home, one model, jewelry first** (`03` HOUSE LIFESTYLE + MODEL REALISM).
8. **Source discipline:** SKU main folder only, gold set by default, reuse `media_id`s, never re-upload (`03` PERMISSION POLICY). Golden CADs live in `workspace/golden/<SKU>/`.

**Every rejection this round was geometry or asset fidelity — never composition or lighting.** That is where the next catalog's scrutiny belongs.

## Approved Benchmarks
- Approved jewelry renders
- Approved logo benchmark
- Approved cloth benchmark
- Approved lighting benchmark
- Approved camera benchmark

## Failure Memory
- Jewelry failures
- Physics & logical failures
- Logo failures
- Cloth failures
- Lighting failures
- Camera failures
- Logo placement & catalog composition failures

### CATEGORY AUTO-REJECTS (user-locked 2026-07-20 — non-ring SKUs)
Applies to every bracelet / necklace / earring catalog. Detail + preservation blocks: `20` §9.

| Category | Auto-reject if |
|---|---|
| Bracelet | clasp missing or type changed · link count differs from spec |
| Necklace | chain style changed · drop length visually inconsistent with spec |
| Earring | **only one earring rendered** · the two are not mirror-accurate · backing type wrong |
| All | try-on body part wrong for the category (finger on a bracelet, wrist on a necklace, etc.) |

**Root cause this prevents:** a ring preservation block applied to a non-ring SKU tells the model to preserve prongs, gallery, basket and shank on a product that has none — which invites hallucination rather than suppressing it. `BRACELET.json` inherited ring settings exactly this way; its delivered images were built on ring geometry rules and are queued for re-render. **Never fall back to the ring template on an unknown category — fail loudly** (`20` §9.3).

### FM-0163 / FM-0164 — Ref-text leak & band artifacts (LR-0162, 2026-07-18)
- **FM-0163 — Internal reference text/IDs in the image.** The rear render engraved "REF1=LR-0162" on the band. *Prevent:* never render prompts, IDs, reference labels, watermarks, hidden annotations or metadata into any image; OCR-check before delivery — if any readable text other than the official Lucent Carat Lab logo appears, reject (see `03` NO TEXT / NO WATERMARK, `04` §14.1d).
- **FM-0164 — Band reflection/phantom-geometry artifact.** Unnatural reflection/geometry artifact on the lower-inside of the band. *Prevent:* the band is one continuous clean 18K gold surface with physically correct reflections only; inspect the full band at ~200% zoom and reject any dents, seams, folds, duplicated edges, warped reflections or phantom geometry on the metal.

### Catalog 0159 — Logo Overlay · Cloth Drift · Geometry Simplification · CGI Feel — REJECTED (2026-07-18)
Four permanent entries (strengthen existing Design-Preservation / Cloth `11` / Logo `04` 14.1b / Photorealism `03` policies — not new policies):
- **F1 Logo overlay** — logo rendered as a separate graphic layer, not embedded print. *Prevent:* reject any image where the logo reads as visually independent of the fabric; the print must inherit weave, wrinkles, lighting, shadows and fibre texture. Root fix pending user decision (in-model can't guarantee embed; local composite is the reliable path).
- **F2 Cloth quality drift** — generic white fabric with a slight grey cast and coarse repetitive weave instead of premium luxury bright-white cotton. *Prevent:* lock cloth globally to the premium bright-white benchmark; reject any colour/texture drift (`11` CLOTH VALIDATION).
- **F3 Geometry drift** — rear gallery, prongs (thicker, more rounded tips, altered spacing), shoulder transitions and pavé layout subtly reinterpreted vs CAD. *Prevent:* part-by-part CAD comparison before approval; any structural deviation, however small, → reject and regenerate.
- **F4 AI simplification** — fine CAD detail (support bars, gallery elements, band-width transitions, pavé bead consistency) smoothed into generic geometry. *Prevent:* preserve every visible CAD edge/transition/support bar/gallery/setting detail exactly; no smoothing, approximation or reinterpretation.
Also: gold lacked environmental reflections, edges mathematically perfect, weak contact shadow / minimal cloth compression → CGI feel (`03` PHOTOREALISM MASTER).

### Catalog 0150 — Head & Shank Geometry Drift — REJECTED (2026-07-17)
**Reference:** approved Image 1 (hero front) = the locked jewelry benchmark for Catalog 0150.

**Observed errors in the rejected output:** centre diamond enlarged · halo diameter enlarged · head wider and heavier · centre-stone-to-halo proportion differs · halo diamond size/spacing/arrangement altered · twisted split-shank geometry changed · shank crossing points don't match · open spaces inside the twisted shoulders differently shaped · left/right shoulder curves inconsistent · head-to-shank connection altered · ring balance and silhouette no longer match.

**Locked approved benchmark** — every future 0150 image preserves exactly: centre diamond size and proportion · halo diameter and thickness · halo diamond count, size, spacing and placement · four-prong position and shape · twisted split-shank curves · shoulder crossing locations · open-space geometry within both shoulders · head-to-shank connection · overall silhouette and proportions. **Only camera angle, ring orientation and natural photographic composition may change.**

**Prevention rule — before delivering every 0150 image:** (1) compare directly against approved Image 1 · (2) check centre-stone and halo scale · (3) trace BOTH twisted shoulders head→shank · (4) compare every crossing point and open space · (5) confirm the complete silhouette matches · (6) reject if any geometry is enlarged, simplified, shifted or reinterpreted. **The engine must PHOTOGRAPH the exact approved 0150 ring — never generate a similar twisted halo ring.**

**No-repeat rule:** the enlarged centre stone, enlarged halo and modified twisted-shank geometry must never appear again; any future 0150 output repeating them is rejected automatically before delivery.

### Catalog 0154 — D2D Last-Mile Drift — REJECTED (2026-07-17, v3 → v5)
The renders reached 9.2 → 9.7 → 9.9/10 and were still rejected. **A near-miss is a rejection.** The drifts the engine repeats on every pass, in the order they were caught:

**v3 (9.2/10):** band width — shoulders slimmer than the CAD, especially the upper half · shoulder pavé — finer, more numerous and brighter than the CAD · cathedral curvature softened, head reads more open · head height marginally raised · gallery triangle corners rounded and the triangle widened · centre stone raised above the basket · faceting more stylised than the CAD.

**v4 (9.7/10):** lower shank still thicker and rounder than the CAD cross-section · pavé still finer and brighter · cathedral→head transition still smoother than the CAD · centre stone still fractionally raised.

**v5 (9.9/10):** cathedral shoulders still fuller — must taper more before the head · micro pavé still too bright and too uniformly white (CAD stones sit more recessed with more **visible shared metal**) · V-gallery beneath the centre stone still thicker than the CAD line · prongs still rounder and heavier than the CAD profile · centre diamond still seated a fraction high · cloth carried a subtle warm cast · the over-distressed logo print was *worse* than the previous cleaner one.

**Prevention:** run `13 §4.1` D2D ACCURACY MODE → STRICT CAD MATCH → **FINAL CAD MATCH MODE** (the last-mile list) on every render, then `03 §G` FINAL REALISM VALIDATION. **Only the camera position may change. Jewelry accuracy outranks rendering quality.**

### Catalog 0154 — Vector Logo · Logo Too Prominent · Cloth Master Changed — REJECTED (2026-07-17, v2)
**Failure 1 — digital logo appearance.** *Cause:* logo rendered as a clean vector overlay (edges too sharp, gold lines too clean/uniform, ink not blending into the weave, uniform brightness). *Prevention:* treat the logo as **real screen-printed ink embedded into** the preserved premium white cotton — the ink inherits cloth weave · fiber texture · fold deformation · shadow density · highlight rolloff · slight ink diffusion, and its density varies subtly across highlights and shadows. **Never render the logo as a perfectly sharp vector graphic.**

**Failure 2 — logo too prominent.** *Cause:* the logo competes with the jewelry. *Prevention:* **the jewelry is always the primary subject**; the printed logo is secondary branding — subtle, modest in scale, naturally integrated, never dominating the composition.

**Failure 3 — cloth master changed.** *Cause:* the background cloth differs from the approved master (different weave, inconsistent sheen, different fold pattern). *Prevention:* office photoshoots **always reuse the exact preserved premium white cotton**. Do not generate a new cloth texture, weave, sheen or fold style per image — the same master cloth persists across the entire catalog.

### Catalog 0154 — Artificial Logo + Cloth Deviation — REJECTED (2026-07-17)
**Failure 1 — artificial logo appearance.** *Cause:* logo appears digitally overlaid instead of physically printed (unnaturally crisp edges, no interaction with the weave, flat uniform opacity, no inherited micro-shadows or lighting variation). *Prevention:* the official logo must behave as **real screen-printed ink on premium white cotton** — ink follows fabric weave, folds, wrinkles, stretching, shadows and highlights; micro fabric texture stays visible **through** the ink. **No overlay, sticker, floating, embossing or vector appearance.** (Owner: `04 §14`.)

**Failure 2 — cloth inconsistency.** *Cause:* fabric deviates from the approved premium white cotton (grey/beige cast, flat appearance, canvas-like weave, insufficient sheen). *Prevention:* every office photoshoot uses the **exact same preserved premium white cotton**; colour stays pure neutral white — no beige, cream, grey, blue, pink, yellow or warm cast; weave, sheen and texture stay consistent across the catalog. (Owner: `11` OFFICE PHOTOSHOOT PRIORITY.)

**Failure 3 — logo detached from fabric.** *Cause:* the logo does not inherit cloth physics. *Prevention:* the print must **deform with the cloth** — compress, stretch and bend with every fold; ink density varies naturally with the fabric surface.

**Priority rule:** the cloth is a LOCKED MASTER ASSET and the logo is a LOCKED PRINTED ASSET. **If either deviates from the approved benchmark → reject before delivery and regenerate.**

### Catalog 0150 — PARKED (2026-07-17)
**Status:** paused by the user after repeated geometry rejections — *"will start at the end of all catalog."* **Do not resume LR-0150 until every other catalog is complete.**

**Approved and locked:** Image 1 / hero front (job `ebdfc118-ca4a-4d62-80b7-c054b77f1f8c`) = the jewelry benchmark for this SKU. Source CAD: `workspace/golden/LR-0150/r91_2|4|8.jpg`.

**Standing conclusion:** on this design the prompt path holds the concept but rebuilds the structure (head height, halo profile, gallery windows, crossover curvature, pavé scale, stone seating). All three failure sections below apply on resume; run `13 §4.1` D2D ACCURACY MODE at 100% tolerance, and prefer the composite pipeline (`15`) where geometry must be guaranteed by construction rather than by prompt.

### Catalog 0150 — Side Profile Head & Gallery Reconstruction — REJECTED (2026-07-17)
**Root cause:** the generator preserved the overall **concept** but **reinterpreted** the head assembly and shoulder structure instead of rendering the exact CAD geometry. **Concept-level similarity is not a pass.**

**Observed errors:** **head assembly** — source has a taller head, more open gallery, greater halo↔shoulder distance and slimmer support members; output compressed the head vertically, compacted the gallery, lowered the halo and thickened the supports · **halo** — source thin profile with a distinct side profile and uniform outer edge; output thicker with a rounded side wall and larger visual mass · **gallery** — source long triangular supports with larger open triangular windows and thin members; output shorter supports, smaller openings, thicker metal · **shoulder** — source long flowing crossover with strong curvature and narrow metal between the pavé rows; output shortened the crossover, softened the curvature, thickened the metal · **pavé** — source smaller diamonds, more spacing, narrower path; output larger diamonds, wider path, changed gold borders · **centre stone** — source higher seating with more pavilion visible; output lower seating, less pavilion · **overall** — the side profile reads shorter and heavier than the source.

**Prevention rule — before final approval preserve exactly:** overall silhouette · head height · halo height · halo thickness · halo diameter · gallery shape · gallery openings · support angles · basket geometry · stone seating height · pavilion visibility · shoulder curvature · shoulder crossover geometry · shoulder openings · metal thickness · pavé path · pavé count · pavé spacing · pavé diameter. **Any structural difference → reject immediately · update QUALITY_MEMORY · regenerate.**

**MASTER RULE:** the source is a **finished manufactured product**; the renderer creates a photograph of that exact product and must **never reconstruct, reinterpret, optimise, beautify or approximate** the jewelry geometry. (See `13 §4.1` D2D ACCURACY MODE.)

### Catalog 0150 — Side Angle Design Substitution — REJECTED (2026-07-17)
**Observed failure:** the side-angle output abandoned the CAD entirely — the ring became an eternity-style twisted openwork band with the halo tipped flat toward the camera and the head/cathedral rise, gallery and split-shank structure gone. A total design substitution, not a drift.

**Root cause:** the engine re-synthesised a "similar" ring for an unfamiliar viewpoint instead of photographing the locked CAD object; comparison was holistic rather than component-by-component.

**Prevention:** run **D2D ACCURACY MODE** (`13 §4.1`) before and after every generation at **100% tolerance** — build the master design profile from the CAD, render only, then compare overall / head / halo / centre stone / prongs / shoulders / pavé / band / gallery component-by-component. Any deviation → reject · record · regenerate.

### Catalog 0150 — CAD Structural Drift — REJECTED (2026-07-17)
**Reference:** the source CAD (side profile). **Camera angle was acceptable — the failure is jewelry geometry, not viewpoint.**

**Observed errors:** (1) **head height** — source head sits higher above the shoulder with more vertical clearance below the halo; output head sits lower, halo closer to the shoulders · (2) **halo profile** — source halo thinner with a flatter side profile; output thicker with a deeper side wall · (3) **shoulder connection** — source infinity shoulder meets the halo in a smooth flowing transition with a larger open space; output joins differently, open space reduced, transition thicker · (4) **pavé path** — source shoulder pavé follows the exact outer edge with uniform spacing; output path shifted, spacing differs, shoulder curvature differs · (5) **centre stone seating** — source diamond sits slightly higher with more pavilion visibility; output diamond sits deeper inside the halo · (6) **band profile** — source split shank has stronger curvature; output flatter.

**Correction rule — before rendering, compare the generated jewelry against the CAD at the STRUCTURAL level and lock:** head height · halo thickness · halo diameter · halo profile (side-wall depth) · shoulder geometry · shoulder openings · shoulder curvature · shoulder-to-head connection · split-shank geometry · pavé path · pavé spacing · pavé count · stone seating depth · gallery height · basket profile · overall proportions. **Any difference → reject internally · update QUALITY_MEMORY · regenerate.**

**MASTER RULE:** the renderer must treat the CAD as a **finished manufactured ring**. It may change ONLY camera angle · camera distance · lighting · background · environment. **It must never reinterpret or rebuild the jewelry geometry, even if the resulting render appears aesthetically pleasing.**

### Logo Placement & Catalog Composition — REJECTED (2026-07-17)
**Observed failure:** the ring was positioned directly over the printed logo, hiding a significant portion of it; only the lower part of the logo remained visible, making the branding look incomplete.

**Root cause:** the composition prioritised ring centring without validating complete logo visibility; the framing did not reserve sufficient space for the full printed logo beneath the jewelry.

**Prevention rule (before finalising composition):** predict the ring footprint · predict the logo footprint · ensure the ring does NOT cover the primary logo · reposition the ring or camera if necessary · keep the complete printed logo naturally visible. **The logo may be partially cropped only by the IMAGE BOUNDARY, never by the jewelry itself.**

**Composition validation (before approval):**
- [ ] Complete logo visible · [ ] diamond icon visible · [ ] "LUCENT" fully visible · [ ] "CARAT LAB" fully visible · [ ] tagline visible unless intentionally cropped by the image edge · [ ] ring does not overlap the printed logo · [ ] logo remains naturally printed on the cloth · [ ] composition looks like a real product photoshoot

**Expected result:** the jewelry remains the primary subject while the official printed logo is fully readable and naturally integrated into the same cloth — the logo enhances the composition without competing with, or being obscured by, the ring.

**Learning:** future office photoshoots must automatically reserve adequate space for the complete printed logo during camera composition. If the logo is obscured by the ring → reject · record · regenerate with corrected framing. (Owner detail: `04` LOGO COMPLETENESS VALIDATION.)

## Learning Rules
- Every rejected image automatically records:
  - Failure
  - Cause
  - Prevention Rule
- Every future generation loads this file before generation.
- Previously recorded failures must never repeat.
- Approved benchmark images become the new reference standard.

## Continuous Learning System (user-locked 2026-07-17)
The system must continuously improve from every rejected image so that identical or substantially similar mistakes never recur.

**Automatic failure recording** — whenever an image is rejected, automatically record: failure category · affected component · root cause · violated policy · prevention rule · validation rule · correct expected behaviour. **No rejected image is discarded without updating QUALITY_MEMORY.**

**Pre-generation learning** — before EVERY new generation: load the complete QUALITY_MEMORY · apply every previously recorded prevention rule · validate the new image against every historical failure before delivery.

**Duplicate failure prevention** — compare each new image against ALL previously recorded failures. If a similar failure is detected: reject immediately · do not deliver · apply the recorded prevention rule · regenerate automatically. **The same failure must never require manual reporting twice.**

**Learning priority** — previously recorded failures outrank generation preferences. Proactively prevent known mistakes instead of repeating them.

**Regression prevention** — every successful correction becomes part of QUALITY_MEMORY. Future generations preserve successful corrections while preventing previous failures. **No solved issue may reappear.** (See `14_NO_REGRESSION_POLICY`.)

**Per-decision recording (user-locked 2026-07-17)** — for EVERY approval, correction or rejection record: result (Approved / Rejected) · successful element · failure or requested change · root cause · prevention rule · correct expected result · applicable policy section. Never create duplicate rules — merge a learning into the existing relevant policy only when it creates a permanent generation requirement (`17` POLICY MERGE RULE).

**Per-catalog learning chain** — each subsequent image must learn from: successes of previously approved images · failures of rejected images · user corrections · existing Failure Memory · Approved Benchmarks.

**FINAL CATALOG LEARNING (after a catalog is fully approved)** — review all successful images · review all rejected images · consolidate duplicate learnings · store final successes as **Approved Benchmarks** · store final failures + prevention rules here · preserve only permanent, reusable learnings · never rewrite or duplicate locked policies. Only then are commits/pushes made (`03` GIT RULE, `15`).

**MASTER LEARNING RULE** — image quality must improve continuously throughout the project. Every rejection makes the system more accurate; every approved image strengthens the approved benchmark; every future generation must show measurable improvement by avoiding all previously solved mistakes. **A mistake already identified, corrected and recorded must not appear again unless the user explicitly changes the source design or requirements.**
