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

## RUNTIME POLICY (user-locked 2026-07-11)
Aggressive token optimization with ZERO change to output quality or behavior.
- **Load only required files.** Never reload a file that is unchanged; reuse it from session memory. Reload ONLY files modified since last read.
- **Reuse cached studio assets** every shot: premium white cloth, preserved logo, lighting, camera, white balance (plus media_ids/presets/poses/verified sources). Never re-import/re-analyze unless the asset changed.
- **Do not summarize loaded files** back to the user; **do not explain reasoning**; think internally.
- **Return only the final result** (report count/IDs only — no narration, no re-printing prompts/URLs/schemas).
- This is an efficiency layer only: if any optimization could change the output in ANY way, do NOT apply it (output quality is #1).

## CONTEXT-LOADING / LAZY-LOADING POLICY (locked 2026-07-10)
Startup loads ONLY `CLAUDE_SETUP.md`. Never preload docs/prompts/cache/changelog/master-spec. Lazy-load exactly one relevant file per task (see the CLAUDE_SETUP §1 map); for normal generation load the runtime trio (`config/project_manifest.json` + `prompts/07_PROMPTS.md` + `config/QUALITY_MEMORY.json`). Load `docs/06_CACHE.md`/`QUALITY_MEMORY.json` only to prevent/learn failures, then unload. Load `docs/09_CHANGELOG.md` only for history/rollback/version-compare; `docs/01_MASTER_SPECIFICATION.md` only for architecture/global-standard changes. After extracting rules from a file, discard unused sections. Reduced context must never reduce output quality — load one more small file if needed, never the whole repo.
