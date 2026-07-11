# 09 — CHANGELOG

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
