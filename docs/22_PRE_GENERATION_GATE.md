# 22 — PRE-GENERATION GATE (PERMANENT, user-locked 2026-07-21)

**Scope.** This file is the single **mandatory checklist run before AND after every image generation**, for every catalog, image, session, and device. It CONSOLIDATES the locks that already live in the owning docs — it does not replace them; on any detail the owning doc wins (`docs/02`, `03`, `04`, `11`, `13`, `16`, `18`, `config/QUALITY_MEMORY.json`).

**Workflow is unchanged.** Use the existing Higgsfield image-generation workflow exactly as it is — do NOT change the workflow, provider, source-loading method, or generation lifecycle (`docs/21`). This gate operates *around* generation, never modifies it.

## 0. LOAD BEFORE GENERATING (all must be active)
Do not begin generation until all of these are loaded and enforced:
1. **MASTER_JEWELRY_PRESERVATION_POLICY** — `docs/13`, `docs/02`
2. **IMAGE_GENERATION_RULES** — `docs/03`
3. **LOGO_WORKFLOW** — `docs/04`
4. **QUALITY_MEMORY** — `config/QUALITY_MEMORY.json`
5. **FAILURE_MEMORY** — `config/QUALITY_MEMORY.json` (`failure_memory`)
6. **APPROVED_BENCHMARKS** — `config/deliveries/`, `workspace/golden/`

## 1. SOURCE LOCK
The source CAD is the ONLY source of truth. Never add, remove, redesign, reconstruct, improve, simplify, beautify, or invent any jewelry detail. Preserve exactly:
- Overall ring geometry; silhouette and proportions
- Band width and thickness
- Every curve, bend, taper, narrowing, widening, and profile
- Head, basket, gallery, bridge, cathedral, and setting
- Center diamond shape, size, proportions, orientation, crown, table, pavilion, position
- Side-diamond count, size, spacing, orientation, placement
- Pavé count, size, spacing, coverage
- Prong count, shape, thickness, angle, length, position
- Metal thickness, structure, curves, finish

Never add or remove prongs. Never add extra diamonds, metal, supports, decorations, halos, bridges, gallery elements, or head details. Never make the band wider or thinner than the source. If the source HAS a bend/taper/curve/narrowing/widening, preserve it exactly; if it does NOT, never invent one. **Only the camera angle may change.**

## 2. LOGO LOCK
Use only the official preserved Lucent Carat Lab logo (`assets/logo/logo_official.png`). Preserve exactly: diamond icon, typography, gold colour, black tagline, gradients, kerning, spacing, alignment, line thickness, scale ratio, layout.
- **"LUCENT CARAT LAB" must remain GOLD.**
- **"FUTURE OF FINE JEWELRY" must remain BLACK. Never recolour the tagline to gold.**
- Never redraw, regenerate, restyle, approximate, distort, simplify, or replace the logo. (It may be softened only by real depth-of-field blur — focus/brightness only, never colour or design; `config/QUALITY_MEMORY.json#jewelry-hero-logo-soft-secondary`, `#logo-color-lock-black-tagline`.)
- Must look naturally printed into the cloth fibres, following folds and weave.
- Never allow: fake logo · missing logo · multiple logos · sticker look · floating overlay · white box · glow · shadow behind the logo · artificial embossing · wrong perspective · wrong opacity · wrong placement · a logo that ignores cloth folds/weave.

## 3. CLOTH LOCK
Use only premium pure neutral-white cotton cloth: fine realistic cotton weave, soft natural sheen, elegant natural folds, soft daylight, real cloth shadows, neutral colourless appearance. Never: plain/cheap cloth · grey/cream/ivory/beige/yellow/pink/red/blue/orange cloth · any colored lighting or colour cast · artificial fabric texture. Final image must have natural, colour-neutral lighting.

## 4. PERMANENT FAILURE MEMORY
Every rejected mistake is recorded automatically (`config/QUALITY_MEMORY.json` schema): exact failure, cause, prevention rule, catalog/SKU, image angle, repeat count, corrected result when approved. Before every generation, load all recorded failures and prevent recurrence. Never duplicate a record — increment `repeat_count` and append to `occurrences`.

**Permanent blocked failures:** wrong logo · missing logo · gold tagline instead of black · artificial logo printing · wrong cloth · colored cloth · plain low-quality cloth · colored lighting / colour cast · wrong prong count · extra prongs · missing prongs · wrong prong shape or position · extra diamonds · missing diamonds · wrong diamond size/position/orientation/spacing · added head details · added gold or metal in the head · changed basket/gallery/bridge/cathedral/setting · band too wide or too thin · missing source bend or taper · invented bend or taper · changed ring proportions · any geometry not present in the source.

## 5. GENERATION GATE
**Before sending the request:** confirm the correct 4-view CAD is loaded; confirm the official logo is loaded; confirm the cached Design Profile matches the source; add all relevant Failure Memory restrictions to the compact prompt; keep the Higgsfield workflow unchanged.

**After generation:** compare jewelry vs the source CAD; logo vs the official benchmark; cloth vs the approved white-cotton benchmark; output vs every recorded failure.

**If any mismatch:** reject internally → record the failure → regenerate → never deliver the failed image. Do NOT claim success merely because generation completed (`docs/21` §8).

**Deliver ONLY when:** jewelry matches source · diamonds match source · prongs match source · band width and all bends match source · head and setting match source · logo matches the official asset · tagline remains black · cloth is premium pure white cotton · lighting is natural and colour-neutral · no recorded failure is repeated.

> **Environment note.** Where a session cannot fetch the rendered output (e.g. a sandbox whose proxy blocks the CDN), the after-generation visual comparison is performed by the operator / via the Drive read-back loop (`config/QUALITY_MEMORY.json#drive-readback-verify-loop`); never mark a shot verified without an actual comparison. The guaranteed logo fix is the local composite (`scripts/print_logo_on_cloth.py`), run where the render is downloadable.

**These rules are permanent for every catalog, image, session, and device.**
