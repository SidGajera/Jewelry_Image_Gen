# POLICY — GENERATED from policy/registry.json (DO NOT EDIT)

Read-only projection of the rule registry. Edit `policy/registry.json`, then run `python policy/gen_policy.py`. `policy/check.py` runs before every catalog and STOPs on conflicts.

**27 rules active** · 23 enforced by gates · 4 advisory (empty enforced_by) · 3 superseded (kept for provenance).

Precedence: 100 source fidelity · 90 platform compliance · 80 physical plausibility · 50 user preference · 10 doc defaults. Higher wins; the loser is superseded, never deleted.

## Active rules

| ID | Prec | Statement | Enforced by | Origin |
|---|---|---|---|---|
| `METAL_SOURCE_GOVERNED` | 100 | metal read from source into specs/<SKU>.json; no document-level default; 14K only a tiebreaker when source ambiguous AND Etsy title says 14K | spec_source_read | user 2026-07-30 |
| `SOURCE_FIDELITY` | 100 | the source CAD is the only truth; AI redraw disabled; geometry from source pixels only | G2_ACCENT_COUNT, G3_ACCENT_SIZE, G4_ACCENT_RUN, G5_SETTING_STYLE, G6_STONE_RATIO, G7_SETTING_COUNT, G8_UNAUTHORIZED, G9_PIECE_COUNT | user 2026-07-17 |
| `CONTENT_ETSY` | 90 | jewellery is the subject; no kissing/faces-in-contact/embrace/suggestive; couple never outweighs the ring | G14_CONTENT | user 2026-07-30 |
| `LOGO_LOCKED` | 90 | the Lucent logo is only the locked composited asset on studio cloth; AI never draws a logo; no AI text on studio renders | G11_LOGO | user 2026-07-16 |
| `MARKS_EXCLUDE` | 90 | exclude any source watermark/hallmark/vendor/engraved mark; inner shank plain; only the official Lucent logo permitted | G12_MARKS | user 2026-07-30 |
| `PLAUSIBILITY_L1_CONTINUITY` | 80 | band arms both terminate on the same finger/wrist; band crossing an inter-finger gap = FAIL; bracelet must close | G15_HAND_ANATOMY | user 2026-07-30 |
| `PLAUSIBILITY_L2_PLACEMENT` | 80 | ring centre between MCP and PIP of one finger; webbing/over-knuckle/past-fingertip = FAIL | G15_HAND_ANATOMY | user 2026-07-30 |
| `PLAUSIBILITY_L3_ANATOMY` | 80 | MediaPipe: 5 digits, correct joints, detection confidence >0.8; fused/extra/missing digits or impossible thumb = FAIL | G15_HAND_ANATOMY | user 2026-07-30 |
| `PLAUSIBILITY_L4_L8_VISUAL` | 80 | support/gravity, occlusion, light consistency, scale, reflection sanity â€” mandatory visual checklist on EVERY render until automated | _advisory_ | user 2026-07-30 |
| `REFS_REAL_PHOTO` | 80 | every lifestyle reference is a real camera photograph (no AI/render), unambiguous one-finger placement, real skin detail | refs_preflight | user 2026-07-30 |
| `SKIN_REALISM` | 80 | exposure-normalized skin high-frequency energy above threshold; plastic/over-smoothed skin = FAIL | G16_SKIN_REALISM | user 2026-07-30 |
| `ANGLE_NUMERIC_MATRIX` | 50 | camera defined by numeric azimuth/elevation/crop per slot; filenames carry no geometry; within-group pairwise separation 20az/15el | G10_ANGLE, refs_preflight | user 2026-07-30 |
| `ANGLE_STUDIO_SLOTS` | 50 | ring studio 4 = top_down, true_side (edge-on stone), front_elevation, gallery_back (rear 3/4, filigree gallery + back of shank); gallery_back replaces macro_head | G10_ANGLE | user 2026-07-30 |
| `AUTONOMY_RUN` | 50 | permissions granted once; run every catalog end-to-end with no check-ins; internal output only; user reviews after completion | run_catalog | user (19+20) |
| `BACKGROUND_VELVET` | 50 | studio background is premium plain pure-white velvet only; plain, no AI-generated cloth | _advisory_ | docs 11 |
| `COUNTS_4_6` | 50 | exactly 4 studio (white velvet) + 6 lifestyle; one image per angle/pose | slot_manifest | user 2026-07-28 |
| `FORMAT_ASPECT` | 50 | 1:1 square, 2048x2048 minimum, native, no upscale | G1_FORMAT | user 2026-07-30 |
| `FROZEN_CALL` | 50 | Higgsfield generation call frozen: text-to-image, 2k/1:1/count1/one batch, medias [pose/studio ref, SOURCE piece]; no img2img/denoise/compositing of jewelry (accent-run composite exception approved) | run_catalog | user 2026-07-30 |
| `GEN_ENGINE_LOCK` | 50 | Higgsfield MCP is the only production image-generation engine; never swap providers | run_catalog | user (21) |
| `OUTPUT_STORE` | 50 | all render outputs live in the single store deliveries/<SKU>/ (gitignored); images never committed | run_catalog | user 2026-07-30 |
| `PIPELINE_SOP` | 50 | per-catalog order P0-P9: source gate -> spec -> prompts -> frozen batch -> validate -> retry -> download(deliveries/) -> manifest -> failure memory -> commit+push | run_catalog | user (22) |
| `REALISM_ANTI_AI` | 50 | genuine photography, varied non-generic models/wardrobe; banned beige/cream/oatmeal knit, neutral couch, seamless backdrop in a lifestyle frame | G16_SKIN_REALISM | user (24 P6) |
| `REFS_PER_SLOT` | 50 | medias[0] is a distinct per-slot reference from refs/<SKU>/; --stage prompts hard-fails if any missing | refs_preflight | user 2026-07-30 |
| `REGRESSION_NO_REGRESS` | 50 | quality only ratchets up; a gate that stops catching a past failure fails the build; goldens are permanent | regression_suite | user (14+15) |
| `SUBAGENT_BAN` | 50 | never spawn subagent/background-task/agent; read source in-thread once; no gallery-display widgets; job_display retrieval only, one pass per catalog | preflight | user 2026-07-30 |
| `THEME_PER_CATALOG` | 50 | one coherent theme within a catalog; a different theme per catalog rotated by SKU hash | _advisory_ | user (24 P5) |
| `TOKEN_BUDGET` | 50 | <=15k tokens per catalog; savings come only from what is displayed, never from source fidelity, prompt detail, or validation | _advisory_ | user (05+17) |

## Superseded rules (provenance — never deleted)

| ID | Statement | Superseded by |
|---|---|---|
| `ANGLE_STUDIO_MACRO_HEAD` | studio slot 04 = macro_head | `ANGLE_STUDIO_SLOTS` |
| `FORMAT_PORTRAIT` | all images portrait | `FORMAT_ASPECT` |
| `METAL_DEFAULT_18K` | default 18K natural yellow gold unless source otherwise | `METAL_SOURCE_GOVERNED` |

## Advisory rules (empty enforced_by — not machine-verified)

- `PLAUSIBILITY_L4_L8_VISUAL` — support/gravity, occlusion, light consistency, scale, reflection sanity â€” mandatory visual checklist on EVERY render until automated
- `TOKEN_BUDGET` — <=15k tokens per catalog; savings come only from what is displayed, never from source fidelity, prompt detail, or validation
- `BACKGROUND_VELVET` — studio background is premium plain pure-white velvet only; plain, no AI-generated cloth
- `THEME_PER_CATALOG` — one coherent theme within a catalog; a different theme per catalog rotated by SKU hash
