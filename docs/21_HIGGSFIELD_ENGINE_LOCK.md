# 21 — HIGGSFIELD MCP ENGINE LOCK (PERMANENT PRODUCTION LOCK, user-locked 2026-07-16)

**Scope.** This file owns ONE thing: **which engine generates production images, and what may never be swapped for it.** It does not own pipeline *version* selection — that is `docs/15` + `config/pipeline_versions.json` (§6 below reconciles the two).

## 1. THE LOCK
**Higgsfield MCP is the ONLY approved production image generation engine.** Every production image MUST be generated through Higgsfield MCP. Never replace, bypass, redesign, or migrate the Higgsfield MCP workflow.

**Never automatically switch to:** Nano Banana · Nano Banana 2 · GPT Image · Flux · Stable Diffusion · Midjourney · any alternate image generation provider · any experimental image generation pipeline.

Always execute generation through the existing Higgsfield MCP integration that produced the previously approved catalogs. **That workflow is the production baseline.**

## 1a. AUTHORIZATION PHRASE + FULL NEVER-AUTO LIST (user-locked 2026-07-16)

**The image generation pipeline may change ONLY on the explicit instruction:**

> **"Change the image generation pipeline."**

**No other instruction authorizes it.** Not a bug report, not a quality complaint, not a geometry failure, not a timeout, not an internal recommendation, not an optimization goal. If an instruction seems to imply a pipeline change without that sentence, it does not authorize one - stop and ask.

**Never automatically switch to:** another connector · another provider · another image generation workflow · **Composite-v1** · Hybrid Composite · Local Composite · Manual Composite · Upload Widget · Media Upload Workflow · Browser Upload Workflow · Alternative MCP · Experimental Pipeline · any future image generation pipeline.

**Model names are NOT in that list** (user-locked 2026-07-16). Do not hard-code model names and do not permanently ban internal model names - they are Higgsfield MCP internals, not providers. See §3.

**"Local/Manual Composite" in that list means a composite GENERATION pipeline** (composite-v1: the ring composited instead of generated). It does **NOT** mean the logo composite, which is a mandatory production stage in every pipeline (`docs/04` §8, P0) and is not generation (§2 below).

**On ANY Higgsfield failure - generation, timeout, API, connector, quality, geometry - the pipeline does NOT change.** Retry within the Higgsfield workflow, recover the session, repair execution, resume from the failed step, preserve the pipeline. Pipeline replacement is prohibited as a remedy for anything. A geometry-drift rejection is a QC outcome (`docs/18`), never a reason to switch.

**This policy overrides** automatic recovery logic, optimization logic, provider selection logic, fallback logic, experimental features, and future migrations.

## 2. WHAT "GENERATION" MEANS HERE (binding, resolves an apparent conflict)
"Generate" = **synthesise new image content**. Only Higgsfield may do that.

**Compositing preserved pixels is NOT generation.** Placing the source-CAD ring (`scripts/composite_ring_into_scene.py`) and the locked logo (`scripts/print_logo_on_cloth.py`) into a Higgsfield-rendered scene invents nothing — every one of those pixels comes from a locked asset. The LOGO composite is REQUIRED by `docs/04` (P0: AI never renders the logo) in EVERY pipeline, including the restored `legacy` production baseline. The RING composite belongs to `composite-v1`, which is retained for experimentation and is NOT production (`docs/15` §0).

Therefore the ban on "PIL/OpenCV rendering" targets **synthesis** engines, never the composite/QC/cut steps. Python may: manage files, cut/key source assets, composite preserved assets, validate, QC, crop, resize, rename, log, automate. Python may **never synthesise image content**.

## 3. MODEL POLICY — BACKWARD COMPATIBILITY DECIDES (user-locked 2026-07-16)

**Do NOT hard-code model names. Do NOT permanently ban internal model names.** Models are Higgsfield MCP internals; naming one is not a provider switch, and banning one is not provider hygiene.

**The rule:** select the model inside Higgsfield MCP that **preserves backward compatibility with the previously approved catalogs**. Today that is **the production model** (`config/project_manifest.json` -> `generation_settings.model`, `CLAUDE_SETUP.md` §4) - the model that produced them.

**If Higgsfield internally updates model names or routing, continue with the equivalent production model** that preserves the same workflow and output characteristics. Internal renames/reroutes are not migrations and require no authorization.

> **Observed routing (2026-07-16):** requests specifying the production model are executed by the server as `an internal routing alias`. This is Higgsfield-internal routing, outside our control. Per the rule above this is **not** a provider switch, **not** a defect to "fix" by changing providers or pipelines, and **not** grounds to stop. Continue; the workflow is unchanged.

**Backward compatibility with previously approved catalogs outranks experimental pipeline changes.** A different model - even a Higgsfield-native one such as `marketing_studio_image` - would restart geometry tuning from zero and break that compatibility. It requires explicit authorization.

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

**Relationship to `docs/15`:** this file fixes the ENGINE (always Higgsfield MCP). `docs/15` fixes the PIPELINE VERSION (`legacy` = production baseline, user-restored 2026-07-16; `composite-v1` = retained for experimentation, not production). Both are true simultaneously: legacy uses Higgsfield MCP for the scene and the jewelry; the preserved logo is still composited locally per `docs/04` P0. The production pipeline is `legacy`, the original Higgsfield lifecycle (`docs/15` §0, user-restored 2026-07-16); `composite-v1` is retained for experimentation only.

## 7. REGRESSION
If any change produces worse image quality or different generation behavior: immediately revert to the last stable Higgsfield MCP workflow (`docs/15` §3, `scripts/rollback-pipeline.*`), preserve all validated learnings and corrections (`config/QUALITY_MEMORY.json`), and never lose previously approved capabilities. Backward compatibility is mandatory — every existing catalog must keep working exactly as before.

## FINAL PRINCIPLE
Use Higgsfield MCP for 100% of production image generation. Improve everything around it, but never replace or redesign the Higgsfield MCP generation workflow without explicit user approval.
