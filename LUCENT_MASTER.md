# LUCENT CARAT LAB — PROJECT MASTER

**Ownership:** this file owns **project vision, business rules, architecture, folder structure and references**.

It is **not** the runtime entry point and **not** a policy authority. It states *what* the project is and *why*; it never restates *how* a rule is executed — the owning document does that, and wins on any conflict.

| Concern | Owner |
|---|---|
| Vision · business rules · architecture · folder structure · references | **this file** |
| AI runtime · startup order · loading order · execution rules · token policy | [`CLAUDE_SETUP.md`](CLAUDE_SETUP.md) |
| Machine-readable runtime configuration | [`config/runtime.json`](config/runtime.json) |

The **repository as a whole** is the single source of truth. No individual file is.

---

## 1. PROJECT VISION

A portable, reproducible system that turns a jewelry SKU's source CAD renders into a **12-image marketing catalog**, with the jewelry **100% identical to the source**, on the brand's locked white studio cloth, carrying the exact Lucent Carat Lab logo.

Any session can clone this repository and reproduce the approved workflow with no other context. Behavior comes from these files — never from chat history.

## 2. BUSINESS RULES

Non-negotiable commitments. Execution detail lives in the owning docs (§5).

- **The jewelry is the product.** It must be 100% identical to the correct source CAD — design, stones, prongs, gallery, basket, band, proportions. Nothing changes without permission. Only photography changes: camera, lighting, background, environment. *(→ `docs/13`, `docs/16`)*
- **Verify the source before generating.** Use the correct source file; ignore stray or mislabeled images. If the source cannot be verified, do not generate. *(→ `docs/19` §2)*
- **A rejected image is acceptable; a redesigned ring is not.** Act as a QC inspector whose job is to reject drift, not to produce a nicer picture. *(→ `docs/18`)*
- **The logo is a preserved asset, never AI-rendered.** Exact asset composited to read as printed into the cloth, or omitted. Missing is acceptable; incorrect is not. *(→ `docs/04`)*
- **The cloth is a locked asset, never AI-invented.** Premium neutral-white cotton, natural draping, consistent across every image. *(→ `docs/11`)*
- **Catalog shape:** 12 images per SKU — 5 studio, 4 lifestyle, 3 close-up. All 1:1, all 2K, no exceptions. *(→ `docs/03`, `docs/12`)*
- **One approval per catalog.** Generate image 1, iterate until explicitly approved, lock it as the standard, then auto-batch the remainder. Never approval-per-image; never batch before approval. *(→ `CLAUDE_SETUP.md` §2.5)*
- **Quality is never traded for tokens.** Optimize by loading less — never by lowering resolution, model, verification depth, or QC. *(→ `docs/17`)*
- **Operate only as `lucentcaratlab@gmail.com`.** Cost basis: 2 credits per image; local post-processing is 0 credits.
- **`main` is the only branch.** No feature branches or PR workflow without explicit permission. *(→ `CLAUDE_SETUP.md` §0.5)*

## 3. ARCHITECTURE

**Startup.** A session reads `CLAUDE_SETUP.md` and nothing else, then lazy-loads exactly one file per task from its §1 map. The repository is modular specifically to keep context small.

**Generation pipeline.**

```
Drive source (SKU CAD)  ─┐
                         ├─→ media_import_url ─→ Higgsfield generate_image ─→ clean-cloth render
Drive pose reference   ──┘        (production model, 1:1, 2K)                          │
                                                                                    ▼
                                                            local composite (0 credits, Pillow)
                                                            print_logo_on_cloth.py → whiten_cloth.py
                                                                                    │
                                                                                    ▼
                                                              QC gate → approve → Drive Output + commit
```

The studio render is a **logo-free intermediate** by design. The logo is applied locally from the locked asset — never prompted, never AI-drawn.

**Layers.** Policy (`docs/`) · prompts (`prompts/`) · machine config (`config/`) · locked assets (`assets/`) · local tooling (`scripts/`, `tool/`).

**State.** `config/QUALITY_MEMORY.json` records verified failures and permanent fixes. `docs/06_CACHE.md` holds durable Drive file IDs — Higgsfield `media_id`s are session-ephemeral and must be re-imported.

## 4. FOLDER STRUCTURE

Top-level orientation only. **File-by-file detail is owned by [`docs/08_PROJECT_STRUCTURE.md`](docs/08_PROJECT_STRUCTURE.md)** — this section never duplicates it.

```
Lucent-Carat-Lab/
├── CLAUDE_SETUP.md      # runtime entry point — read this first
├── LUCENT_MASTER.md     # this file — vision, business rules, architecture
├── README.md            # orientation · NEW_PROJECT.md · RECOVERY.md · VERSION.md
├── docs/                # policy documents (01-20), one topic per file
│   └── archive/         # superseded documents — never loaded
├── prompts/             # 00 master system prompt · 07 per-shot deltas
├── config/              # machine-readable: manifest, runtime, VERSION, QUALITY_MEMORY
├── assets/              # locked logo + background — byte-preserved
├── scripts/             # local 0-credit post-processing
├── tool/                # backend service
└── workspace/           # golden baselines
```

## 5. REFERENCES

| Topic | Owner |
|---|---|
| Runtime, startup, loading order, agent behavior | `CLAUDE_SETUP.md` |
| Machine-readable runtime config | `config/runtime.json` |
| Full specification · system rules | `docs/01` · `docs/02` |
| Image generation rules | `docs/03` |
| Logo workflow (preserved asset) | `docs/04` |
| Drive ID cache | `docs/06` |
| Folder structure (detailed) | `docs/08` |
| Changelog — authoritative version history | `docs/09` |
| Current state · catalog approval workflow | `docs/10` |
| Background / cloth standard | `docs/11` |
| Studio camera angles | `docs/12` |
| Jewelry geometry preservation | `docs/13` |
| No-regression policy | `docs/14` |
| Safe pipeline versioning | `docs/15` |
| Zero jewelry invention | `docs/16` |
| Token optimization policy | `docs/17` |
| Zero-tolerance QC | `docs/18` |
| Zero-confirmation execution | `docs/19` |
| Zero internal output (production) | `docs/20` |
| Prompts | `prompts/00` · `prompts/07` |
| Pre-split historical snapshot (archived, not authoritative) | `docs/archive/LUCENT_MASTER_LEGACY_2026-07-16.md` |
