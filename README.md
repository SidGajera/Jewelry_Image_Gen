# Lucent Carat Lab — AI Catalog Image Generation

| | |
|---|---|
| **Current Stable Version** | 1.3.5 (stable build ✅) |
| **Latest Commit** | see [`config/VERSION.json`](config/VERSION.json) → `latest_commit_hash` |
| **Startup / Entry File** | [`CLAUDE_SETUP.md`](CLAUDE_SETUP.md) — the ONLY file loaded at startup |
| **Recovery** | [`RECOVERY.md`](RECOVERY.md) · machine-readable [`config/VERSION.json`](config/VERSION.json) |
| **Repository** | [SidGajera/Claude_Lucent_Image_Gen](https://github.com/SidGajera/Claude_Lucent_Image_Gen) (`main`) |

> **Git is the source of truth.** Behavior comes from the files in this repository, never from prior chat history. A new Claude session assumes no memory and reconstructs the entire approved workflow from these files.

## Project purpose
Portable, reproducible system for generating **12 marketing catalog photos per jewelry SKU** — 5 studio + 4 lifestyle + 3 close-up, all **1:1 / 2K** — that keep the jewelry **100% identical to the source**, on the brand's locked white studio cloth, with the **exact** Lucent Carat Lab logo (never AI-invented). Any session can clone this repo and reproduce the workflow with no other context.

## Current workflow
Per SKU: find source → study the ring (verify correct file) → import source + references → **generate 1 verification image → user confirms fidelity → generate the rest in one batch** → user downloads → composite the exact logo locally (0 credits) → update docs + commit. Full loop in [`docs/10_CURRENT_STATE.md`](docs/10_CURRENT_STATE.md); five studio angles in [`docs/12_STUDIO_ANGLES_STANDARD.md`](docs/12_STUDIO_ANGLES_STANDARD.md).

### Image generation flow
- **PRIMARY — Higgsfield + Claude MCP.** Model `nano_banana_2`, `resolution:"2k"`, `aspect_ratio:"1:1"`, `count:1`, medias `[reference, SOURCE, (optional OFFICIAL-logo)]`, 2 credits/image. This is the approved generation path.
- **FALLBACK — Python zero-credit post-processing** (Pillow + NumPy, 0 credits): [`scripts/print_logo_on_cloth.py`](scripts/print_logo_on_cloth.py) composites the exact logo to look printed on the cloth; [`whiten_cloth.py`](whiten_cloth.py) forces neutral-white cloth. Used to fix our own output locally — never burn credits correcting our mistakes.

## Low-token loading policy
- **At startup, load ONLY `CLAUDE_SETUP.md`.** It carries the hard rules, environment, and per-SKU loop needed to begin. Do NOT preload docs, prompts, cache, changelog, or the master spec.
- **Lazy-load exactly one relevant file per task** using the map in `CLAUDE_SETUP.md` §1; discard unused sections after extracting the rules.
- **Normal generation loads the runtime trio only:** [`config/project_manifest.json`](config/project_manifest.json) + [`prompts/07_PROMPTS.md`](prompts/07_PROMPTS.md) + [`config/QUALITY_MEMORY.json`](config/QUALITY_MEMORY.json). These three restate every active production rule, pointer, and verified fix — self-sufficient for a full catalog.
- **Output-compatibility guarantee:** this policy changes only *how much context is loaded*, never *what is produced*. Every jewelry-fidelity, diamond, cloth, lighting, physics, camera, logo, format (1:1/2K), and token rule is unchanged. Reducing loaded context must never reduce output quality — if you need more, load one more small file, never the whole repo.

## Required files & assets
**Config:** [`config/VERSION.json`](config/VERSION.json) (version, commit, `minimum_required_files`) · [`config/project_manifest.json`](config/project_manifest.json) (files, assets, checksums, runtime trio, pointers) · [`config/QUALITY_MEMORY.json`](config/QUALITY_MEMORY.json) (verified error fixes).

**Docs (`docs/`):** `01_MASTER_SPECIFICATION` · `02_SYSTEM_RULES` (P0–P8) · `03_IMAGE_GENERATION_RULES` · `04_LOGO_WORKFLOW` · `05_TOKEN_OPTIMIZATION` · `06_CACHE` (Drive IDs) · `08_PROJECT_STRUCTURE` · `09_CHANGELOG` · `10_CURRENT_STATE` · `11_BACKGROUND_STANDARD` · `12_STUDIO_ANGLES_STANDARD`. Prompts: [`prompts/07_PROMPTS.md`](prompts/07_PROMPTS.md).

**Assets:** `assets/logo/logo_official.png` (LOCKED exact upload — never modify/AI-render) · `assets/logo/logo_official_transparent.png` (background-keyed for compositing) · `assets/background/sample_studio_background_with_logo.png` (locked cloth reference).

**Scripts:** `scripts/print_logo_on_cloth.py` · `whiten_cloth.py`.

## New-project setup
1. Clone the repo: `git clone https://github.com/SidGajera/Claude_Lucent_Image_Gen.git`.
2. Open **`CLAUDE_SETUP.md`** — read only that file to start.
3. Lazy-load per its §1 map when a task needs a deeper file.
4. Operate all Google Drive / Higgsfield actions as `lucentcaratlab@gmail.com`.
5. Wait for the user's instruction (e.g. "go for 0XXX folder").

## Git sync
- Keep local in sync: `git pull origin main`.
- Push work to the canonical repo: `git push -u origin main`.
- **Origin must be `Claude_Lucent_Image_Gen`.** The GitHub rename redirect can rewrite origin to the old name — verify with `git remote -v` and, if needed, `git remote set-url origin https://github.com/SidGajera/Claude_Lucent_Image_Gen.git` before pushing.

## Recovery
Read `CLAUDE_SETUP.md` → `config/VERSION.json` (version, commit, `minimum_required_files`) → the documented file order → `RECOVERY.md`. Git tags cannot be pushed from the generating environment (proxy denies `refs/tags/*`), so **do not rely on tags** — `config/VERSION.json` is the self-describing version record. The repository is the single source of truth.

## Non-negotiables
1. Logo is a locked asset — NEVER AI-rendered; composited from the exact original. **Omit over approximate:** a missing logo is acceptable, an incorrect one is not.
2. Jewelry 100% identical to the source (never add/remove/resize/recolor stones or alter setting/band/metal).
3. Diamonds: single real facet pattern, natural bright+dark mix, no doubling/CGI/artificial whitening.
4. Cloth material + neutral-white color locked; consistent every image.
5. Always 1:1 / 2K. Operate as `lucentcaratlab@gmail.com`.
