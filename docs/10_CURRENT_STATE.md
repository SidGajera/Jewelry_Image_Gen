# 10 — CURRENT STATE (exact current workflow)

As of 2026-07-11 (v1.3.2). This is precisely what happens for a new SKU today.

**Context loading:** startup loads ONLY `CLAUDE_SETUP.md`; lazy-load one file per task (§1 map). Normal generation loads the runtime trio (`config/project_manifest.json` + `prompts/07_PROMPTS.md` + `config/QUALITY_MEMORY.json`) — self-sufficient, identical output.

## PER-SKU WORKFLOW (current, exact)
1. **Locate source:** `search_files` in source parent for `title contains '<SKU#>'` → get the SKU folder → list its images. **MAIN FOLDER ONLY (user-locked 2026-07-16):** use only the images directly in the SKU's main folder; NEVER descend into subfolders (e.g. a "photo and video" subfolder) for source images without the user's explicit permission. **GOLD BY DEFAULT (user-locked 2026-07-16):** when the SKU has renders in multiple metal colors (gold / rose / white / "Model G"), default to the GOLD version as the source unless the user specifies another metal.
2. **Study the ring:** `download_file_content` on the top view (and one side view) → decode base64 to PNG locally → view. Identify: center cut, side stones (type/color/cut/count), prongs, band, metal, gallery. Use the CORRECT file; ignore strays.
3. **Log the design** in `LUCENT_MASTER.md` (§14 product codes) + `docs/06_CACHE.md`.
4. **Import source** once: `media_import_url("https://drive.google.com/uc?id=<SRC_ID>&export=download")` → source media_id.
5. **References:**
   - Studio: reuse the 5 branded `Offie_photoshoot` refs (re-import from Drive IDs if media_ids expired).
   - Lifestyle + closeup: import DIFFERENT pose files than the previous SKU (from `Reference_US_Ring` + `Closup_houselifestyle`).
6. **Two-phase catalog approval (user-locked 2026-07-16 — see "CATALOG APPROVAL WORKFLOW" below):** generate ONLY Image 1 first → user reviews → collect corrections → regenerate Image 1 → repeat until the user EXPLICITLY approves Image 1. Then generate ALL remaining images for that catalog in ONE automatic batch under the Image-1 lock — no further approval per image. `generate_image`, `model:"the production model"`, `resolution:"2k"`, `aspect_ratio:"1:1"`, `count:1`, medias `[reference, source]`. Prompts = canonical base + group wrapper + SKU design string (docs/07). **Studio prompts force clean cloth with NO logo.**
7. **Report count only.** No preview tools.
8. **Local post-processing (user runs on downloaded outputs, 0 credits):**
   - `whiten_cloth.py` if any cloth drifted warm.
   - `scripts/print_logo_on_cloth.py` on the 5 studio shots to print the locked logo onto the cloth.
9. **Deliver** to Drive Output folder; update tracking log.

## CATALOG APPROVAL WORKFLOW (user-locked 2026-07-16 — MANDATORY)
Each catalog is independent. A catalog begins whenever a new jewelry design (new SKU / source ring) is loaded.

**STEP 1 — FIRST IMAGE.** Generate ONLY Image 1 for the current catalog. Wait for the user's review. Collect every correction, regenerate Image 1, and repeat until the user EXPLICITLY approves Image 1. Do NOT generate any other image for this catalog until Image 1 is approved.

**STEP 2 — CATALOG LOCK.** Once Image 1 is approved, treat it as the MASTER QUALITY STANDARD for this catalog. Freeze every approved property: jewelry geometry, diamond size/orientation/position, stone count, stone shape, prongs, halo, gallery, band width, metal thickness, camera quality, lighting, cloth, logo placement, logo print quality, and the QC rules. These are locked for the rest of the catalog.

**STEP 3 — AUTOMATIC GENERATION.** Automatically generate all remaining required images for the same catalog in one run. Do NOT stop after each image. Do NOT ask for approval again unless a CRITICAL error is detected. Apply every correction learned from the approved Image 1; never repeat a mistake already corrected.

**STEP 4 — NEW CATALOG.** When a different jewelry design / SKU is loaded, RESET this workflow: generate only Image 1 for the new catalog, wait for approval, then auto-generate the rest.

**MANDATORY:** exactly ONE approval image per catalog. Never require approval for every image. Never generate the remaining catalog before Image 1 is approved. The approved Image 1 is the permanent reference standard for every remaining image in that catalog. (Consistent with CLAUDE_SETUP §2.5/§5 "one verification image, then batch" and docs/17 Master Token Policy — the verification image is a full-quality final, not a draft.)

## KEY DECISIONS IN FORCE
- Logo: NEVER AI-rendered; ALWAYS composited from `assets/logo/logo_official.png` to look printed on cloth (P0).
- Cloth: locked material + neutral white; consistent every image (P3).
- Jewelry: 100 % identical to source (P1). Diamonds: single facet pattern, no doubling (P2).
- Format: 1:1, 2K always (P5).
- Lifestyle: cozy US-home, no laptop/desk (P6).
- Efficiency: reuse cache, batch, no previews, compact full-quality prompts (P7).

## GENERATION MECHANICS / GOTCHAS
- `generate_image` requires `params.model` and (for 2K) explicit `params.resolution:"2k"` — default is 1k.
- Response may show an internal routing alias for the multi-image edit path; that is expected — `resolution:"2k"` is what governs quality/credits.
- Higgsfield outputs live on CloudFront and are network-blocked for us to download; the user downloads them and runs the local scripts.
- `media_id`s expire across sessions → re-import from Drive IDs.

## PROGRESS
- Repo `SidGajera/Claude_Lucent_Image_Gen` live (private, `main`), documentation exported.
- Latest SKUs: LR-0156, LR-0136, LR-0137. (Full history in `LUCENT_MASTER.md`.)

## OPEN / NEXT
- Continue new SKUs on request ("go for 0XXX folder").
- For studio shots, apply the printed-logo composite locally after download (the 5 studio shots of LR-0137 were generated logo-free and await the local logo print).


## v1.2.0 UPDATE (2026-07-10)
- Studio logo path in practice: because Claude cannot download Higgsfield CDN renders here, studio shots are generated with the branded reference's printed logo PRESERVED in-model, optionally passing `assets/logo/logo_official.png` as a 3rd reference for pixel-exact match; drifted logos are fixed with the logo-correction edit prompt (prompts/07). The local `print_logo_on_cloth.py` composite stays the pixel-perfect route wherever the render is downloadable.
- Locked this cycle: diamond realism, photography/reference consistency (fixed camera height/distance/lens/exposure/WB), plain-or-folded cloth, natural per-shot variation, pixel-identical logo, physical-scene consistency, repository-maintenance/file-ownership.
- LR-0137 office set (5 angles) generated with logo preserved on cloth.

## MANDATORY IMAGE GENERATION FLOW (8 steps, user-locked 2026-07-17)

The execution sequence for every image. Each step **references** its owning policy and never restates it.

**1. POLICY LOAD (mandatory).** Load `docs/13` (Master Jewelry Preservation — single authority), `config/QUALITY_MEMORY.json` (all failures + approved patterns), `docs/14` (No Regression). **Abort generation if any policy fails to load.**

**2. SOURCE VALIDATION.** Verify: correct 4-view CAD (`97.png` for LR-0151), official preserved logo, correct SKU, correct angle. **Never substitute another source.**

**3. GEOMETRY LOCK** (per `docs/13`). Lock centre diamond · all side diamonds · prongs · basket/gallery · cathedral · bridge · band · proportions · silhouette. **Nothing may change except the camera.**

**4. LOGO LOCK** (per `docs/04`, benchmark at §9). Official preserved logo only · printed into cloth · correct perspective · correct fold deformation · correct opacity · correct scale · entire logo visible.

**5. CLOTH LOCK** (per `docs/11`). Approved white cloth · natural folds · logo integrated into the fabric · no blank cloth · no floating logo.

**6. CAMERA LOCK.** Only camera angle, distance and rotation may change. Nothing else.

**7. FAILURE MEMORY CHECK.** Compare against every recorded failure before generating: geometry drift · diamond drift · prong drift · band drift · cathedral drift · logo missing · logo floating · wrong cloth · wrong lighting · wrong proportions. If a known failure would recur, regenerate before delivery.

**8. FINAL VERIFICATION.** Compare the output against: source CAD · Jewelry Preservation Policy · Failure Memory · approved logo benchmark (`docs/04` §9). **Deliver only if all pass.**

### WHERE THIS FLOW CURRENTLY BREAKS (recorded 2026-07-17)
Steps 3 and 8 are unsatisfiable while the model draws the ring. Step 3 locks geometry in the *request*; the renderer re-synthesises the ring regardless, so step 8 rejects the output. Verified: seven prompt formulations, seven distinct drifts (`QUALITY_MEMORY` → `lr0151-inmodel-geometry-drift`, repeat_count 6).

Step 3 becomes a real lock — rather than a request — only when the source-CAD pixels are composited into the generated scene. Same for step 4: the approved logo benchmark (`docs/04` §9) is reproduced by the local composite at `--scale 0.28-0.34 --opacity 0.45-0.6 --displace 6-8 --soften 1.0`; an in-model logo has never passed it.

The flow above is correct and stays as written. What it needs is a pipeline in which steps 3 and 4 are enforceable by construction (`docs/15` §0, `docs/21` §1a).
