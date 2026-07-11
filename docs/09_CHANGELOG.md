# 09 — CHANGELOG

## v1.3.20 — 2026-07-11 (fake-gem + moody-lighting guard)
- **Modified:** docs/03_IMAGE_GENERATION_RULES.md (§L fake-gem forbidden list, §E lighting character), config/QUALITY_MEMORY.json (fake-gem-and-moody-lighting fix), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Captured the net-new bits of the LUXURY JEWELRY PRODUCT LOCK not already covered: every stone must read as a premium natural-looking lab-grown diamond, never CZ/moissanite/glass/plastic/acrylic/artificial-crystal/CGI-gem; lighting must be neutral daylight/luxury studio (soft shadows, clean highlights, neutral WB), never yellow/orange/blue/blackish/dark/warm-indoor/cinematic/dramatic/moody; white fabric pure neutral white, gold natural yellow, diamonds colorless. The rest of the directive (product/geometry/metal/lifestyle/photography locks) was already covered by v1.3.5-v1.3.19.
- **Reason:** User LUXURY JEWELRY PRODUCT LOCK directive.
- **Impact:** Names two failure modes (fake-gem look, moody/cinematic lighting) under existing P2/color rules. No change to format/camera/token rules.

## v1.3.19 — 2026-07-11 (oval + tapered-baguette shape lock)
- **Modified:** config/QUALITY_MEMORY.json (oval-baguette-shape-lock fix), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Added a shape-substitution guard for oval+tapered-baguette SKUs: elongated oval center must stay a true elongated oval in every view (never round/cushion/pear/wider/shorter/deeper/flatter/thicker/differently-faceted); tapered baguette side stones preserved exactly (shape/taper/size/length/width/facets/angle/placement/setting/metal border) - never reshaped/swapped/simplified. Reference image is the sole source of truth; only camera/scene/background/composition/lighting change; reject+regenerate on any geometry drift. Verified against a consistent 6-image oval+baguette catalog.
- **Reason:** User EXACT PRODUCT LOCK (oval center + tapered baguettes) for a catalog + all upcoming images.
- **Impact:** Names the oval/baguette drift failure mode under the existing geometry locks. No change to format/camera/color/token rules.

## v1.3.18 — 2026-07-11 (diamond geometry + physical optics lock)
- **Modified:** docs/03_IMAGE_GENERATION_RULES.md (§L geometry+optics+side-view+accent locks), prompts/07_PROMPTS.md (cut-anatomy runtime detail), config/QUALITY_MEMORY.json (diamond-geometry-optics-lock fix), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Locked full diamond cut anatomy (dimensions, L:W, table, crown angle+height, pavilion depth, girdle, culet, facet layout/count/proportions, star/bezel/upper+lower-girdle facets, pavilion mains, symmetry, polish, optical symmetry) as identical across every camera angle; physical optics constant (facet pattern/brilliance/scintillation/fire/contrast/transparency/light-return/depth) with no invented reflections/facets/pavilion/crown, no melted facets/blurry junctions; side-view lock (never thinner/thicker/longer/shorter etc; pavilion+crown+girdle consistent with front; looks like the same ring rotated 20/45/60/90); accent-quality lock (side/baguette/pave get center-grade macro quality+exact geometry, never simplified/blurred/replaced with glass). IGI-grade from every angle.
- **Reason:** User DIAMOND GEOMETRY LOCK + PHYSICAL OPTICS LOCK + SIDE VIEW + SIDE DIAMOND QUALITY directive (highest priority).
- **Impact:** Deepens P2 to full cut-anatomy + cross-angle optics constancy. No change to format/camera/color/token rules.

## v1.3.17 — 2026-07-11 (side stone & band lock)
- **Modified:** docs/03_IMAGE_GENERATION_RULES.md (§A SIDE STONE & BAND LOCK), prompts/07_PROMPTS.md (side-stone/band runtime bullet), config/QUALITY_MEMORY.json (side-stone-band-lock fix), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Locked side/band diamonds and the band: preserve exactly each accent stone (shape,size,count,proportions,position,spacing,orientation,alignment,setting,prongs/beads,metal coverage) and the band (width,thickness,shoulder width,taper,curvature,cross-section,metal volume,polish,proportions); never redesign/resize/replace/reinterpret. Side+band stones must show the same center-grade optics (no glow/over-whitening/blur/plastic/painted highlights). Every diamond reads as a real pro-photographed stone; only camera/environment/lighting change.
- **Reason:** User SIDE STONE & BAND LOCK directive (absolute priority).
- **Impact:** Extends P1/P2 to accents + band. No change to format/camera/color/token rules.

## v1.3.16 — 2026-07-11 (studio angle distinctness)
- **Modified:** docs/12_STUDIO_ANGLES_STANDARD.md (§A ANGLE DISTINCTNESS), prompts/07_PROMPTS.md (STUDIO 5 ANGLES bullet), config/QUALITY_MEMORY.json (studio-angle-distinctness fix), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Locked mandatory angle distinctness for the 5 studio shots so they are visibly different camera positions (>=30-40 deg yaw/pitch apart), not near-identical front views. Defined explicit camera geometry per angle (hero straight-on; 45L/45R yawed ~45 + raised ~30-35; side true 90; three-quarter high ~60 top-down at ~30 yaw). If two read as the same angle, regenerate the duplicate. Camera-only; ring stays byte-identical.
- **Reason:** User reported 3 of 4 studio angles were the same position.
- **Impact:** Fixes duplicate-looking studio angles across catalogs. No change to jewelry geometry/logo/cloth/color/token rules.

## v1.3.15 — 2026-07-11 (side-profile consistency)
- **Modified:** docs/03_IMAGE_GENERATION_RULES.md (§A side-profile consistency), prompts/07_PROMPTS.md (gem-geometry runtime bullet), config/QUALITY_MEMORY.json (side-profile-consistency fix), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Locked side-profile consistency for the gemstone: from any side angle preserve the reference's exact profile — never deepen the pavilion, increase crown height, shorten/widen the outline, or let an oval appear rounder. Apparent proportions across front/30/45/60/side/rear views equal those of the one physical ring (L:W + crown/pavilion profile constant; only real-perspective foreshortening changes).
- **Reason:** User SIDE PROFILE CONSISTENCY directive.
- **Impact:** Sharpens the Gem Geometry Lock for multi-angle/oval cases. No change to other rules.

## v1.3.14 — 2026-07-11 (gem geometry lock)
- **Modified:** docs/03_IMAGE_GENERATION_RULES.md (§A GEM GEOMETRY LOCK), prompts/07_PROMPTS.md (gem-geometry runtime bullet), config/QUALITY_MEMORY.json (gem-geometry-lock fix), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Locked the GEM GEOMETRY LOCK: the gemstone is the exact physical stone (never estimate/reconstruct/reinterpret/recreate). Preserve identical across every camera angle: shape, outline, length-to-width ratio, table size, crown height, pavilion depth, girdle thickness, culet position, symmetry, profile, silhouette, apparent size, orientation, optical proportions. Rotating the camera reveals the same stone from a new view (only facet light/brilliance changes per real optics); proportions never change.
- **Reason:** User GEM GEOMETRY LOCK directive (absolute priority).
- **Impact:** Extends P1 geometry lock to the gemstone itself for cross-angle consistency. No change to format/camera/color/token rules.

## v1.3.13 — 2026-07-11 (same-physical-ring mental model)
- **Modified:** docs/03_IMAGE_GENERATION_RULES.md (§A mental model), prompts/07_PROMPTS.md (mental-model note), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Locked the "same physical ring moved to another photoshoot, never a new ring" mental model onto the Product Geometry Lock: only photography changes; the ring is the identical object in every studio AND lifestyle image. If two catalog shots could be two different rings (e.g. full symmetric halo vs open/asymmetric bypass halo), the jewelry drifted -> regenerate all shots to the single source geometry.
- **Reason:** User reinforcement of PRODUCT GEOMETRY LOCK with the same-physical-ring framing.
- **Impact:** Strengthens P1 cross-shot consistency (studio vs lifestyle must match). No change to any other rule.

## v1.3.12 — 2026-07-11 (product geometry lock)
- **Modified:** docs/03_IMAGE_GENERATION_RULES.md (§A PRODUCT GEOMETRY LOCK), prompts/07_PROMPTS.md (geometry-lock runtime bullet), config/QUALITY_MEMORY.json (product-geometry-lock fix), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Locked the PRODUCT GEOMETRY LOCK standard: the reference image is the exact master product (not inspiration/style). Preserve every listed geometry component AND the relative distances between them (silhouette, proportions, head/gallery/basket, prongs count/position/shape/thickness, center+side stone size/count/spacing, halo diameter+geometry, crossover, split-shank, band width/thickness/curvature, shoulder, setting, metal coverage, placement). Every visible pixel of the reference jewelry = ground truth; only camera/environment/lighting/background/composition may change; any component differing triggers regeneration.
- **Reason:** User PRODUCT GEOMETRY LOCK directive (absolute priority).
- **Impact:** Strengthens P1 jewelry fidelity with an exhaustive component + relative-distance lock. No change to format/camera/color/token rules.

## v1.3.11 — 2026-07-11 (diamond standard scoped to all environments + all stones)
- **Modified:** docs/03_IMAGE_GENERATION_RULES.md (§L SCOPE note), prompts/07_PROMPTS.md (DIAMONDS scope), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Extended the diamond realism standard to EVERY environment (office studio, home lifestyle, indoor, outdoor, editorial, luxury product, macro, any future scene) and EVERY stone (center + all side/accent stones) across all shapes/cuts/carats: auto-preserve correct proportions/facet-pattern/optics per shape; lighting follows the actual environment while optics stay physically accurate; every stone indistinguishable from a real VVS/IF lab-grown diamond; natural realism outranks enhancement.
- **Reason:** User NATURAL DIAMOND STANDARD (absolute priority, all environments).
- **Impact:** Broadens P2 diamond realism from studio to all scenes and all stones. No change to jewelry geometry/format/camera/color/token rules.

## v1.3.10 — 2026-07-11 (diamond optical-realism spec locked)
- **Modified:** docs/03_IMAGE_GENERATION_RULES.md (§L OPTICAL SPEC), prompts/07_PROMPTS.md (DIAMONDS runtime bullet), config/QUALITY_MEMORY.json (diamond-optical-realism fix), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Locked a detailed diamond optical-realism standard: match the reference's optics as a professionally macro-photographed premium lab-grown VVS/IF diamond (not AI-enhanced) — crystal-clear water-like transparency, razor-sharp facet definition, excellent light return, high bright/dark facet contrast, natural white brilliance, small fire only where physically correct, accurate crown/table/pavilion/girdle geometry, crisp per-facet reflections; forbid milky/cloudy/washed-out/glow/bloom/fake-sparkle/overexposure/over-sharpening/plastic/glass/CGI; brilliance never boosted artificially.
- **Reason:** User DIAMOND REALISM directive (mandatory).
- **Impact:** Strengthens P2 diamond realism. No change to jewelry geometry/format/camera/color/token rules.

## v1.3.9 — 2026-07-11 (execution-optimization details locked)
- **Modified:** docs/05_TOKEN_OPTIMIZATION.md (EXECUTION-OPTIMIZATION DETAILS), prompts/07_PROMPTS.md (execution-opt runtime bullet), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Locked the detailed token-optimization execution policy (identical output; execution-only): checksum/version-aware loading (reload only modified files); base64 source images never enter context/cache (download→temp file→Read→drop→use temp file only); analyze each SKU source ONCE and cache a lightweight structured design profile in docs/06_CACHE.md for reuse; import media once/session and reuse media_id; reuse cached studio cloth/camera/lighting/WB/logo/runtime-prompt/params/media_ids/design-profile; load only task-relevant QUALITY_MEMORY fixes; one canonical base prompt + minimum delta; verification split (global assets once/session, per-image only jewelry/physics/angle/diamond/cloth); internal reasoning, return only required output; always pick the lowest-token path that yields identical output.
- **Reason:** User TOKEN OPTIMIZATION POLICY (mandatory).
- **Impact:** Lower token consumption; ZERO change to image quality/design/logo/cloth/realism or any locked rule.

## v1.3.8 — 2026-07-11 (runtime token-optimization policy locked)
- **Modified:** docs/05_TOKEN_OPTIMIZATION.md (new RUNTIME POLICY), prompts/07_PROMPTS.md (runtime bullet), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Locked aggressive runtime token optimization with zero output change: load only required files; never reload unchanged files (reuse session memory); reload only modified files; reuse cached studio assets (cloth, preserved logo, lighting, camera, white balance); do not summarize loaded files or explain reasoning; think internally and return only the final result. Guarded by output-quality-is-#1 (skip any optimization that could alter output).
- **Reason:** User Runtime Policy directive.
- **Impact:** Fewer tokens per session; zero change to image quality/behavior or any locked rule.

## v1.3.7 — 2026-07-11 (studio starting-point build sequence locked)
- **Modified:** docs/12_STUDIO_ANGLES_STANDARD.md (new §0 STUDIO STARTING-POINT SEQUENCE), prompts/07_PROMPTS.md (runtime build-order bullet), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Locked the mandatory build order for every office/studio photoshoot: (1) approved premium white cotton cloth first → (2) preserved official logo printed INTO the cloth (never AI) → (3) place the jewelry only after cloth+logo are prepared → (4) photograph the completed scene with the fixed approved studio setup, varying only ring orientation/camera angle/composition/natural folds. Added the per-image FINAL VALIDATION gate (approved cloth, preserved logo, printed-in, jewelry-after-prep, physics, neutral WB, no AI logo, no AI cloth). Noted the practical pipeline (render = clean-cloth+ring intermediate; logo composited locally per docs/04) while the build order + validation still govern the deliverable.
- **Reason:** User STUDIO IMAGE GENERATION STARTING POINT directive (absolute priority).
- **Impact:** Organizes existing cloth/logo/jewelry/color/physics rules into one mandatory sequence + checklist. No change to jewelry geometry/format/camera/token rules; no new assets.

## v1.3.6 — 2026-07-11 (official logo policy consolidated + scoped)
- **Modified:** docs/04_LOGO_WORKFLOW.md (§2 exhaustive forbidden-AI verb list; scope+remedy note), docs/11_BACKGROUND_STANDARD.md (FAILURE POLICY remedy), prompts/07_PROMPTS.md (LOGO runtime scope+remedy), config/VERSION.json, config/project_manifest.json, README (version).
- **Summary:** Reinforced the OFFICIAL LOGO POLICY as permanent for EVERY office/studio photoshoot: exhaustive list of forbidden AI operations on the logo (generate/recreate/redraw/interpret/complete/repair/restyle/enhance/approximate/regenerate — none allowed); logo must be the preserved asset with only cloth-caused transformations (perspective/folds/curvature/lighting/shadows/crop/occlusion); cloth stays the approved premium neutral-white cotton (never AI-invented/tinted); explicit remedy — reject and automatically regenerate until satisfied, and NEVER return a studio image with an AI-generated logo.
- **Reason:** User OFFICIAL LOGO POLICY (absolute priority). Mostly consolidates v1.3.2–v1.3.4 with added verb-list exhaustiveness, studio scope, and regenerate-until-satisfied remedy.
- **Impact:** No new workflow; strengthens P0 logo + P3 cloth enforcement and the reject/regenerate gate. Jewelry/color/format/camera/physics/token rules unchanged.

## v1.3.5 — 2026-07-11 (color fidelity standard locked)
- **Modified:** docs/03_IMAGE_GENERATION_RULES.md (new §O COLOR FIDELITY), prompts/07_PROMPTS.md (color-fidelity runtime bullet), config/QUALITY_MEMORY.json (color-fidelity fix), config/project_manifest.json (workflow_behavior.color), config/VERSION.json, README (version).
- **Summary:** Locked an absolute COLOR FIDELITY standard: the source image is the master for all colors; preserve its palette and neutral white balance exactly; forbid all color grading / artistic-cinematic styling / warm-tone enhancement / creative white balance and any pink/yellow/red/orange/beige/cream/ivory/gray/blue/purple/green tint or warm/cool cast; keep lighting neutral (no added warmth/saturation/contrast/HDR/exposure); metal+diamonds keep natural color with no contamination; cloth stays source neutral white. Added a per-image FINAL VALIDATION gate (correct with whiten_cloth.py or regenerate on any shift). Color fidelity outranks artistic styling.
- **Reason:** User COLOR FIDELITY STANDARD (absolute priority).
- **Impact:** Strengthens neutral-color/white-balance enforcement across studio + lifestyle + close-up. No change to jewelry geometry/format/camera/physics/token rules; complements docs/11 FAILURE POLICY.

## v1.3.4 — 2026-07-11 (locked logo+cloth assets: failure policy + cross-device caching)
- **Modified:** docs/11_BACKGROUND_STANDARD.md (cloth-as-preserved-asset + FAILURE POLICY + caching), docs/04_LOGO_WORKFLOW.md (§13 failure policy & caching), prompts/07_PROMPTS.md (failure-policy runtime bullet), config/QUALITY_MEMORY.json (logo-cloth-failure-policy fix), config/project_manifest.json (cloth asset checksum + asset_caching), config/VERSION.json, README (version).
- **Summary:** Formalized the user's LOCKED LOGO & CLOTH ASSETS spec: both logo and cloth are preserved ASSETS, never AI-generated; added an explicit reject-the-image FAILURE POLICY (logo differs/AI-looking/not-merged; cloth material-change/yellowish/flat-cheap); registered the cloth asset in locked_asset_checksums; added a byte-preserving cross-device/session caching rule that must never alter quality or fidelity.
- **Reason:** User LOCKED LOGO & CLOTH ASSETS directive (asset-only, failure policy, caching).
- **Impact:** Adds a hard quality gate + cache-integrity contract. No change to jewelry/diamond/format/camera/physics/token rules; no workflow restructuring.

## v1.3.3 — 2026-07-11 (logo + cloth integrity rules locked)
- **Modified:** docs/04_LOGO_WORKFLOW.md (new §12), docs/11_BACKGROUND_STANDARD.md (never-AI-invent-cloth + premium cotton), prompts/07_PROMPTS.md (CLOTH + LOGO runtime bullets), config/QUALITY_MEMORY.json (3 new fixes), CLAUDE_SETUP.md (P3), config/project_manifest.json (workflow_behavior), config/VERSION.json.
- **Summary:** Locked three reported quality failures as permanent rules: (1) NEVER AI-generate the logo OR the background cloth — logo = exact preserved asset via local composite or omit; cloth = approved premium white cotton reproduced faithfully, never a new AI fabric; (2) the logo must MERGE NATURALLY as ink printed into the cloth (multiply-blend, texture shows through, follows folds/light) — a pasted/floating look is a FAIL; (3) cloth must be premium white cotton with natural soft draping — never yellowish (fix with whiten_cloth.py) and never flat/simple/cheap.
- **Reason:** User reported inaccurate/AI-generated logos, logos not merging with cloth, and yellowish/simple cloth.
- **Impact:** Reinforces P0 logo + P3 background integrity. No change to jewelry/diamond fidelity, format (1:1/2K), camera, physics, or token rules; no workflow restructuring.

## v1.3.2 — 2026-07-11 (safe low-token loading finalized + README rewrite)
- **Modified:** README.md (full rewrite), config/VERSION.json, config/project_manifest.json, docs/10_CURRENT_STATE.md.
- **Summary:** Finalized the safe low-token loading policy (startup = CLAUDE_SETUP.md only; lazy-load one file per task; normal generation = runtime trio manifest+07_PROMPTS+QUALITY_MEMORY) and rewrote README to document it: project purpose, current workflow, Higgsfield+Claude MCP primary / Python zero-credit fallback, startup entry file, low-token loading policy, output-compatibility guarantee, required files/assets, new-project setup, git sync, recovery, current stable version + latest commit, "Git is the source of truth." Added config/QUALITY_MEMORY.json to VERSION.minimum_required_files and manifest.required_files.
- **Reason:** User task — implement safe low-token loading without changing output behavior + update README.
- **Impact:** Documentation/metadata only. Zero change to generation quality or any jewelry/diamond/cloth/lighting/physics/camera/logo/format/token rule. Loading policy was already active (v1.3.0/v1.3.1); this release documents and locks it.

## v1.3.1 — 2026-07-11 (context lazy-loading policy)
- **Modified:** CLAUDE_SETUP.md (startup loads only this file; §1 replaced with lazy-loading map), docs/05_TOKEN_OPTIMIZATION.md (policy note), config/VERSION.json, config/project_manifest.json.
- **Summary:** Startup context reduced to CLAUDE_SETUP.md only; all other files lazy-loaded per task. Normal generation loads the runtime trio. Hard rules/env/loop kept inline in CLAUDE_SETUP so quality is unaffected.
- **Reason:** User CONTEXT LOADING POLICY (modular, fast startup, minimum tokens, identical quality).
- **Impact:** Lower per-session token load; zero change to generation quality/rules.

## v1.3.0 — 2026-07-10 (safe low-token runtime)
- **Modified/added:** prompts/07_PROMPTS.md (RUNTIME RULES compact authoritative section), config/QUALITY_MEMORY.json (new, 12 verified fixes), config/project_manifest.json (runtime_files + runtime_pointers), config/VERSION.json.
- **Summary:** Enabled low-token loading (manifest + 07_PROMPTS + QUALITY_MEMORY). All active production rules + pointers + verified error fixes compiled into the 3 runtime files. Coverage comparison test PASS (all rules/pointers/fixes present) — behavior unchanged.
- **Reason:** User safe low-token loading policy.
- **Impact:** Fewer files read per generation; zero change to jewelry/diamond/cloth/lighting/physics/camera/logo behavior. Long docs still authoritative for edits/recovery/audit.

## v1.2.1 — 2026-07-10 (logo: omit-over-approximate)
- **Modified:** docs/04_LOGO_WORKFLOW.md (new §11 governing rule), config/VERSION.json, config/project_manifest.json.
- **Summary:** Logo governing rule locked — AI must never approximate the logo; use the exact preserved asset or OMIT it. Missing logo acceptable; incorrect logo unacceptable. Studio default reverts to clean cloth + exact-asset composite (or absent). In-model logo-reference path allowed only when verified pixel-identical.
- **Reason:** User CRITICAL directive prioritizing brand-logo integrity over presence.
- **Impact:** Prevents AI-drawn/garbled logos in deliverables. No change to jewelry/diamond fidelity, cloth, format, or token rules.

## v1.2.0 — 2026-07-10 (studio standards consolidation)
- **Version:** 1.2.0  **Date:** 2026-07-10
- **Modified files:** docs/03_IMAGE_GENERATION_RULES.md, docs/04_LOGO_WORKFLOW.md, prompts/07_PROMPTS.md, docs/06_CACHE.md, docs/12_STUDIO_ANGLES_STANDARD.md (renamed from 12_STUDIO_ANGLES_AND_PHYSICS.md), docs/10_CURRENT_STATE.md, config/project_manifest.json, config/VERSION.json.
- **Summary:** Folded the recently locked standards into their owner files (no new duplicate docs): diamond realism, photography/reference consistency, natural per-shot variation (03); pixel-identical logo policy, logo-as-metallic-ink-into-cloth, logo-as-generation-reference (04); logo-preserving studio prompt v2 + logo-correction edit prompt (07); official-logo generation-reference cache note (06); renamed the studio-angles file to the policy-owned name (12).
- **Reason:** User locked diamond-realism, reference-consistency, physical-scene, absolute-logo, and repository-maintenance policies; consolidate per file-ownership rules.
- **Impact:** Studio images now generated with the printed logo preserved in-model (3-reference path) or corrected via the logo-edit prompt; local composite remains the pixel-perfect fallback when the render is downloadable. No change to jewelry-fidelity, cloth, format (1:1/2K), or token rules.

## v1.1.0 — 2026-07-10 (STABLE MILESTONE: portable export + printed-logo policy)
- **Logo policy finalized → PRINTED-ON-CLOTH.** The logo must always appear, composited from the locked asset to look physically printed on the fabric (follows folds/perspective/lighting, partial crop/occlusion OK, off-center). Supersedes the interim "generate clean cloth, no logo at all" idea — the logo is NOT removed, it is composited.
- **Locked brand logo asset added** (`assets/logo/logo_official.png`, exact user upload, 1,079,081 bytes; Drive id `1QZgjplaFWenZHt048tzQntk-L-Ezy_qH`) + transparent derivative (`assets/logo/logo_official_transparent.png`, background-keyed, ink pixels preserved).
- **`scripts/print_logo_on_cloth.py`** added — multiply-blend + brightness-modulation + optional fold displacement so the logo reads as printed, not pasted.
- **MASTER BACKGROUND STANDARD locked** — cloth material + neutral-white color + texture/fold style are canonical and consistent across all catalogs.
- **All images standardized to 1:1 / 2K** (previously 4:5 for lifestyle).
- **Canonical base prompt locked** (user-provided VVS/fidelity wording).
- **Token-optimization rules (10)** locked as highest-priority efficiency layer; cache of Drive IDs documented.
- **Full portable documentation exported** to `docs/` + `NEW_PROJECT.md`, `RECOVERY.md`, `VERSION.md`, `README.md`.
- **Catalogs generated this session:** LR-0156 (round solitaire, bead-set shoulders), LR-0136 (oval + green emeralds), LR-0137 (oval + tapered baguettes).
- **Repo created & pushed:** `SidGajera/Claude_Lucent_Image_Gen` (private, branch `main`).

## Earlier learnings folded in (2026-07-08/09/10)
- **Diamond doubling fix:** enforce single real facet pattern; no CGI kaleidoscope. Benchmark = LR-0156 studio shot.
- **Logo hallucination:** model renders fake logos ("ELLYREID") → never let AI render the logo; composite locally.
- **Lifestyle theme fix:** cozy warm US-home; forbid laptop/desk/office scenes.
- **Model/resolution coercion:** set `params.model:"nano_banana_2"` AND explicit `resolution:"2k"` (default is 1k); server may label the edit path `nano_banana_flash`.
- **Cloth warmth:** fix locally with `whiten_cloth.py` (0 credits), never regenerate for color.
- **Correct source file:** ignore stray/mislabeled images (LR-0167 "Copy of 7/4" belonged to another ring).
- **media_id expiry:** durable cache = Drive file IDs; re-import when rejected.

## v1.0.0 — Initial checkpoint
- Repo initialized; website files committed; `LUCENT_MASTER.md` (merged master spec) + `whiten_cloth.py` added.

## Prior sessions (pre-repo)
- SKUs LR-0160/0162/0164/0165/0166/0167/0168/0190/0191/0192 generated; workflow, diamond standard, cloth/logo rules, lean workflow, and 6-doc consolidation established (captured in `LUCENT_MASTER.md`).
