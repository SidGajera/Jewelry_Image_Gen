# assets/logo — LOCKED brand logo

**Do not modify these files.** They are the protected brand asset (policy P0, see `docs/04_LOGO_WORKFLOW.md`).

| File | Purpose | SHA-256 | Bytes |
|---|---|---|---|
| `logo_official.png` | Exact official upload — pixel source of truth | `2e022162b5ff7b21ef30129cc4fac157a25e33464a4b6cf1f4f497f36a40f34f` | 1079081 |
| `logo_official_transparent.png` | Background-keyed derivative for compositing (ink pixels preserved) | `1b8dc7c37b9385f07efd589899483131beea2346b7f0386b3e4b5dd742aa1982` | 1174590 |

Drive origin of `logo_official.png`: `Lucent Carat Lab Logo.png`, file id `1QZgjplaFWenZHt048tzQntk-L-Ezy_qH`.

Regenerate the transparent version (non-destructive white-key) if ever needed:
```
python scripts/print_logo_on_cloth.py --make-transparent \
  --logo assets/logo/logo_official.png --out assets/logo/logo_official_transparent.png
```
