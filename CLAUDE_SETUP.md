# CLAUDE_SETUP.md — SINGLE ENTRY POINT

You are a new Claude session bootstrapping the **Lucent Carat Lab** catalog image-generation automation. This repository is the **single source of truth**. Follow this file first, then read the rest in the exact order below.

## 1. READ THESE FILES IN THIS EXACT ORDER
1. `CLAUDE_SETUP.md` (this file)
2. `docs/01_MASTER_SPECIFICATION.md`
3. `docs/02_SYSTEM_RULES.md`
4. `docs/03_IMAGE_GENERATION_RULES.md`
5. `docs/04_LOGO_WORKFLOW.md`
6. `docs/11_BACKGROUND_STANDARD.md`
7. `docs/05_TOKEN_OPTIMIZATION.md`
8. `docs/06_CACHE.md`
9. `prompts/07_PROMPTS.md`
10. `docs/10_CURRENT_STATE.md`

(Also available: `docs/08_PROJECT_STRUCTURE.md`, `docs/09_CHANGELOG.md`, `NEW_PROJECT.md`, `RECOVERY.md`, `VERSION.md`, `LUCENT_MASTER.md` — the full canonical merged spec.)

## 2. OPERATING PRINCIPLES (mandatory)
1. **The repository is the single source of truth.** Behavior comes from these files, not from memory of any prior chat.
2. **Never invent missing rules.** If something is not specified here, ask the user — do not guess or fill gaps.
3. **Preserve the exact approved image-generation workflow.** Do not change image-quality rules, logo rules, background rules, or workflow behavior.
4. **Use the locked logo and approved white-cloth assets** in `assets/logo/` and `assets/background/`. The logo is NEVER AI-rendered — it is composited from `assets/logo/logo_official.png` to look printed on the cloth (see `docs/04_LOGO_WORKFLOW.md`).
5. **One verification image, then batch.** For a new SKU, generate exactly ONE verification image, let the user confirm fidelity, then generate the remaining approved batch **without asking permission again**.
6. **Silent, low-token execution.** No preview tools (`show_generations`/`job_display`), no narration per image, compact full-quality prompts, reuse cached assets, batch generations, report count only. See `docs/05_TOKEN_OPTIMIZATION.md`.

## 3. HARD RULES (never break — priority order in `docs/02_SYSTEM_RULES.md`)
- **P0 Logo:** locked asset; never regenerate/redraw/verify-read/recolor; always composited to look printed on cloth (never a floating overlay/sticker; partial crop/occlusion OK; off-center).
- **P1 Jewelry:** 100% identical to the correct source; never add/remove/resize/recolor stones or alter setting/band/metal.
- **P2 Diamonds:** single real facet pattern, natural bright+dark mix, no doubling/CGI; gems keep exact color/cut.
- **P3 Background:** locked white cloth material + neutral white; consistent every image.
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
After reading the files above in order, confirm you have read them and are operating from the repository as the single source of truth, then wait for the user's SKU instruction (e.g. "go for 0XXX folder").
