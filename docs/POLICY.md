# POLICY — GENERATED from policy/registry.json (DO NOT EDIT)

Read-only projection of the rule registry. Edit `policy/registry.json`, then run `python policy/gen_policy.py`. `policy/check.py` runs before every catalog and STOPs on conflicts.

**31 rules active** · 23 enforced (blocking gate) · 8 observed (non-blocking gate / visual checklist) · 0 advisory (no gate) · 9 superseded.

Precedence: 100 source fidelity · 90 platform compliance · 80 physical plausibility · 50 user preference · 10 doc defaults. Higher wins; the loser is superseded, never deleted.

## Active rules

| ID | Prec | Statement | Enforced by | Origin |
|---|---|---|---|---|
| `HIGGSFIELD_ONLY` | 100 | ALL delivered pixels come from Higgsfield generate_image. Call shape frozen: medias [reference, SOURCE piece], 2k, 1:1, count 1, one batch per catalog. Python may NOT create or alter delivered pixels (no compositing, cutout-into-output, PIL paste, affine placement, relight, shadow synthesis, any pixel write). Python allowed only for read-only gates, spec/prompt building, download, manifests, failure memory, hashing, hygiene. Geometry enforcement = catch-and-retry: every render gated, any geometry fail auto-regenerates, max 5 rounds, then STOP and report. | run_catalog | user 2026-07-31 |
| `JEWELRY_PRESERVATION` | 100 | Jewellery redesign/redraw PROHIBITED: diamond shape/size/cut/facet/count/placement, prongs/setting/gallery/band and metalwork come ONLY from the source CAD, unchanged (target: D2D pixel-perfect), on EVERY image including lifestyle. Only the camera angle may change. Read ALL source angles before generating; never generate an angle without a source view. Materials must look 100% real (no plastic/CZ/CGI). Aspirational under HIGGSFIELD_ONLY (text-to-image cannot guarantee D2D); kept as the locked target and enforced where measurable (G22 scale, G20 framing, G12 marks, G-INVENT coverage). | G_INVENT, G20_MIN_SUBJECT_SCALE, G22_STONE_WITHIN_FINGER | user 2026-07-31 |
| `METAL_SOURCE_GOVERNED` | 100 | metal read from source into specs/<SKU>.json; no document-level default; 14K only a tiebreaker when source ambiguous AND Etsy title says 14K | spec_source_read | user 2026-07-30 |
| `PROCESS_NO_WIDGETS` | 100 | never spawn subagent/background-task/agent; read source in-thread once. NO Higgsfield widgets/galleries of any kind, INCLUDING job_display, show_generations, show_marketing_studio_generations, media_upload_widget or any gallery/grid/preview/widget tool. Take a generation's URL/ID only from its own result already in hand; the user previews results in Higgsfield. Silent operation: one short final status line, no in-chat image previews. | preflight | user 2026-07-31 |
| `SOURCE_COVERAGE_REQUIRED` | 100 | every item a studio slot reveals must be established by a supplied source view (config/view_coverage.json); + azimuth within 45deg; else block. No inference, no category priors, no defaults | G_INVENT | user 2026-07-30 |
| `SOURCE_FIDELITY` | 100 | the source CAD is the only truth; AI redraw disabled; geometry from source pixels only | G2_ACCENT_COUNT, G3_ACCENT_SIZE, G4_ACCENT_RUN, G5_SETTING_STYLE, G6_STONE_RATIO, G7_SETTING_COUNT, G8_UNAUTHORIZED, G9_PIECE_COUNT | user 2026-07-17 |
| `SOURCE_REF_CALL` | 100 | Higgsfield call feeds the matching source-CAD angle as a structure-lock REFERENCE (image-to-image / subject-preserve) so the exact ring geometry is held while only the scene changes; medias [pose/studio ref, SOURCE piece]; 2k/1:1/count1/one batch. Per HIGGSFIELD_ONLY, all delivered pixels come from Higgsfield and Python never composites/writes delivered pixels. Supersedes the earlier text-to-image/no-img2img call. | run_catalog | user 2026-07-31 |
| `CONTENT_ETSY` | 90 | jewellery is the subject; no kissing/faces-in-contact/embrace/suggestive; couple never outweighs the ring | G14_CONTENT | user 2026-07-30 |
| `LOGO_LOCKED` | 90 | the Lucent logo is only the locked composited asset on studio cloth; AI never draws a logo; no AI text on studio renders | G11_LOGO | user 2026-07-16 |
| `MARKS_EXCLUDE` | 90 | exclude any source watermark/hallmark/vendor/engraved mark; inner shank plain; only the official Lucent logo permitted | G12_MARKS | user 2026-07-30 |
| `PLAUSIBILITY_L1_CONTINUITY` | 80 | band arms both terminate on the same finger/wrist; band crossing an inter-finger gap = FAIL; bracelet must close | G15_HAND_ANATOMY | user 2026-07-30 |
| `PLAUSIBILITY_L2_PLACEMENT` | 80 | ring centre between MCP and PIP of one finger; webbing/over-knuckle/past-fingertip = FAIL | G15_HAND_ANATOMY | user 2026-07-30 |
| `PLAUSIBILITY_L3_ANATOMY` | 80 | MediaPipe: 5 digits, correct joints, detection confidence >0.8; fused/extra/missing digits or impossible thumb = FAIL | G15_HAND_ANATOMY | user 2026-07-30 |
| `PLAUSIBILITY_L4_L8_VISUAL` | 80 | support/gravity, occlusion, light consistency, scale, reflection sanity â€” mandatory visual checklist on EVERY render until automated | visual_checklist | user 2026-07-30 |
| `REFS_REAL_PHOTO` | 80 | every lifestyle reference is a real camera photograph (no AI/render), unambiguous one-finger placement, real skin detail | refs_preflight | user 2026-07-30 |
| `RING_SCALE_ON_HAND` | 80 | on every on-hand/lifestyle image the ring is at true real-life scale: the centre stone sits WITHIN the finger's width (stone width <= finger width), never wider/oversized/cocktail-huge; an elongated stone spans ALONG the finger but must not overhang the finger sides. Reject if the diamond looks oversized for the hand. | G22_STONE_WITHIN_FINGER | user 2026-07-31 |
| `SKIN_REALISM` | 80 | exposure-normalized skin high-frequency energy above threshold; plastic/over-smoothed skin = FAIL | G16_SKIN_REALISM | user 2026-07-30 |
| `SUBJECT_SCALE_MIN` | 80 | lifestyle jewellery bounding box >= 12% of frame area (>= 25% on the two macro lifestyle slots); below threshold the model cannot resolve real geometry and substitutes a generic piece -> FAIL, regenerate with tighter framing. | G20_MIN_SUBJECT_SCALE | user 2026-07-31 |
| `ANGLE_NUMERIC_MATRIX` | 50 | camera defined by numeric azimuth/elevation/crop per slot; filenames carry no geometry; within-group pairwise separation 20az/15el | G10_ANGLE, refs_preflight | user 2026-07-30 |
| `ANGLE_STUDIO_SLOTS` | 50 | ring studio 4 = top_down, true_side (edge-on stone), front_elevation, gallery_back (rear 3/4, filigree gallery + back of shank); gallery_back replaces macro_head | G10_ANGLE | user 2026-07-30 |
| `AUTONOMY_RUN` | 50 | permissions granted once; run every catalog end-to-end with no check-ins; internal output only; user reviews after completion | run_catalog | user (19+20) |
| `BACKGROUND_VELVET` | 50 | studio background is premium plain pure-white velvet only (low saturation, high luminance, fine fabric texture); reject coloured backgrounds, seamless paper, hard gradients, props | G18_BACKGROUND | docs 11 |
| `COUNTS_4_6` | 50 | exactly 4 studio (white velvet) + 6 lifestyle; one image per angle/pose | slot_manifest | user 2026-07-28 |
| `FORMAT_ASPECT` | 50 | 1:1 square, 2048x2048 minimum, native, no upscale | G1_FORMAT | user 2026-07-30 |
| `OUTPUT_STORE` | 50 | all render outputs live in the single store deliveries/<SKU>/ (gitignored); images never committed | run_catalog | user 2026-07-30 |
| `PIPELINE_SOP` | 50 | per-catalog order P0-P9: source gate -> spec -> prompts -> frozen batch -> validate -> retry -> download(deliveries/) -> manifest -> failure memory -> commit+push | run_catalog | user (22) |
| `REALISM_ANTI_AI` | 50 | genuine photography, varied non-generic models/wardrobe; banned beige/cream/oatmeal knit, neutral couch, seamless backdrop in a lifestyle frame | G16_SKIN_REALISM | user (24 P6) |
| `REFS_PER_SLOT` | 50 | medias[0] is a distinct per-slot reference from refs/<SKU>/; --stage prompts hard-fails if any missing | refs_preflight | user 2026-07-30 |
| `REGRESSION_NO_REGRESS` | 50 | quality only ratchets up; a gate that stops catching a past failure fails the build; goldens are permanent | regression_suite | user (14+15) |
| `THEME_PER_CATALOG` | 50 | one coherent theme within a catalog; a different theme per catalog rotated by SKU hash | G17_THEME | user (24 P5) |
| `TOKEN_BUDGET` | 50 | <=15k tokens per catalog; savings come only from what is displayed, never from source fidelity, prompt detail, or validation | run_catalog.budget_check | user (05+17) |

## Superseded rules (provenance — never deleted)

| ID | Statement | Superseded by |
|---|---|---|
| `ANGLE_STUDIO_MACRO_HEAD` | studio slot 04 = macro_head | `ANGLE_STUDIO_SLOTS` |
| `FORMAT_PORTRAIT` | all images portrait | `FORMAT_ASPECT` |
| `FROZEN_CALL` | Higgsfield generation call frozen: text-to-image, 2k/1:1/count1/one batch, medias [pose/studio ref, SOURCE piece]; no img2img/denoise/compositing of jewelry (accent-run composite exception approved) | `SOURCE_REF_CALL` |
| `G19_COMPOSITE_PROVENANCE` | every delivery carries its source cutout name + sha256 and asserts whole-asset affine only; no sidecar or hash mismatch = no ship. Pixel-counters G2-G9 retired for composites; geometry verified by cutout hash. | `HIGGSFIELD_ONLY` |
| `GEN_COMPOSITE_V2` | Jewellery is composited from source CAD cutouts (whole-asset affine transform only); Higgsfield generates BACKGROUND PLATES ONLY (call shape unchanged: 2k,1:1,count1,one batch); no jewellery word or geometry in any prompt. | `HIGGSFIELD_ONLY` |
| `GEN_ENGINE_LOCK` | Higgsfield MCP is the only production image-generation engine; never swap providers | `GEN_COMPOSITE_V2` |
| `GEOMETRY_FROM_SOURCE` | Higgsfield generates 100% of every scene (velvet, cloth, hands, skin, wardrobe, environment, light, shadow). The jewellery layer is PLACED from the source CAD cutout by affine transform only (scale/rotate/translate) — never redrawn, never generatively filled inside the jewellery bounds. Text-to-image cannot hold stone-size ratios (proven LR-0203/0206/0211, 3%-53% framing); this path makes geometry exact by construction. | `HIGGSFIELD_ONLY` |
| `METAL_DEFAULT_18K` | default 18K natural yellow gold unless source otherwise | `METAL_SOURCE_GOVERNED` |
| `SUBAGENT_BAN` | never spawn subagent/background-task/agent; read source in-thread once; no gallery-display widgets; job_display retrieval only, one pass per catalog | `PROCESS_NO_WIDGETS` |

## Advisory rules (empty enforced_by — not machine-verified)

- (none)
