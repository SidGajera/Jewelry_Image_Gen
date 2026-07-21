# 23 — HIGGSFIELD PRODUCTION EXECUTION POLICY (PERMANENT, user-locked 2026-07-21)

The permanent execution wrapper around production image generation. Consolidates the locks in the owning docs (they win on any detail) and adds the **response contract**. Use the existing Higgsfield MCP pipeline permanently — never redesign, replace, migrate, experiment with, or automatically change the workflow, provider, source-loading method, prompt lifecycle, model-routing, media order, resolution, aspect ratio, or production characteristics.

## 1. MANDATORY STARTUP (load & enforce before every generation)
`docs/03` Image-Generation Rules · `docs/04` Logo Workflow · `docs/11` Background Standard · `docs/12` Studio Angles · `docs/13` Master Jewelry Preservation · `docs/14` No-Regression · `docs/16` Zero Jewelry Invention · `docs/17` Master Token Policy · `docs/18` Zero-Tolerance QC · `docs/19` Zero-Confirmation · `docs/20` Zero Internal Output · `docs/21` Higgsfield Engine Lock · `docs/22` Pre-Generation Gate · `config/QUALITY_MEMORY.json` (QUALITY_MEMORY + FAILURE_MEMORY) · Approved Benchmarks (`config/deliveries/`, `workspace/golden/`) · Cached Design Profile (`docs/06`).
If any mandatory policy or asset is unavailable, **stop with one concise verified error.**

## 2. SOURCE & DESIGN LOCK
Use the correct catalog **four-view CAD** as the authoritative source. Never substitute: a single-view image when the 4-view CAD exists · a model/lifestyle image as CAD · another SKU · another catalog · an older design profile. The cached Design Profile must match the current source. Never add, remove, resize, rotate, reposition, reinterpret, improve, simplify, or reconstruct any stone (center/side/pavé — count, size, spacing, position, orientation, crown, table, pavilion, proportions), prongs (count/shape/thickness/angle/length/placement), head/basket/gallery/bridge/cathedral/halo/hidden-halo/setting/supports/under-gallery, or band (width/thickness/taper/bends/curvature/profile/proportions/silhouette/metal volume), or any structural/decorative detail. **Only the requested camera angle may change** (full detail: `docs/13`, `docs/16`, `docs/22` §1).

## 3. HIGGSFIELD EXECUTION
Generate only through the approved Higgsfield MCP production flow. Never ask the user to choose provider, model, pipeline, upload method, media workflow, fallback, or recovery method. Do not switch away from Higgsfield even after failure — recover **inside** the Higgsfield workflow, retry once when appropriate; if it still fails, stop with the verified Higgsfield error (`docs/21`).

## 4. LOGO & CLOTH
Exactly ONE official preserved logo (`assets/logo/logo_official.png`); preserve diamond icon, typography, layout, kerning, alignment, line thickness, gold colours/gradients, the BLACK tagline "FUTURE OF FINE JEWELRY", scale ratio, spacing. Logo looks naturally printed into premium pure neutral-white cotton (follows weave, folds, perspective, lighting, blur, occlusion) — rendered **in-model by Higgsfield only** (user-locked 2026-07-21; `print_logo_on_cloth.py` not used), held exact by prompt + QC + regenerate (`docs/04` method override, `docs/22` §2). Never allow: missing/duplicate/recreated/modified logo · gold tagline · floating/pasted/sticker/watermark/embossed/glowing/boxed logo · independent logo shadow · logo competing with the jewelry · cheap/plain/synthetic/tinted/coloured/grey/cream/beige/pink/blue/yellow cloth. **Jewelry is always the primary focus**; a logo near the jewelry gets only natural DoF blur, never a colour/design change (`docs/22` §0a, §2, §3).

## 5. NO-REGRESSION ENFORCEMENT
Before generation, load every recorded failure and append all relevant prevention rules to the compact prompt. After generation, compare against source CAD · Design Profile · Master Jewelry Preservation · official logo benchmark · approved cloth benchmark · approved images · every recorded failure. Auto-reject any repeat of a known issue (geometry drift · wrong diamond/prongs · extra/missing stones · added head/gallery/bridge/setting/metal · wrong band width/taper/bend/proportions · wrong/missing/duplicate/artificial logo · wrong cloth/colour cast · jewelry not primary focus · repeated camera angle · a previously approved image being regenerated/modified). Record each NEW rejection (catalog + angle, exact failure, cause, prevention rule, repeat count, corrected pattern when available); never duplicate a record — increment `repeat_count` (`docs/14`, `config/QUALITY_MEMORY.json`).

## 6. CATALOG LIFECYCLE
Per new catalog: (1) generate Image 1 only; (2) wait for approval/correction; (3) apply corrections to Image 1 until approved; (4) after approval, automatically generate the remaining required angles; (5) never regenerate or modify approved images; (6) never repeat the same angle unless explicitly requested (`docs/10`, `CLAUDE.md` §4).

## 7. OUTPUT STABILITY
New instructions may improve quality, caching, QC, portability, recovery, and token efficiency ONLY — never reduce output quality or alter the Higgsfield lifecycle. Approved outputs are the minimum quality baseline; every new catalog must be equal-or-better. If a change makes results worse, immediately revert to the last approved working behaviour while preserving all validated learning and Failure Memory (`docs/14`, `docs/17`).

## 8. RESPONSE POLICY (user-locked 2026-07-21)
**Execute silently.** Do not narrate or show reasoning, validation, planning, previews, model names, routing details, or debugging. Do not repeatedly ask for confirmation when the required source and instructions already exist (`docs/19`, `docs/20`). Visible responses are **no more than three short lines**. For a generation run, the visible response is:

```
Generating...
```
then
```
Done.
```
or, on failure:
```
Stopped: <verified concise error>.
```

> Harness note: in a CLI/agent surface the harness itself surfaces tool activity (commands, generation calls); that is the harness, not narration. This policy governs Claude's own visible text — keep it to the ≤3-line contract above; it does not require (or enable) suppressing harness-rendered tool rows.

These rules are permanent for every catalog, image, session, and device.
