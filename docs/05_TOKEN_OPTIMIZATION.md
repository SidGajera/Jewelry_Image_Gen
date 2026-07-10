# 05 — TOKEN OPTIMIZATION (highest-priority efficiency layer)

Objective: minimize input + output tokens while producing IDENTICAL image quality and composition. Optimization must NEVER reduce quality or change design/lighting/realism/materials/angle/composition.

## THE 10 RULES (user-locked 2026-07-10)
1. **Reuse all cached assets** — imported media_ids, preset_ids, pose_ids, source_ids. Never re-import/re-analyze unless the asset changed.
2. **Never repeat catalogs/images** — if a catalog/source/output was already processed, skip it. Detect dupes by file ID / media ID / hash / catalog ID.
3. **Never repeat prompts** — store reusable instructions as presets; send only the minimum params per generation.
4. **Never repeat URLs, schemas, metadata, or prior responses** — return only essential IDs + results.
5. **Never search/scan storage** if the asset already exists in cache.
6. **Batch operations** to avoid repeated tool calls (fire all 12 generations in one block).
7. **Cache intelligently** — cache only reusable resources (imports, presets, poses, verified sources); do NOT re-cache existing generated images; reuse cached refs.
8. **Output quality is #1** — result must be visually identical to the un-optimized output.
9. **If an optimization could change output in ANY way, do NOT apply it.**
10. **Before generating, check if an identical generation already exists** — if so reuse its generation ID; only generate when the requested output differs.

## WHERE TOKENS GO (per 12-image catalog, measured)
| Task | ~Tokens | Note |
|---|---|---|
| `generate_image` echoes (prompt + 2 media URLs per call) | ~5,400 | 12 × ~450. #1 cost, scales with prompt length. |
| `media_import_url` (source + pose refs) | ~1,200 | one-time per catalog; reuse studio refs. |
| Drive search + source study (view 1–2 images) | ~1,000–2,000 | required for fidelity. |
| Viewing a generated image | ~1,300 each | only when explicitly pulled up. |
| Tool schema loads (`ToolSearch`) | ~500–4,000 | `models_explore list` alone dumps ~4k — avoid. |
| `show_generations` / `job_display` | ~10,000–15,000 | **BANNED** — never call. |

## LEVERS (apply all; none reduce quality)
- Reuse cached media_ids (no re-import).
- Fire all 12 correct the first time (retries re-echo the whole prompt — the #1 avoidable cost).
- No `models_explore`, no `show_generations`, no `job_display`, no base64 in context.
- Don't view outputs yourself — the user reviews in Higgsfield.
- Keep prompts compact but full-quality (canonical base prompt + short angle/scene tag).
- Fix cloth color and logo LOCALLY (0 credits) instead of regenerating.

## SILENT EXECUTION
- Report count only ("LR-XXXX done: 5 studio + 4 lifestyle + 3 closeup"). No preview widgets, no narration of each image, no re-printing of prompts/URLs.
- Take permission once per batch, then run the whole batch.

## TRUE ZERO-TOKEN GENERATION (optional)
Generation through chat has an unavoidable floor (~450 tokens/image echoed by the tool). The only 0-token path is to hand the user the ready-to-paste prompt pack + settings (model `nano_banana_2`, 2K, 1:1, which source + pose per shot) and have them run the 12 generations in the Higgsfield app directly.
