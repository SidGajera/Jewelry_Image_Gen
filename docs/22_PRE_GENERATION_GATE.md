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

## 0a. JEWELRY PRIORITY & FOCUS HIERARCHY (MANDATORY, user-locked 2026-07-21)
The jewelry is ALWAYS the primary subject. Every image must draw the viewer's eye to the jewelry before anything else, and the jewelry stays the **sharpest, brightest, highest-detail** object in the scene. The logo, cloth and background exist ONLY to support it.

**Focus hierarchy (strict):** 1 Jewelry → 2 Diamond → 3 Logo → 4 Cloth → 5 Background. Never let the logo or cloth compete with the jewelry.

**Keep perfectly sharp:** jewelry, diamond, prongs, pavé — maximum micro-detail and the highest local contrast on the **jewelry only**.

**Logo depth of field:** when the logo sits close to or behind the jewelry, keep it naturally out of focus per real camera DoF — blur subtle and physically realistic, the jewelry always sharper. The logo must NEVER be the visual focus. Even blurred, preserve EXACTLY its geometry, typography, diamond icon, GOLD colour, BLACK tagline, kerning, alignment, layout, line thickness, spacing, perspective. Blur may never change, distort, stretch, recolour, regenerate, or simplify the logo — it must read as a real printed logo falling outside the focal plane (§2).

**Cloth:** naturally soft and secondary; never let cloth texture, folds, highlights, or logo printing dominate the jewelry (§3).

**REJECT if:** the logo attracts more attention than the jewelry · the cloth attracts more attention than the jewelry · the logo is sharper than the jewelry · the logo blur changes its design/colour/typography/tagline · the jewelry is not the primary visual focus.

**LIFESTYLE SCENE VARIETY (user-locked 2026-07-21).** Every lifestyle / house-lifestyle / closeup-lifestyle frame must be a DISTINCT scene — vary surface, prop, palette, camera and light; **never reuse the same surface+prop+palette (e.g. raw-silk + dried baby's breath + warm-autumn) across frames**, and use different lifestyle scenes than the previous SKU. Reject any lifestyle frame that looks the same as another (`config/QUALITY_MEMORY.json#lifestyle-scene-variety`, `#natural-photography-angle-variety`).

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
**PRIMARY METHOD — LOGO IS GENERATED IN-MODEL BY HIGGSFIELD ONLY (user-locked 2026-07-21, supersedes the earlier local-composite method).** `scripts/print_logo_on_cloth.py` is **NOT used** (the user found it makes too many mistakes) — do not call it. For studio/packaging shots, render the logo **in-scene by Higgsfield**, passing the official logo artwork (`assets/logo/logo_official.png`) as a reference, and hold it to the full quality lock below by strong prompting + QC + regenerate-on-failure. REQUIRED in-model: exact two-tone (gold emblem + "LUCENT CARAT LAB", **BLACK** "FUTURE OF FINE JEWELRY" tagline), EXACTLY ONE logo, printed into the cloth (follows weave/folds/light, no overlay/sticker/glow/box/independent-shadow), **no background diamond-outline / wireframe / line-art anywhere**, jewelry stays the sharp hero with the logo softened only by real DoF (never a colour/design change). If any of these fail, REJECT and regenerate. The rules below define what the in-model logo must satisfy.

Use only the official preserved Lucent Carat Lab logo (`assets/logo/logo_official.png`). Preserve exactly: diamond icon, typography, gold colour, black tagline, gradients, kerning, spacing, alignment, line thickness, scale ratio, layout.
- **"LUCENT CARAT LAB" must remain GOLD.**
- **"FUTURE OF FINE JEWELRY" must remain BLACK. Never recolour the tagline to gold.**
- Never redraw, regenerate, restyle, approximate, distort, simplify, or replace the logo. (It may be softened only by real depth-of-field blur — focus/brightness only, never colour or design; `config/QUALITY_MEMORY.json#jewelry-hero-logo-soft-secondary`, `#logo-color-lock-black-tagline`.)
- Must look naturally printed into the cloth fibres, following folds and weave.
- Never allow: fake logo · missing logo · multiple logos · sticker look · floating overlay · white box · glow · shadow behind the logo · artificial embossing · wrong perspective · wrong opacity · wrong placement · a logo that ignores cloth folds/weave.

**Print integration (ZERO TOLERANCE, user-locked 2026-07-21).** The logo must appear as a REAL physical print INSIDE the premium white cotton — never digitally overlaid. It must: be absorbed into the cotton fibres; follow every wrinkle, fold and the fabric weave; receive the IDENTICAL lighting, shadows, highlights and perspective as the cloth; look printed during fabric manufacturing. It must NEVER appear to sit on top of the cloth. **Reject immediately if:** letters appear above the cloth · text ignores cloth folds · text stays perfectly flat while the cloth bends · logo edges are too sharp vs the cloth texture · logo looks pasted/sticker-like · logo has its own lighting · logo has its own shadow.

**Exactly ONE logo (ZERO TOLERANCE).** Exactly ONE official Lucent Carat Lab logo is allowed. Never generate a second logo, partial duplicate, background logo, watermark logo, ghost logo, the diamond icon repeated elsewhere, duplicate typography, or extra decorative logo elements. If more than one logo (or a duplicated logo element) appears anywhere in the image, reject automatically.

**Logo final validation — REJECT if:** the logo is not fully merged into the cloth · the logo appears digitally overlaid · multiple logos exist · any logo element is duplicated · the cloth and logo appear to be separate layers.

> In-model diffusion cannot guarantee true print-into-fibre integration; if a render fails these checks after retries, fall back to the local composite (`scripts/print_logo_on_cloth.py`), which enforces fold displacement, weave-through, matched lighting and ink diffusion (`config/QUALITY_MEMORY.json#printed-logo-fabric-realism`).

## 3. CLOTH LOCK (premium benchmark, ZERO TOLERANCE, user-locked 2026-07-21)
The cloth is a LOCKED visual asset. Always use the approved premium benchmark: premium luxury white COTTON, fine high-thread-count weave, soft natural sheen, dense cotton texture, elegant natural folds, soft daylight illumination, natural contact shadows, studio-quality fabric, pure neutral white (RGB-neutral), premium luxury product-photography quality — it must instantly read as expensive jewelry-display fabric.
- **Never generate:** cheap · plain · flat · thin · synthetic · rough · low-quality-weave · muslin-like · bed-sheet · paper-like · smooth-CGI · plastic-looking fabric.
- **Never allow:** grey/yellow/cream/ivory/beige cloth · blue/pink/green tint · warm or cold colour cast. Final lighting stays natural and colour-neutral.

**LOGO IS MANDATORY ON EVERY STUDIO IMAGE (user-locked 2026-07-21).** Never deliver jewelry on plain cloth and never deliver a studio image without the logo. The logo is rendered **in-model by Higgsfield** (§2 primary method) and must read as physically printed into the fabric (fibres/weave/folds/perspective, identical lighting+shadows as the cloth), a single exact instance. Reject if: no logo · plain cloth delivered · logo pasted/floating/detached/sticker-like · gold tagline · duplicate/background-wireframe logo · cloth does not match the benchmark. On any failure, regenerate on Higgsfield (the local composite is not used).

## 4. PERMANENT FAILURE MEMORY
Every rejected mistake is recorded automatically (`config/QUALITY_MEMORY.json` schema): exact failure, cause, prevention rule, catalog/SKU, image angle, repeat count, corrected result when approved. Before every generation, load all recorded failures and prevent recurrence. Never duplicate a record — increment `repeat_count` and append to `occurrences`.

**Permanent blocked failures:** wrong logo · missing logo · gold tagline instead of black · artificial logo printing · logo digitally overlaid / not merged into cloth · multiple or duplicated logos / repeated logo elements · wrong cloth · colored cloth · plain low-quality cloth · colored lighting / colour cast · wrong prong count · extra prongs · missing prongs · wrong prong shape or position · extra diamonds · missing diamonds · wrong diamond size/position/orientation/spacing · added head details · added gold or metal in the head · changed basket/gallery/bridge/cathedral/setting · band too wide or too thin · missing source bend or taper · invented bend or taper · changed ring proportions · any geometry not present in the source.

## 5. GENERATION GATE
**Before sending the request:** confirm the correct 4-view CAD is loaded; confirm the official logo is loaded; confirm the cached Design Profile matches the source; add all relevant Failure Memory restrictions to the compact prompt; keep the Higgsfield workflow unchanged.

**After generation:** compare jewelry vs the source CAD; logo vs the official benchmark; cloth vs the approved white-cotton benchmark; output vs every recorded failure.

**If any mismatch:** reject internally → record the failure → regenerate → never deliver the failed image. Do NOT claim success merely because generation completed (`docs/21` §8).

**Deliver ONLY when:** jewelry matches source · diamonds match source · prongs match source · band width and all bends match source · head and setting match source · logo matches the official asset · tagline remains black · cloth is premium pure white cotton · lighting is natural and colour-neutral · **the jewelry is the primary visual focus and sharper than the logo/cloth (§0a)** · no recorded failure is repeated.

> **Environment note.** Where a session cannot fetch the rendered output (e.g. a sandbox whose proxy blocks the CDN), the after-generation visual comparison is performed by the operator / via the Drive read-back loop (`config/QUALITY_MEMORY.json#drive-readback-verify-loop`); never mark a shot verified without an actual comparison. The guaranteed logo fix is the local composite (`scripts/print_logo_on_cloth.py`), run where the render is downloadable.

**These rules are permanent for every catalog, image, session, and device.**
