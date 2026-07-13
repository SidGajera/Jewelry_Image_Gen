# Lucent Carat Lab — AI Catalog Image Generation

| | |
|---|---|
| **Current Version** | 1.4.0 (stable ✅) — see [`config/VERSION.json`](config/VERSION.json) |
| **Startup / Entry File** | [`config/runtime.json`](config/runtime.json) (clean-session startup) → [`CLAUDE_SETUP.md`](CLAUDE_SETUP.md) rules entry |
| **Repository** | [SidGajera/Claude_Lucent_Image_Gen](https://github.com/SidGajera/Claude_Lucent_Image_Gen) (**`main` only**) |
| **Recovery** | [`RECOVERY.md`](RECOVERY.md) · machine-readable [`config/VERSION.json`](config/VERSION.json) |

> **Git is the source of truth.** Behavior comes from the files in this repository, never from prior chat history. A new session assumes no memory and reconstructs the entire approved workflow from these files.

## Project purpose
Portable, reproducible system for generating **12 marketing catalog photos per jewelry SKU** — 5 studio + 4 lifestyle + 3 close-up, all **1:1 / 2K** — that keep the jewelry **100% identical to the source CAD**, on the brand's locked white studio cloth, with the **exact** two-tone Lucent Carat Lab logo. Any session can clone this repo and reproduce the workflow with no other context.

## Per-SKU workflow (current)
Locate source in Drive → **study the ring once** (cache the design profile) → import source + branded cloth + logo + rotated poses → **generate 12** with the strict locked-geometry prompts → **auto-QC vs source** → **auto-fallback on any drift** → user approves → deliver + record. Full loop in [`docs/10_CURRENT_STATE.md`](docs/10_CURRENT_STATE.md); five studio angles + rotation in [`docs/12_STUDIO_ANGLES_STANDARD.md`](docs/12_STUDIO_ANGLES_STANDARD.md).

### Generation
- **Model** `nano_banana_2`, `resolution:"2k"`, `aspect_ratio:"1:1"`, `count:1`, 2 credits/image. Medias: source CAD views **first** (max geometry weight), then optional branded cloth + official logo, then the pose reference.
- Server may label the multi-image edit path `nano_banana_flash` — expected; `resolution:"2k"` governs quality.

## Geometry-immutable auto-fallback (the core guarantee, v1.4.0)
Jewelry geometry is **immutable**; only camera/composition/cloth/background/lighting/DoF may change. Per shot, automatically (never asking which method):
1. **AI generation** with the strict CAD-lock prompt.
2. **Auto-QC vs source** — head, halo diameter + rim, center-to-halo ratio, prong count/positions, shank, gallery, metal thickness, silhouette; lighting; logo.
3. On **any** drift → do NOT deliver; fall through: **(1)** composite the *real source-ring pixels* into the AI scene ([`scripts/composite_ring_into_scene.py`](scripts/composite_ring_into_scene.py)); **(2)** if the angle is unreachable, render it from the CAD file, then composite.

Honest limit: `nano_banana` biases toward the CAD but cannot guarantee <1% geometry — that is *why* the fallback ladder exists. Details in [`config/QUALITY_MEMORY.json`](config/QUALITY_MEMORY.json) (`geometry-immutable-auto-fallback`) and [`docs/12`](docs/12_STUDIO_ANGLES_STANDARD.md) §A3.

## Locked standards (this repo enforces, auto-applied from `QUALITY_MEMORY.json`)
- **Logo — required, in-scene, two-tone:** every studio shot carries the logo, hot-foil printed *into* the fabric (follows folds, weave shows through, matched lighting, no float/emboss). It is **two-tone**: emblem + "LUCENT CARAT LAB" gold, **"FUTURE OF FINE JEWELRY" black** — never gold-ified. Exact-typography fallback = local composite ([`scripts/print_logo_on_cloth.py`](scripts/print_logo_on_cloth.py)).
- **Jewelry is always the hero:** ring = 70–90% of visual attention, framed large, background soft-blurred and never sharper than the ring; lifestyle hand is a stand, not the subject.
- **Per-catalog angle rotation + natural photography:** rotate camera geometry each SKU (incl. harder angles); real macro look (shallow DoF, off-center-yet-dominant framing, real-lens character); no AI tells.
- **Color/diamond/cloth fidelity:** source is master for all color; neutral-white daylight; single real facet pattern; premium neutral-white cloth.

## Runtime & token policy
- **Clean-session startup:** read ONLY [`config/runtime.json`](config/runtime.json) → reply `READY — 0 ACTIVE PROCESSES` → wait.
- **Token-only optimization:** cache Drive IDs, read each source once, reuse the design profile, never re-list unchanged folders, never echo full prompts/URLs/schemas, batch equivalent calls — **without ever changing output, geometry, QC depth, or resolution.**
- **Token-safety:** when budget is critically low, stop launching new work and return a status summary instead.
- **Permissions:** granted once per session (allowlisted in `.claude/settings.local.json`); no repeat prompts. Mid-turn "Stream closed"/"Denied by user" are MCP **transport** drops, not permission asks — auto-reconnect and retry.

## Git workflow — `main` only (permanent)
All development, fixes, commits, and pushes go **directly to `main`**. No feature branches, no PR workflow (unless explicitly requested). Verify you are on `main` before each task. Origin must be `Claude_Lucent_Image_Gen` — the GitHub rename redirect can rewrite it, so run `git remote set-url origin https://github.com/SidGajera/Claude_Lucent_Image_Gen.git` if a push 404s. Full policy in [`CLAUDE_SETUP.md`](CLAUDE_SETUP.md) §0.5.

## Deliveries
Approved catalogs are recorded in [`config/deliveries/`](config/deliveries) as `LR-XXXX.json` (SKU, locked design, all 12 job IDs, source folder). Committed only on explicit "Approve catalog LR-XXXX".

## Repository layout
- **Config:** [`config/VERSION.json`](config/VERSION.json) · [`config/project_manifest.json`](config/project_manifest.json) · [`config/QUALITY_MEMORY.json`](config/QUALITY_MEMORY.json) (verified fixes, auto-applied) · [`config/runtime.json`](config/runtime.json) · [`config/deliveries/`](config/deliveries).
- **Docs (`docs/`):** `01_MASTER_SPECIFICATION` · `02_SYSTEM_RULES` · `03_IMAGE_GENERATION_RULES` · `04_LOGO_WORKFLOW` · `05_TOKEN_OPTIMIZATION` · `06_CACHE` (Drive IDs) · `08_PROJECT_STRUCTURE` · `09_CHANGELOG` · `10_CURRENT_STATE` · `11_BACKGROUND_STANDARD` · `12_STUDIO_ANGLES_STANDARD`. Prompts: [`prompts/07_PROMPTS.md`](prompts/07_PROMPTS.md).
- **Assets:** `assets/logo/logo_official.png` (LOCKED two-tone) · `assets/logo/logo_official_transparent.png` · `assets/background/sample_studio_background_with_logo.png`.
- **Scripts:** [`scripts/print_logo_on_cloth.py`](scripts/print_logo_on_cloth.py) (hot-foil two-tone logo composite) · [`scripts/composite_ring_into_scene.py`](scripts/composite_ring_into_scene.py) (exact-ring fallback) · `whiten_cloth.py`.
- **Tool (`tool/`):** web-app scaffold to run the whole pipeline with auto-QC + approval gate — see [`tool/README.md`](tool/README.md).

## New-project setup
1. `git clone https://github.com/SidGajera/Claude_Lucent_Image_Gen.git`
2. Open **`config/runtime.json`** (clean-session start), then `CLAUDE_SETUP.md` for the rules entry.
3. Operate all Google Drive / Higgsfield actions as `lucentcaratlab@gmail.com`.
4. Wait for the instruction (e.g. "go for 0XXX").

## Non-negotiables
1. Jewelry geometry is immutable — 100% identical to source; on drift, composite the real ring, never ship a redesign.
2. Logo is a locked two-tone asset — never AI-approximated; black tagline stays black.
3. Diamonds: single real facet pattern, natural brilliance, no CGI/doubling/whitening.
4. Cloth: locked premium neutral-white cotton, consistent every image.
5. Always 1:1 / 2K. `main` only. Operate as `lucentcaratlab@gmail.com`.
