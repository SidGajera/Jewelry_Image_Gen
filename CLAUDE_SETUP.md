# CLAUDE_SETUP.md — SINGLE ENTRY POINT

You are a new Claude session bootstrapping the **Lucent Carat Lab** catalog image-generation automation. This repository is the **single source of truth**. The repo is intentionally modular to minimize context — **at startup load ONLY this file**, then lazy-load exactly one relevant file per task (section 1).

## 0. VERSIONING & BOOTSTRAP (do this before anything else)
Every new Claude session MUST:
1. **Load ONLY `CLAUDE_SETUP.md` (this file) at startup.** Do NOT preload docs, prompts, cache, changelog, or the master spec.
2. **Treat the repository as the single source of truth**; never depend on previous conversation history (assume none exists).
3. This file already carries the hard rules (§3), environment (§4), and per-SKU loop (§5) needed to start. Pull any deeper file only when the task actually needs it (§1).
4. (Only when explicitly verifying/recovering) check `config/VERSION.json` for version/commit and `minimum_required_files`, and `config/project_manifest.json` for `required_files/required_assets`.

## 0.5 GIT WORKFLOW — MAIN ONLY (permanent policy, user-locked 2026-07-13)
This is the permanent Git workflow. It overrides any prior branch instruction.
- **`main` is the only branch.** All development, fixes, commits, and pushes go **directly to `main`**.
- **Never** create a feature branch, sub-branch, or worktree without the user's **explicit** permission.
- **No PR workflow.** Never ask whether to merge or open a PR; do not open PRs unless the user explicitly requests one. Never ask the user where to commit — the answer is always `main`.
- **Before every new task, verify you are on `main`** (`git branch --show-current`); if not, switch to `main` first.
- **If a branch ever exists:** merge it into `main` immediately, resolve any conflicts, push `main`, then delete the merged branch **locally and on GitHub**. Never leave code stranded on a feature branch — `main` must always hold the latest approved code.
- **Remote:** `origin` = `https://github.com/SidGajera/Claude_Lucent_Image_Gen.git`. The GitHub rename redirect can rewrite origin to `Jewelery-Website`; if a push 404s, run `git remote set-url origin https://github.com/SidGajera/Claude_Lucent_Image_Gen.git` and retry.
- Commit trailers (Co-Authored-By + Claude-Session) still apply. Nothing is git-ignored (per user request; still never commit real secrets/.env).

## 1. LAZY-LOADING MAP (load only what the current task needs; unload after extracting the rules)
| Task | Load ONLY |
|---|---|
| **Normal image generation** | `config/project_manifest.json` + `prompts/07_PROMPTS.md` + `config/QUALITY_MEMORY.json` (the runtime trio — self-sufficient for generation) |
| Image-generation rule detail | `docs/03_IMAGE_GENERATION_RULES.md` |
| Logo issue | `docs/04_LOGO_WORKFLOW.md` |
| Studio camera angles | `docs/12_STUDIO_ANGLES_STANDARD.md` |
| Jewelry geometry preservation / CAD fidelity / QA checklist | `docs/13_JEWELRY_PRESERVATION_SPEC.md` |
| Invented components (pavé bridge / hidden halo / gallery diamonds) / difference detector | `docs/16_ZERO_JEWELRY_INVENTION.md` |
| No-regression policy / golden suite / rollback / change discipline | `docs/14_NO_REGRESSION_POLICY.md` |
| Pipeline versioning / mode switch / rollback / shadow test / fallback / learning store | `docs/15_SAFE_PIPELINE_VERSIONING.md` (+ `config/pipeline_versions.json`) |
| Token / preview / commit / reasoning / response-length precedence (governs all) | `docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md` |
| Confirmation / auto-selection / when to ask the user | `docs/19_ZERO_CONFIRMATION_POLICY.md` |
| Production output / silence / no preview (governs all output) | `docs/20_ZERO_INTERNAL_OUTPUT_POLICY.md` |
| Background/cloth question | `docs/11_BACKGROUND_STANDARD.md` |
| Prompt writing/editing | `prompts/07_PROMPTS.md` (per-shot deltas) + `prompts/00_MASTER_SYSTEM_PROMPT.md` (fixed system layer) |
| Master system prompt (reused every generation) | `prompts/00_MASTER_SYSTEM_PROMPT.md` |
| Prevent past failures / update learning | `config/QUALITY_MEMORY.json` (+ `docs/06_CACHE.md` for Drive IDs) — do not keep permanently in context |
| Version info | `config/VERSION.json` |
| Current status | `docs/10_CURRENT_STATE.md` |
| Project history / rollback / version compare | `docs/09_CHANGELOG.md` |
| New workflow / architecture / global standard change | `docs/01_MASTER_SPECIFICATION.md` (+ `docs/02_SYSTEM_RULES.md`) |
| Project recovery | `RECOVERY.md` |
| Folder structure | `docs/08_PROJECT_STRUCTURE.md` |

Rules: never load the whole repository; load the **smallest** relevant file; after extracting the needed rules, discard unused sections from working memory. Reducing loaded context must NEVER reduce output quality — if you need more, load one more small file, never the whole repo. Never preload documentation, history, or archived files.

## 2. OPERATING PRINCIPLES (mandatory)
1. **The repository is the single source of truth.** Behavior comes from these files, not from memory of any prior chat.
2. **Never invent missing rules.** If something is not specified here, ask the user — do not guess or fill gaps.
3. **Preserve the exact approved image-generation workflow.** Do not change image-quality rules, logo rules, background rules, or workflow behavior.
4. **Use the locked logo and approved white-cloth assets** in `assets/logo/` and `assets/background/`. The logo is NEVER AI-rendered — it is composited from `assets/logo/logo_official.png` to look printed on the cloth (see `docs/04_LOGO_WORKFLOW.md`).
5. **One approval image per catalog, then auto-batch (user-locked 2026-07-16).** Each catalog (new SKU / source ring) is independent. Generate ONLY Image 1; collect corrections and regenerate Image 1 until the user EXPLICITLY approves it — generate nothing else for the catalog until then. On approval, LOCK Image 1 as the master standard (freeze geometry, stones, prongs, halo, gallery, band, metal thickness, camera, lighting, cloth, logo placement + print quality, QC rules) and AUTOMATICALLY generate all remaining images in one run, applying every learned correction — never re-ask per image unless a CRITICAL error appears. A new SKU RESETS the workflow. Exactly ONE approval per catalog; never approval-per-image; never batch before Image 1 is approved. Full detail: `docs/10_CURRENT_STATE.md` "CATALOG APPROVAL WORKFLOW".
6. **Silent, low-token execution.** No preview tools (`show_generations`/`job_display`), no narration per image, compact full-quality prompts, reuse cached assets, batch generations, report count only. Governed by `docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md` (the single token-optimization policy).

## 3. HARD RULES (never break — priority order in `docs/02_SYSTEM_RULES.md`)
- **P0 Logo:** locked asset; never regenerate/redraw/verify-read/recolor; always composited to look printed on cloth (never a floating overlay/sticker; partial crop/occlusion OK; off-center).
- **P1 Jewelry:** 100% identical to the correct source; never add/remove/resize/recolor stones or alter setting/band/metal.
- **P2 Diamonds:** single real facet pattern, natural bright+dark mix, no doubling/CGI; gems keep exact color/cut.
- **P3 Background:** never AI-invent the cloth — locked premium white COTTON with natural soft draping, pure neutral white (never yellowish/flat/simple); consistent every image.
- **P4 Light:** natural/realistic only; no over-lighting/CGI glow/starburst.
- **P5 Output:** always 1:1 and 2K.
- **P6 Lifestyle:** cozy warm US-home; five-finger natural hand; no laptop/desk; no invented logo.
- **P7 Tokens / P8 Communication:** as in docs 05; fix our own mistakes locally (0 credits), never burn credits on them.

## 4. ENVIRONMENT
- Higgsfield MCP: `nano_banana_2`, `resolution:"2k"`, `aspect_ratio:"1:1"`, 2 credits/image. medias `[reference, SOURCE]`.
- Google Drive MCP: READ/SEARCH/CREATE. Operate ONLY as `lucentcaratlab@gmail.com`.
- Local Python (Pillow+NumPy) for 0-credit post: `scripts/print_logo_on_cloth.py` (print logo) and `whiten_cloth.py` (neutral-white cloth).
- `media_id`s expire across sessions → re-import from the Drive file IDs in `docs/06_CACHE.md`.

## 5. PER-SKU LOOP (summary — full detail in `docs/10_CURRENT_STATE.md`)
Search source → study the ring (verify correct file) → import source → reuse studio refs, import fresh lifestyle/closeup poses → **1 verification image → user confirms → generate the rest in one batch** (studio on clean cloth, NO logo) → report count → user downloads → run `print_logo_on_cloth.py` + `whiten_cloth.py` locally → update docs + commit.

## 6. START
Operating from this file as the entry point (single source of truth), lazy-load per §1 only when a task needs it, then wait for the user's instruction (e.g. "go for 0XXX folder"). Do not preload the rest of the repo.
