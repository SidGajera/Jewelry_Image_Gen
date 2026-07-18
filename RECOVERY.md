# RECOVERY.md — Restore / continue the project from GitHub

Use this when a session/container was reclaimed, or you're picking the project up fresh from the repo. **Recovery uses ONLY this repository — no Git tags, no external state, no prior chat memory.** (Git tags cannot be pushed from the generating environment; the repo is self-describing via `config/VERSION.json`.)

## 0. RECOVER USING ONLY THIS REPOSITORY (authoritative sequence)
1. `git clone https://github.com/SidGajera/Claude_Lucent_Image_Gen.git && cd Claude_Lucent_Image_Gen`
2. Open **`config/VERSION.json`** — read `current_version`, `latest_commit_hash`, `branch`, `entry_file`, `minimum_required_files`.
3. Confirm you are on the right commit: `git rev-parse HEAD` should match `latest_commit_hash` (or be newer on `main`).
4. Open the entry file **`CLAUDE_SETUP.md`** and follow it (it reads VERSION.json, verifies files, then reads the documented order).
5. Verify all `minimum_required_files` (and `config/project_manifest.json → required_files/required_assets`) exist. If any missing → STOP, report; the checkout is broken.
6. Treat the repo as the single source of truth. Do not rely on any previous conversation.

## 1. CLONE
```
git clone https://github.com/SidGajera/Claude_Lucent_Image_Gen.git
cd Claude_Lucent_Image_Gen
```

## 2. VERIFY THE LOCKED ASSETS ARE PRESENT
```
ls -la assets/logo/logo_official.png assets/logo/logo_official_transparent.png whiten_cloth.py scripts/print_logo_on_cloth.py
```
- `assets/logo/logo_official.png` must be **1079081 bytes** (the exact official upload). If it differs, re-download from Drive id `1QZgjplaFWenZHt048tzQntk-L-Ezy_qH` — do NOT recreate it.
- If `assets/logo/logo_official_transparent.png` is missing/wrong, regenerate it (non-destructive key):
  ```
  pip install pillow numpy
  python scripts/print_logo_on_cloth.py --make-transparent --logo assets/logo/logo_official.png --out assets/logo/logo_official_transparent.png
  ```

## 3. RE-READ THE RULES
Read in order: `LUCENT_MASTER.md` → `docs/02_SYSTEM_RULES.md` → `docs/04_LOGO_WORKFLOW.md` → `docs/11_BACKGROUND_STANDARD.md` → `docs/10_CURRENT_STATE.md`. These fully define behavior; chat memory is not required.

## 4. RECONNECT SERVICES
- Higgsfield MCP (image gen), Google Drive MCP (READ/SEARCH/CREATE), GitHub/git.
- Operate as `lucentcaratlab@gmail.com`.

## 5. REBUILD EPHEMERAL STATE
- Higgsfield `media_id`s from earlier sessions are **expired**. Do not reuse them. Re-import from the durable **Drive file IDs** in `docs/06_CACHE.md` via `media_import_url` when you need them.
- Decoded source PNGs / crops in scratchpad are gone — re-download from Drive as needed.

## 6. RESUME WORK
- To continue a SKU already generated: check `LUCENT_MASTER.md` progress + `docs/09_CHANGELOG.md`. Do NOT regenerate completed catalogs (token rule #2).
- Studio shots awaiting the printed logo: run `scripts/print_logo_on_cloth.py` on the downloaded outputs.
- For a new SKU: follow `docs/10_CURRENT_STATE.md` per-SKU loop.

## 7. GIT
- Branch `main`, remote `origin = https://github.com/SidGajera/Claude_Lucent_Image_Gen.git`.
- Commit doc/asset changes after each SKU. Repo is the source of truth.

## 8. SANITY CHECKLIST BEFORE GENERATING
- [ ] Correct source file verified (ignore strays).
- [ ] The production model (`config/project_manifest.json`), `resolution:"2k"`, `aspect_ratio:"1:1"`.
- [ ] Studio prompts force clean cloth, NO logo.
- [ ] Fresh lifestyle/closeup poses (different from last SKU).
- [ ] Plan to composite the logo + whiten cloth locally (0 credits).
