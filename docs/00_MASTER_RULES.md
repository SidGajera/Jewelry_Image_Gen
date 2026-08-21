# 00 — LUCENT CARAT LAB MASTER RULES (PERMANENT, every catalog, no exceptions)

Top authority + policy index. Missing any single rule below fails the catalog. Each section names its owner doc and the gate that enforces it. **To override FORMAT or METAL, edit the RESOLVED CONFLICTS box here only — everything reads from it.**

```
╔═ RESOLVED CONFLICTS ═══════════════════════════════════════════════╗
║ FORMAT = 1:1 SQUARE, 2048x2048 minimum.                            ║
║   Square wins (what G1 enforces; what the LR-0203 rejections       ║
║   assumed). Overrides any "portrait" note.                         ║
║ METAL  = SOURCE-GOVERNED. specs/<SKU>.json "metal" is the ONLY     ║
║   authority, read from the source CAD. No document-level default   ║
║   exists (docs/01 & docs/03 point here, never restate a value).    ║
║   14K is only a TIEBREAKER — used solely when the source is        ║
║   genuinely ambiguous AND the live Etsy title says 14K. Not a      ║
║   default. (LR-0203 white gold, LR-0206 yellow gold, from source.) ║
╚════════════════════════════════════════════════════════════════════╝
```

1. **SOURCE (blocking)** — read CAD first, confirm every angle, build full geometry before any prompt; AI redraw DISABLED; geometry traces to a source view, camera may be new; unclear/missing = STOP. → `docs/13` §6b, `docs/24` P0 · gate: `validate_source`.
2. **JEWELLERY FIDELITY** — D2D pixel-perfect (stone count/size/cut/facets/shape/proportions · prongs · halo · gallery · pavé · band · metal · finish); only camera + setting change. → `docs/13` · gates: G2–G9 (calibrating).
3. **FORMAT** — 1:1 2048² native min, tack-sharp, sRGB neutral WB, no filter/vignette/border/text/watermark; non-square discarded first. → `docs/24` P1 · gate: **G1 (blocking)**.
4. **COUNTS & COVERAGE** — 4 studio + 6 lifestyle, never 5/5; one image per angle/pose; camera as NUMBERS; `medias[0]` distinct per-slot ref from `refs/`. → `docs/12` A-MATRIX, `docs/24` P3/P4 · gates: **G10 + refs preflight (`--stage prompts`) + slot manifest (blocking)**.
5. **THEME** — one coherent theme per catalog, different per catalog (SKU-hash rotated). → `docs/24` P5, `project_catalog_visual_theme`.
6. **REALISM** — genuine photography, real skin/fabric/light, varied models/wardrobe; BANNED beige/cream/oatmeal knit + neutral couch + seamless backdrop in lifestyle; ring true-to-source scale. → `docs/24` P6, `docs/23` · gate: G9 scale (advisory), lifestyle realism prompt block.
7. **JEWELLERY IS THE SUBJECT** — sharpest/most prominent in every frame; people in shallow DoF; Etsy-compliant (no kissing/faces-in-contact/embrace/suggestive/couple-as-subject). → `docs/23` · gate: **G14 (blocking)**.
8. **MARKS & WATERMARKS** — source watermark/hallmark/vendor/engraved mark = source artifact, exclude losslessly; inner shank plain; only the official Lucent logo (composited from the locked asset) is permitted. → `docs/04`, `docs/24` P7 · gate: **G12 (blocking)**.
9. **ENGINE ORDER** — engine 1 `higgsfield` is the production default and the ONLY catalog-approved stills engine; engine 2 `openflow` (Google Flow bridge) is opt-in for video/exploration, never auto-selected, never a fallback, never writes a delivered image. → `docs/21`, `docs/26`, `config/engines.json` · gate: **`scripts/engine.py --check` (blocking, in regression)**.
10. **AUTONOMY** — permissions granted once in `.claude/settings.json`; never ask again; run every catalog end-to-end (source→spec→prompts→generate→download→gate→auto-retry→manifest→failure memory→commit→push); no check-ins; user reviews after completion. → `docs/19`, `feedback_subagent_ban_absolute`.
11. **COMPLETION (a claim)** — COMPLETE requires: all 10 rendered · all 10 downloaded · all blocking gates PASS · failures auto-retried+re-gated · spec+manifest+failure-memory pushed. Refuse COMPLETE unless every box checks; print unchecked boxes; state advisory count: `"LR-XXXX: 10/10 · N gates blocking, M advisory · pushed · COMPLETE"`; never imply geometry was verified when it wasn't. → `run_catalog.py --stage finish`.

**GATE MAP:** §3→G1 · §4→G10 + refs preflight + slot manifest · §6→G9 scale · §7→G14 · §8→G12 · §2→G2–G9 (calibrating; promote per gate on goldens via `scripts/calibrate.py` + `config/gates.json`). Blocking today: G1, G10, G11, G12, G14 (+pairwise). Advisory: G2–G9 until PASS goldens promote them.
