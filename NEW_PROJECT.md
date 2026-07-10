# NEW_PROJECT.md — Initialize a brand-new Claude project to reproduce this exactly

Follow these steps to recreate identical behavior, quality, workflow, and outputs in a fresh Claude project. Assume no memory of prior conversations — everything needed is in this repository.

## STEP 0 — CONNECTORS / TOOLS REQUIRED
- **Higgsfield MCP** (image generation): model `nano_banana_2`, 2 credits / 2K image. Needs `generate_image`, `media_import_url`, `balance`, `transactions`.
- **Google Drive MCP** (READ/SEARCH/CREATE): `search_files`, `download_file_content`, `read_file_content`, `create_file`.
- **GitHub MCP or git** with access to `SidGajera/Claude_Lucent_Image_Gen`.
- Local Python 3 with `pillow` + `numpy` (for the 0-credit local scripts).
- Operate ONLY as `lucentcaratlab@gmail.com`.

## STEP 1 — LOAD THE RULES (in order)
Read and internalize, in priority order:
1. `LUCENT_MASTER.md` (root) — full canonical spec.
2. `docs/02_SYSTEM_RULES.md` — permanent rules + priority order (P0–P8).
3. `docs/04_LOGO_WORKFLOW.md` — the locked logo + printed-on-cloth policy (P0).
4. `docs/11_BACKGROUND_STANDARD.md` — locked cloth.
5. `docs/03_IMAGE_GENERATION_RULES.md`, `prompts/07_PROMPTS.md`, `docs/05_TOKEN_OPTIMIZATION.md`, `docs/06_CACHE.md`.

## STEP 2 — KICKOFF MESSAGE (paste to the new Claude)
> Continuing Lucent Carat Lab catalog image generation. Read this repo's `LUCENT_MASTER.md` and `docs/` fully and follow every rule in priority order. Account: `lucentcaratlab@gmail.com`. Tool: Higgsfield `nano_banana_2`, 2K, 1:1, 2 credits/image. Source SKU parent `1mKqVAi2iv_35zs12jn91UYaeX2vKGdyy`; studio refs `1A9UJJcnlVA1Tvohd6Wa8O57eenCb7sQ2`; lifestyle refs `1GFwd4SHSPuCoaQj2WHYJWb7nTsvFUPzi`; logo asset `assets/logo/logo_official.png` (Drive `1QZgjplaFWenZHt048tzQntk-L-Ezy_qH`). 12 images per SKU = 5 studio + 4 lifestyle + 3 closeup, all 1:1/2K. HARD RULES: (P0) logo is a LOCKED asset, NEVER AI-rendered — generate studio on clean white cloth then composite the printed logo locally with `scripts/print_logo_on_cloth.py`; (P1) ring 100% identical to the correct source; (P2) diamonds single real facet pattern, no doubling/CGI, gems keep their color; (P3) locked white cloth, neutral white; natural light; (P7) reuse cache, batch, no preview tools. media_ids expire → re-import from the Drive file IDs in `docs/06_CACHE.md`. Confirm you've read it, then wait for the next SKU ("go for 0XXX folder").

## STEP 3 — PER-SKU LOOP (see docs/10_CURRENT_STATE.md)
Search source → study ring → import source → import fresh pose refs (reuse studio refs) → fire all 12 in one batch (clean cloth, no logo in studio) → report count → user downloads → run `whiten_cloth.py` + `scripts/print_logo_on_cloth.py` locally.

## STEP 4 — NON-NEGOTIABLES
- Never let the AI draw the logo. Never modify the jewelry design. Never change the cloth material/color. Always 1:1/2K. Never use preview tools. Never spend credits fixing our own mistakes if a local fix works.

## STEP 5 — KEEP DOCS CURRENT
After each SKU, update `LUCENT_MASTER.md` progress + `docs/06_CACHE.md` + `docs/09_CHANGELOG.md`, and commit to the repo. The repo — not chat memory — is the source of truth.
