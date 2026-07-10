# Lucent Carat Lab — AI Catalog Image Generation

| | |
|---|---|
| **Current Stable Version** | 1.1.0 (stable build ✅) |
| **Latest Commit** | `__COMMIT_HASH__` (`main`, __COMMIT_DATE__) |
| **Setup File** | [`CLAUDE_SETUP.md`](CLAUDE_SETUP.md) — single entry point |
| **Recovery File** | [`RECOVERY.md`](RECOVERY.md) · machine-readable: [`config/VERSION.json`](config/VERSION.json) |
| **Repository** | [SidGajera/Jewelery-Website](https://github.com/SidGajera/Jewelery-Website) |

### Repository Structure
```
CLAUDE_SETUP.md            # SINGLE ENTRY POINT
README.md                  # this file
NEW_PROJECT.md RECOVERY.md VERSION.md LUCENT_MASTER.md
config/  VERSION.json  project_manifest.json
docs/    01..06, 08..11 (spec, rules, image rules, logo, tokens, cache, structure, changelog, current state, background)
prompts/ 07_PROMPTS.md
scripts/ print_logo_on_cloth.py
assets/  logo/  background/  references/
whiten_cloth.py
```

> **Start here: open `CLAUDE_SETUP.md`** — the single entry point. A new Claude session reads that one file, then the ordered list it points to, and can reproduce the entire approved workflow.

Portable, reproducible system for generating **12 marketing photos per jewelry SKU** (5 studio + 4 lifestyle + 3 close-up, all 1:1 / 2K) that keep the jewelry 100% identical to the source, on the brand's locked white studio cloth with the **printed** Lucent Carat Lab logo.

## Entry & recovery
- **`CLAUDE_SETUP.md`** — SINGLE ENTRY POINT (read first).
- **`config/project_manifest.json`** — manifest (version, commit, files, assets, checksums, setup order).
- **`LUCENT_MASTER.md`** — canonical merged spec.
- **`NEW_PROJECT.md`** — bootstrap a brand-new Claude project.
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
- `assets/logo/logo_official.png` — LOCKED brand logo (exact upload; never modify).
- `assets/logo/logo_official_transparent.png` — background-keyed logo for compositing.
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
