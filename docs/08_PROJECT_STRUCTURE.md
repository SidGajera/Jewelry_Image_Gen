# 08 — PROJECT STRUCTURE

## REPOSITORY (github.com/SidGajera/Claude_Lucent_Image_Gen)
```
/
├── LUCENT_MASTER.md              # Canonical merged master spec (single source of truth, §0–§14)
├── README.md                     # Index + quick start
├── NEW_PROJECT.md                # How to bootstrap a brand-new Claude project to reproduce this
├── RECOVERY.md                   # How to restore/continue after cloning the repo
├── VERSION.md                    # Version number, commit hash, date, major improvements
├── logo_official.png             # LOCKED brand logo — exact user upload (never modify)
├── logo_official_transparent.png # Background-keyed logo for compositing (ink pixels preserved)
├── whiten_cloth.py               # 0-credit local script: force pure neutral-white cloth
├── scripts/
│   └── print_logo_on_cloth.py    # 0-credit local script: print the logo onto the cloth
├── docs/
│   ├── 01_MASTER_SPECIFICATION.md
│   ├── 02_SYSTEM_RULES.md
│   ├── 03_IMAGE_GENERATION_RULES.md
│   ├── 04_LOGO_WORKFLOW.md
│   ├── 05_TOKEN_OPTIMIZATION.md
│   ├── 06_CACHE.md
│   ├── 07_PROMPTS.md
│   ├── 08_PROJECT_STRUCTURE.md   # (this file)
│   ├── 09_CHANGELOG.md
│   ├── 10_CURRENT_STATE.md
│   └── 11_BACKGROUND_STANDARD.md
├── index.html / app.js / styles.css / hero_jewelry.png  # (pre-existing website files; not part of the image pipeline)
└── .gitignore
```
> The website files (`index.html`, `app.js`, `styles.css`, `hero_jewelry.png`) were the initial checkpoint content and are unrelated to the image-generation workflow.

## GOOGLE DRIVE (external, durable — see docs/06_CACHE.md for IDs)
```
Lucent (parent)
├── Source parent            → per-SKU subfolders (LR-XXXX) with product images
├── Studio/Office references → Offie_photoshoot (1..5) branded white-cloth+logo
├── Home Lifestyle references→ Reference_US_Ring (wider) + Closup_houselifestyle (macro)
├── Output                   → finished catalog images
├── Logo asset folder        → Lucent Carat Lab Logo.png (official)
├── Tracking sheet / Auto log sheet
```

## EXTERNAL SERVICES
- **Higgsfield MCP** — image generation (`generate_image`, `media_import_url`, `balance`, `transactions`). Model `nano_banana_2`, 2 credits / 2K image.
- **Google Drive MCP** — `search_files`, `download_file_content`, `read_file_content`, `create_file` (READ/SEARCH/CREATE only; cannot edit/delete).
- **GitHub MCP / git** — repo `SidGajera/Claude_Lucent_Image_Gen` (private).

## SESSION-EPHEMERAL (not durable)
- Higgsfield `media_id`s (re-import from Drive IDs when expired).
- Scratchpad working files (decoded source PNGs, crops) — regenerate as needed.
