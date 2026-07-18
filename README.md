# Lucent Carat Lab — AI Catalog Image Generation

| | |
|---|---|
| **Branch** | **`desktop-pc` only** — never merge/checkout/rebase/update `main` (`main` and `desktop-pc` are diverged by design) |
| **Repository** | [SidGajera/Claude_Lucent_Image_Gen](https://github.com/SidGajera/Claude_Lucent_Image_Gen) |
| **Pipeline** | **Higgsfield only** (`docs/15` §0) — the CAD/Blender/Python path is deleted and banned |
| **Policy map** | [`docs/00_POLICY_INDEX.md`](docs/00_POLICY_INDEX.md) — one authoritative owner per topic |
| **Recovery** | [`docs/19_RECOVERY_CHECKPOINT.md`](docs/19_RECOVERY_CHECKPOINT.md) — auto-activation map on fresh pull |

> **Git is the source of truth.** Behavior comes from the files in this repo, never from prior chat. A fresh pull of `desktop-pc` restores the full workflow automatically — load [`docs/00`](docs/00_POLICY_INDEX.md) first; every rule below is already committed and active, no re-prompting.

## Project purpose
Portable, reproducible system for generating jewelry-SKU marketing catalogs — office/studio + house-lifestyle sets, **1:1 / 2K** — with jewelry kept **100% identical to the source**, on the locked premium pure-white cotton cloth, with the **exact preserved** Lucent Carat Lab logo.

## Recovery checkpoint — active permanent rules → where they live
A fresh pull activates all of these automatically (full map in [`docs/19`](docs/19_RECOVERY_CHECKPOINT.md)):

| Rule | Owner |
|---|---|
| Permanent Token Optimizer / targets / token-cost summary | [`17`](docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md) |
| Short-output policy (≤3 lines, one-sentence default) | [`17`](docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md) |
| Silent execution / no reasoning-planning narration | [`17`](docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md) |
| No bash/shell display · no tool-output narration | [`17`](docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md) |
| No thinking/progress narration | [`17`](docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md) |
| No Higgsfield preview widget / silent generation | [`17`](docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md) |
| Full file path with drive name | [`17`](docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md) |
| Retry budget (max 2 credited/angle, then skip) | [`17`](docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md) |
| Safe-optimization guardrails · token-report honesty | [`17`](docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md) |
| One image per angle / camera uniqueness (≤20%) | [`12`](docs/12_STUDIO_ANGLES_STANDARD.md) |
| Cached policies/CAD/logo/cloth/failure memory; never reload | [`17`](docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md) |
| Diamond consistency · metal colour (18K YG) · photorealism/anti-CGI · lifestyle set · no-text/watermark | [`03`](docs/03_IMAGE_GENERATION_RULES.md) |
| Jewelry geometry / D2D / twist / head-shoulder / bottom-shank / no-invention | [`13`](docs/13_JEWELRY_PRESERVATION_SPEC.md) (+ [`16`](docs/16_ZERO_DESIGN_INVENTION.md)) |
| Cloth (pure white cotton) + benchmark | [`11`](docs/11_BACKGROUND_STANDARD.md) |
| Logo: master lock (preserved artwork), embedded print, jewelry-first, visibility, matte params | [`04`](docs/04_LOGO_WORKFLOW.md) §14.0–§14.2 |
| Catalog consistency gate (pre-gen + final validation) | [`18`](docs/18_MASTER_CATALOG_CONSISTENCY_POLICY.md) |
| Failure/Quality Memory (FM-0163, FM-0164, LR-0159 F1–F4, twist recurrences) | [`07`](docs/07_QUALITY_MEMORY.md) + [`config/QUALITY_MEMORY.json`](config/QUALITY_MEMORY.json) |
| Approval + catalog git rule | [`03`](docs/03_IMAGE_GENERATION_RULES.md) + [`15`](docs/15_SAFE_PIPELINE_VERSIONING.md) §8.5 |

## Generation
- **Higgsfield** `nano_banana_2`, `resolution:"2k"`, `aspect_ratio:"1:1"`, `count:1`, ~2 credits/image. Source stills carry max geometry weight; then locked cloth + preserved logo; then the pose/angle delta.
- Server may label the multi-image edit path `nano_banana_flash` — expected; `resolution:"2k"` governs quality.
- Never place image base64/raw bytes in chat context; download → temp file → read locally. No preview/`show_generations`/`job_display` widgets.

## Catalog state
Delivered ([`config/deliveries/`](config/deliveries)): LR-0149, 0151, 0152, 0153, 0154, 0155, 0156, 0157, 0158, 0159, 0161, 0162, 0163, 0164, BRACELET-01. **Parked:** LR-0150.
Delivery records hold design profile, workflow, reference media IDs, and angle map. Output PNGs live in `D:\Lucent Image generation\workspace\output\<SKU>` (gitignored → Drive); golden source stills + regression baseline in [`workspace/golden/<SKU>`](workspace/golden).

## Source fetch
Fetch source images from the SKU's **main Drive folder only** — never enter subfolders without explicit permission. Gold (18K YG) by default. Download each source once; reuse its local path/ID.

## Git workflow — `desktop-pc` only (permanent)
All work stays on `desktop-pc`; never merge/checkout/rebase/update `main`; push only to `origin/desktop-pc`. Standing approval: commit + push automatically every time a catalog is completed/approved — never during generation, never unapproved images/secrets/venv, never rewrite history without explicit approval.

## Non-negotiables
1. Jewelry geometry is immutable — 100% identical to source; never redesign or invent.
2. Logo is a locked preserved asset — never AI-approximated; icon + wordmark + gold tagline present, jewelry-first/subtle, embedded matte textile print.
3. Diamonds: single real facet pattern, natural brilliance, office set = master quality reference, no CGI/doubling/whitening.
4. Cloth: locked premium pure bright white cotton, consistent every image.
5. Always 1:1 / 2K. `desktop-pc` only. Higgsfield-only pipeline.
6. Optimize tokens only by removing redundancy — never trade quality, geometry, pipeline, validation, or output ([`17`](docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md) SAFE-OPTIMIZATION GUARDRAILS).
