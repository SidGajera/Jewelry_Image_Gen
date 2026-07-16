# 21 — HIGGSFIELD MCP ENGINE LOCK (PERMANENT PRODUCTION LOCK, user-locked 2026-07-16)

**Scope.** This file owns ONE thing: **which engine generates production images, and what may never be swapped for it.** It does not own pipeline *version* selection — that is `docs/15` + `config/pipeline_versions.json` (§6 below reconciles the two).

## 1. THE LOCK
**Higgsfield MCP is the ONLY approved production image generation engine.** Every production image MUST be generated through Higgsfield MCP. Never replace, bypass, redesign, or migrate the Higgsfield MCP workflow.

**Never automatically switch to:** Nano Banana · Nano Banana 2 · GPT Image · Flux · Stable Diffusion · Midjourney · any alternate image generation provider · any experimental image generation pipeline.

Always execute generation through the existing Higgsfield MCP integration that produced the previously approved catalogs. **That workflow is the production baseline.**

## 2. WHAT "GENERATION" MEANS HERE (binding, resolves an apparent conflict)
"Generate" = **synthesise new image content**. Only Higgsfield may do that.

**Compositing preserved pixels is NOT generation.** Placing the source-CAD ring (`scripts/composite_ring_into_scene.py`) and the locked logo (`scripts/print_logo_on_cloth.py`) into a Higgsfield-rendered scene invents nothing — every one of those pixels comes from a locked asset. These steps are REQUIRED by `docs/04` (P0: AI never renders the logo) and by `composite-v1`, the production pipeline (`docs/15` §0).

Therefore the ban on "PIL/OpenCV rendering" targets **synthesis** engines, never the composite/QC/cut steps. Python may: manage files, cut/key source assets, composite preserved assets, validate, QC, crop, resize, rename, log, automate. Python may **never synthesise image content**.

## 3. MODEL vs PROVIDER (binding)
`nano_banana_2` is **Higgsfield's own model** and is the locked production model (`config/project_manifest.json` → `generation_settings.model`, `CLAUDE_SETUP.md` §4). The §1 ban list means **alternate providers**; it does NOT ban Higgsfield's own model. Selecting `nano_banana_2` inside Higgsfield is compliance, not a switch.

> **KNOWN DEFECT (open, 2026-07-16):** every `generate_image` request specifying `nano_banana_2` has been executed by the server as `nano_banana_flash`. The model ID is valid in the catalog, so this is server-side routing, not a bad request. Production is therefore NOT currently on the locked model. Do not "fix" this by switching providers.

## 4. SOURCE LOADING — NEVER ASK THE USER
Always use the existing local source images already stored in the project (`workspace/golden/**`, `assets/**`) and the durable Drive IDs in `docs/06_CACHE.md`.

**Never ask for:** upload widget · browser upload · media_ids · manual upload · source re-upload · source re-registration — when the required sources already exist in the repository.

`media_id` is Higgsfield MCP's internal input format (`media_import_url` → `medias[].value`); the API rejects raw URLs. Using it silently is the integration working as designed. The rule above bans **asking the user to upload**, not the API's own plumbing.

## 5. ERROR RECOVERY
On a Higgsfield MCP authentication or infrastructure error:
1. Retry automatically once.
2. Reconnect automatically if the MCP supports it.
3. Retry once after reconnection.
4. If recovery fails, report ONLY the verified API error (`docs/20`).

**Never** silently replace Higgsfield MCP with another provider because of an authentication, infrastructure, or session issue. Mid-turn "Stream closed" / "Denied by user" from MCP are transport disconnects — auto-reconnect and retry; they are not permission prompts.

## 6. ALLOWED vs FORBIDDEN CHANGES
**Allowed (around Higgsfield, never instead of it):** token optimization · caching · geometry verification · QC · error recovery · automatic retry · logging · repository portability · performance optimization.

**These must NEVER modify:** Higgsfield MCP integration · the Higgsfield generation process · prompt execution flow · source image loading workflow · production output characteristics · visual style · image quality · previously approved behavior.

**Never introduce:** pipeline selection dialogs · provider selection dialogs.

**Relationship to `docs/15`:** this file fixes the ENGINE (always Higgsfield MCP). `docs/15` fixes the PIPELINE VERSION (`composite-v1` = production; `legacy` = deprecated, never automatic). Both are true simultaneously: composite-v1 *uses* Higgsfield MCP for the scene. A request for "Higgsfield" is a request for composite-v1 (`docs/15` §0) — never for legacy.

## 7. REGRESSION
If any change produces worse image quality or different generation behavior: immediately revert to the last stable Higgsfield MCP workflow (`docs/15` §3, `scripts/rollback-pipeline.*`), preserve all validated learnings and corrections (`config/QUALITY_MEMORY.json`), and never lose previously approved capabilities. Backward compatibility is mandatory — every existing catalog must keep working exactly as before.

## FINAL PRINCIPLE
Use Higgsfield MCP for 100% of production image generation. Improve everything around it, but never replace or redesign the Higgsfield MCP generation workflow without explicit user approval.
