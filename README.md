# Lucent Carat Lab — AI Catalog Image Generation

Portable, reproducible system for generating **12 marketing photos per jewelry SKU** (5 studio + 4 lifestyle + 3 close-up, all 1:1 / 2K) that keep the jewelry 100% identical to the source, on the brand's locked white studio cloth with the **printed** Lucent Carat Lab logo.

## Start here
- **`LUCENT_MASTER.md`** — canonical merged spec (single source of truth).
- **`NEW_PROJECT.md`** — bootstrap a brand-new Claude project to reproduce this exactly.
- **`RECOVERY.md`** — restore/continue after cloning.
- **`VERSION.md`** — version, commit, date, improvements.

## Documentation (`docs/`)
| File | Topic |
|---|---|
| `01_MASTER_SPECIFICATION.md` | Workflow, architecture, pipeline, success criteria |
| `02_SYSTEM_RULES.md` | Every permanent rule + priority order (P0–P8) |
| `03_IMAGE_GENERATION_RULES.md` | Jewelry, diamonds, metal, camera, lighting, background, composition, cropping, resolution, shadows |
| `04_LOGO_WORKFLOW.md` | Locked logo asset + printed-on-cloth compositing |
| `05_TOKEN_OPTIMIZATION.md` | Cache/reuse/batch/silent-execution rules |
| `06_CACHE.md` | Every reusable asset (Drive IDs) |
| `07_PROMPTS.md` | Reusable prompts |
| `08_PROJECT_STRUCTURE.md` | Folders + files |
| `09_CHANGELOG.md` | What changed |
| `10_CURRENT_STATE.md` | Exact current workflow |
| `11_BACKGROUND_STANDARD.md` | Locked cloth standard |

## Assets & scripts
- `logo_official.png` — LOCKED brand logo (exact upload; never modify).
- `logo_official_transparent.png` — background-keyed logo for compositing.
- `scripts/print_logo_on_cloth.py` — print the logo onto a studio shot (0 credits).
- `whiten_cloth.py` — force pure neutral-white cloth (0 credits).

## Non-negotiables
1. Logo is a locked asset — NEVER AI-rendered; composited from the original to look printed on cloth.
2. Jewelry never modified vs the source.
3. Cloth material + neutral-white color locked.
4. Always 1:1 / 2K.
5. Operate as `lucentcaratlab@gmail.com`.

## Tools
Higgsfield `nano_banana_2` (2K, 2 credits/img) · Google Drive (READ/SEARCH/CREATE) · GitHub. Local post-processing in Python (Pillow + NumPy).
