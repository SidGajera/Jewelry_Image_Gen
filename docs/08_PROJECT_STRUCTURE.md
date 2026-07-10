# 08 — PROJECT STRUCTURE

## REPOSITORY (github.com/SidGajera/Claude_Lucent_Image_Gen — portable template)
```
/
├── CLAUDE_SETUP.md               # SINGLE ENTRY POINT — a new Claude session reads this first
├── README.md                     # Index ("Start here: open CLAUDE_SETUP.md")
├── NEW_PROJECT.md                # Bootstrap a brand-new Claude project to reproduce this
├── RECOVERY.md                   # Restore/continue after cloning the repo
├── VERSION.md                    # Version number, commit hash, date, major improvements
├── LUCENT_MASTER.md              # Canonical merged master spec (§0–§14)
├── whiten_cloth.py               # 0-credit local script: force pure neutral-white cloth
├── docs/
│   ├── 01_MASTER_SPECIFICATION.md
│   ├── 02_SYSTEM_RULES.md
│   ├── 03_IMAGE_GENERATION_RULES.md
│   ├── 04_LOGO_WORKFLOW.md
│   ├── 05_TOKEN_OPTIMIZATION.md
│   ├── 06_CACHE.md
│   ├── 08_PROJECT_STRUCTURE.md   # (this file)
│   ├── 09_CHANGELOG.md
│   ├── 10_CURRENT_STATE.md
│   └── 11_BACKGROUND_STANDARD.md
├── prompts/
│   └── 07_PROMPTS.md             # reusable prompts
├── scripts/
│   └── print_logo_on_cloth.py    # 0-credit local script: print the logo onto the cloth
├── assets/
│   ├── logo/
│   │   ├── logo_official.png             # LOCKED brand logo — exact upload (never modify)
│   │   ├── logo_official_transparent.png # Background-keyed logo for compositing
│   │   └── README.md                     # checksums + Drive origin
│   ├── background/
│   │   ├── sample_studio_background_with_logo.png
│   │   └── README.md                     # locked cloth standard + Drive refs
│   └── references/
│       └── README.md                     # pose/source reference index (Drive IDs)
├── config/
│   └── project_manifest.json     # machine-readable manifest (version, files, assets, checksums, setup order)
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
