# 21 — ENGINE LOCK (single delivering engine; switched by the user, never automatically)

> **AMENDED 2026-08-22.** This file was "HIGGSFIELD MCP ENGINE LOCK" and named Higgsfield as the permanent, only production engine. On explicit, repeated user instruction — *"Use google nano banana 2 pipeline do not use higgsfield now"* — the delivering engine is now a **switch position**, not a fixed identity. **`gflow-nb2` (Google Flow · Nano Banana 2) is live; Higgsfield is off for delivery.** What the lock protects is unchanged and is stated in §1.

**Scope.** This file owns ONE thing: **the rule that exactly one engine delivers and nothing may swap it automatically.** *Which* engine that is comes from the switch (`config/delivery_profiles.json`, thrown by `scripts/pipeline.py`). Pipeline *version* selection is `docs/15` + `config/pipeline_versions.json` (§6 reconciles the two); engine 2's limits are `docs/26`.

## 1. THE LOCK
**Exactly ONE engine delivers at a time, and every other engine is blocked from every delivered pixel.** The delivering engine is whichever the live delivery profile names. Never replace, bypass, redesign, or migrate the live engine's workflow on your own initiative.

**Never automatically switch** — to Nano Banana · Nano Banana 2 · GPT Image · Flux · Stable Diffusion · Midjourney · any alternate provider · any experimental pipeline · *or between the two declared profiles*. The switch is manual in both directions.

`scripts/engine.py --check` asserts the one-engine invariant against the live profile, and `scripts/pipeline.py --check` asserts every derived file agrees with it. Both pass in both switch positions.

## 1a. HOW THE PIPELINE CHANGES (amended 2026-08-22)

**Only a direct user instruction changes it, and it is applied by one command:**

```bash
python scripts/pipeline.py --on      # Google Flow · Nano Banana 2  (live)
python scripts/pipeline.py --off     # Higgsfield
```

The 2026-07-16 authorization phrase *"Change the image generation pipeline."* is retired as a required incantation — the user's plain instruction is what authorizes a switch, and the command is what applies it.

**What still binds:** no bug report, quality complaint, geometry failure, timeout, internal recommendation, or optimization goal authorizes a switch. If an instruction seems to imply a pipeline change without saying so, it does not authorize one — stop and ask. **Never fall back to the other engine on a failure**; retry inside the live engine.

> **Authorized changes on record.** (1) 2026-07-20: production VERSION switched `legacy` → `composite-v1` after the user was shown the trade-offs and confirmed. (2) 2026-07-21: the user reversed it — "use only Higgsfield", "do not ask again" — so production VERSION is now `legacy` (Higgsfield generates every frame). Both changed only the pipeline VERSION (`docs/15`), never the engine — Higgsfield still renders every scene (§2). This clause continues to bind: do not switch production again, and do not re-raise the pipeline choice, without a fresh explicit user instruction. See `config/QUALITY_MEMORY.json#composite-v1-production-lock`.

**Never automatically switch to:** another connector · another provider · another image generation workflow · **Composite-v1** · Hybrid Composite · Local Composite · Manual Composite · Upload Widget · Media Upload Workflow · Browser Upload Workflow · Alternative MCP · Experimental Pipeline · any future image generation pipeline.

**Model names are NOT in that list** (user-locked 2026-07-16). Do not hard-code model names and do not permanently ban internal model names - they are Higgsfield MCP internals, not providers. See §3.

**"Local/Manual Composite" in that list means a composite GENERATION pipeline** (composite-v1: the ring composited instead of generated). It does **NOT** mean the logo composite, which is a mandatory production stage in every pipeline (`docs/04` §8, P0) and is not generation (§2 below).

**On ANY Higgsfield failure - generation, timeout, API, connector, quality, geometry - the pipeline does NOT change.** Retry within the Higgsfield workflow, recover the session, repair execution, resume from the failed step, preserve the pipeline. Pipeline replacement is prohibited as a remedy for anything. A geometry-drift rejection is a QC outcome (`docs/18`), never a reason to switch.

**This policy overrides** automatic recovery logic, optimization logic, provider selection logic, fallback logic, experimental features, and future migrations.

## 2. WHAT "GENERATION" MEANS HERE (binding, resolves an apparent conflict)
"Generate" = **synthesise new image content**. Only Higgsfield may do that.

**Compositing preserved pixels is NOT generation.** Placing the source-CAD ring (`scripts/composite_ring_into_scene.py`) and the locked logo (`scripts/print_logo_on_cloth.py`) into a Higgsfield-rendered scene invents nothing — every one of those pixels comes from a locked asset. The LOGO composite is REQUIRED by `docs/04` (P0: AI never renders the logo) in EVERY pipeline, including the restored `legacy` production baseline. The RING composite belongs to `composite-v1`, which is retained for experimentation and is NOT production (`docs/15` §0).

Therefore the ban on "PIL/OpenCV rendering" targets **synthesis** engines, never the composite/QC/cut steps. Python may: manage files, cut/key source assets, composite preserved assets, validate, QC, crop, resize, rename, log, automate. Python may **never synthesise image content**.

**APPROVED ACCENT-RUN COMPOSITE EXCEPTION (user-locked 2026-07-30).** The Higgsfield generation call is FROZEN (docs/22): plain text-to-image, medias [pose/studio ref, SOURCE piece], 2k/1:1/count 1/one batch — no img2img, no denoise. Because diffusion cannot count discrete accent stones or hold an exact count, **accent/pavé runs MAY be composited post-render, in local Python, from the clean source CAD view** — the same preserved-pixel layer mechanism proven on the logo (§2, `docs/04`). This is a deliberate carve-out to the "do not composite the jewelry" clause, scoped to **accent runs only**: the jewelry BODY (primary stone, head/setting, structure/band) and the SCENE remain **generated**, never composited; only the accent-stone run is transferred so its count is correct by construction. The generation call itself is unchanged. Prerequisite: a clean CAD source view (the 4 required views must pass `validate_source`). `scripts/composite_accent_run.py`.

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

**Relationship to `docs/15`:** this file fixes the ENGINE (always Higgsfield MCP). `docs/15` fixes the PIPELINE VERSION. As of **2026-07-21 (explicit, repeated user instruction: "use only Higgsfield", "do not ask again")** the production version is **`legacy`** — Higgsfield generates every frame, including the ring, from the approved geometry-locked prompts; the preserved logo is still composited locally per `docs/04` P0. This reversed the 2026-07-20 `composite-v1` switch, because the user needs worn lifestyle/close-up frames that composite cannot produce. Engine is unchanged throughout — Higgsfield renders every scene (and, under `legacy`, the ring). See `docs/15` §0, `config/QUALITY_MEMORY.json#composite-v1-production-lock` (updated 2026-07-21).

## 7. REGRESSION
If any change produces worse image quality or different generation behavior: immediately revert to the last stable Higgsfield MCP workflow (`docs/15` §3, `scripts/rollback-pipeline.*`), preserve all validated learnings and corrections (`config/QUALITY_MEMORY.json`), and never lose previously approved capabilities. Backward compatibility is mandatory — every existing catalog must keep working exactly as before.

## FINAL PRINCIPLE
Use Higgsfield MCP for 100% of production image generation. Improve everything around it, but never replace or redesign the Higgsfield MCP generation workflow without explicit user approval.

## 8. SUCCESS VALIDATION — THE GALLERY IS THE ONLY PROOF (user-locked 2026-07-16)

A generation is successful **only** when the image is visible in the official Higgsfield website/gallery.

**None of these is success.** API accepted · job submitted · job queued · job running · background task completed · request ID returned · local preview · temporary cache · MCP success message · internal completion message.

**Success requires all three:**
1. The image is visible in the Higgsfield website/gallery.
2. The image can be opened/downloaded from Higgsfield.
3. The image passes production QC (`docs/18`).

If the image is not visible on the Higgsfield website, **treat the generation as FAILED** and recover inside the Higgsfield workflow (§1a) — never by switching provider, model or pipeline.

**Never report success before verifying the image exists on Higgsfield.** A `status: "pending"` response, or a job id with no retrievable asset, is not a delivered image. Verify by confirming the job appears in the gallery listing with a retrievable `rawUrl`, and by fetching that asset successfully. Only then may `SUCCESS` be reported (`docs/20`).
