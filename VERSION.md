# VERSION

- **Version:** 1.1.0 — "Stable Milestone: Portable Export + Printed-Logo Policy"
- **Date:** 2026-07-10
- **Commit:** `ec4c8658782d0789fad0d8df60e50313f5336a9f` (v1.1.0 docs on top of website base 97a701d)
- **Repo:** https://github.com/SidGajera/Claude_Lucent_Image_Gen (private, branch `main`)

## Major improvements in 1.1.0
- Logo policy finalized: **printed-on-cloth** compositing from a LOCKED asset (`assets/logo/logo_official.png`); AI never renders the logo. Added `scripts/print_logo_on_cloth.py` + `assets/logo/logo_official_transparent.png`.
- **Master Background Standard** locked (cloth material + neutral-white color + fold/texture consistency).
- Output standardized to **1:1 / 2K** for all images.
- Canonical base prompt + 10 token-optimization rules locked.
- **Full portable documentation** exported to `docs/` + `NEW_PROJECT.md` / `RECOVERY.md` / `README.md`, so the project reproduces from the repo alone.
- Catalogs this cycle: LR-0156, LR-0136, LR-0137.

## Version history
- **1.1.0** (2026-07-10) — this milestone.
- **1.0.0** — initial repo checkpoint; `LUCENT_MASTER.md` + `whiten_cloth.py`; website base initial commit `97a701d`.
