# RECOVERY.md — Restore / continue the project after cloning

Use this when a session/container was reclaimed, or you're picking the project up fresh from the repo.

## 1. CLONE
```
git clone https://github.com/SidGajera/Claude_Lucent_Image_Gen.git
cd Claude_Lucent_Image_Gen
```

## 2. VERIFY THE LOCKED ASSETS ARE PRESENT
```
ls -la logo_official.png logo_official_transparent.png whiten_cloth.py scripts/print_logo_on_cloth.py
```
- `logo_official.png` must be **1079081 bytes** (the exact official upload). If it differs, re-download from Drive id `1QZgjplaFWenZHt048tzQntk-L-Ezy_qH` — do NOT recreate it.
- If `logo_official_transparent.png` is missing/wrong, regenerate it (non-destructive key):
  ```
  pip install pillow numpy
  python scripts/print_logo_on_cloth.py --make-transparent --logo logo_official.png --out logo_official_transparent.png
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
- [ ] Model `nano_banana_2`, `resolution:"2k"`, `aspect_ratio:"1:1"`.
- [ ] Studio prompts force clean cloth, NO logo.
- [ ] Fresh lifestyle/closeup poses (different from last SKU).
- [ ] Plan to composite the logo + whiten cloth locally (0 credits).
