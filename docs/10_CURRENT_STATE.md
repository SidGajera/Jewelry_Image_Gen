# 10 — CURRENT STATE (exact current workflow)

As of 2026-07-10 (v1.1.0). This is precisely what happens for a new SKU today.

## PER-SKU WORKFLOW (current, exact)
1. **Locate source:** `search_files` in source parent `1mKqVAi2iv_35zs12jn91UYaeX2vKGdyy` for `title contains '<SKU#>'` → get the SKU folder → `search_files` for its images.
2. **Study the ring:** `download_file_content` on the top view (and one side view) → decode base64 to PNG locally → view. Identify: center cut, side stones (type/color/cut/count), prongs, band, metal, gallery. Use the CORRECT file; ignore strays.
3. **Log the design** in `LUCENT_MASTER.md` (§14 product codes) + `docs/06_CACHE.md`.
4. **Import source** once: `media_import_url("https://drive.google.com/uc?id=<SRC_ID>&export=download")` → source media_id.
5. **References:**
   - Studio: reuse the 5 branded `Offie_photoshoot` refs (re-import from Drive IDs if media_ids expired).
   - Lifestyle + closeup: import DIFFERENT pose files than the previous SKU (from `Reference_US_Ring` + `Closup_houselifestyle`).
6. **Generate all 12 in ONE batch** — `generate_image`, `model:"nano_banana_2"`, `resolution:"2k"`, `aspect_ratio:"1:1"`, `count:1`, medias `[reference, source]`. Prompts = canonical base + group wrapper + SKU design string (docs/07). **Studio prompts force clean cloth with NO logo.**
7. **Report count only.** No preview tools.
8. **Local post-processing (user runs on downloaded outputs, 0 credits):**
   - `whiten_cloth.py` if any cloth drifted warm.
   - `scripts/print_logo_on_cloth.py` on the 5 studio shots to print the locked logo onto the cloth.
9. **Deliver** to Drive Output folder; update tracking log.

## KEY DECISIONS IN FORCE
- Logo: NEVER AI-rendered; ALWAYS composited from `logo_official.png` to look printed on cloth (P0).
- Cloth: locked material + neutral white; consistent every image (P3).
- Jewelry: 100 % identical to source (P1). Diamonds: single facet pattern, no doubling (P2).
- Format: 1:1, 2K always (P5).
- Lifestyle: cozy US-home, no laptop/desk (P6).
- Efficiency: reuse cache, batch, no previews, compact full-quality prompts (P7).

## GENERATION MECHANICS / GOTCHAS
- `generate_image` requires `params.model` and (for 2K) explicit `params.resolution:"2k"` — default is 1k.
- Response may show `model:"nano_banana_flash"` for the multi-image edit path; that is expected — `resolution:"2k"` is what governs quality/credits.
- Higgsfield outputs live on CloudFront and are network-blocked for us to download; the user downloads them and runs the local scripts.
- `media_id`s expire across sessions → re-import from Drive IDs.

## PROGRESS
- Repo `SidGajera/Claude_Lucent_Image_Gen` live (private, `main`), documentation exported.
- Latest SKUs: LR-0156, LR-0136, LR-0137. (Full history in `LUCENT_MASTER.md`.)

## OPEN / NEXT
- Continue new SKUs on request ("go for 0XXX folder").
- For studio shots, apply the printed-logo composite locally after download (the 5 studio shots of LR-0137 were generated logo-free and await the local logo print).
