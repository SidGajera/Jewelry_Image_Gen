# 17 — MASTER TOKEN OPTIMIZATION POLICY (HIGHEST PRIORITY)

> **AUTHORITATIVE OWNER (see `00` POLICY INDEX):** this doc owns silent execution, token optimization, no-image-preview, and the one-sentence default output contract. `05` is subordinate detail.

User-locked 2026-07-16. **This single policy overrides every previous token-saving, workflow, preview, commit, reasoning, memory, QC-narration, and generation-narration rule. If any prior rule conflicts, THIS policy wins.** It is the one precedence order — do not reason about which scattered rule applies; apply this. (The detailed entries in docs/05 and QUALITY_MEMORY remain as subordinate detail; this governs.)

Does NOT override the ABSOLUTE jewelry-preservation / geometry / logo / QC-fidelity rules (docs/02, 13, 16) — see FINAL PRINCIPLE.

## PRIMARY OBJECTIVE
Maximize output quality while minimizing tokens. Every generated token must directly improve the final result; if a token doesn't improve the output, don't generate it.

## ZERO WASTE / SILENT EXECUTION
Never spend tokens on: internal reasoning, chain-of-thought, self-reflection, planning, progress narration, image/source/geometry descriptions, repeated confirmations, policy reminders, previews, verbose logs, unnecessary summaries. Execute internally; never narrate what you are doing or checking; print only important user-facing results.

## DIFFERENTIAL EXECUTION
Never reload unchanged resources; reuse cached data; process only files that changed; never re-read source images unless modified; never repeat previous work.

## INTERNAL REASONING & USER OUTPUT (user-locked 2026-07-18)
Think internally; speak minimally; deliver results only. Never expose reasoning, planning, deliberation, uncertainty, conflict resolution, decision process, internal prompts, validation logic, policy/priority/memory loading, failure-memory contents, implementation details, workflow decisions, or model limitations. Banned phrasings include: "I'm thinking / I'm facing a conflict / the policy says / I should / I could / actually / looking at / the user is asking / the executable path is / I'm going to / I don't know".
- **Policy conflicts:** resolve internally and silently. Do not explain the conflict; do not ask the user to choose between internal workflows unless genuinely-missing essential information blocks the work.
- **During rendering:** no progress/reasoning/validation/job/prompt narration. Emit only one of: `Generating…` · `Completed.` · `Regenerating.` · `Approved.` · `Failed. Retrying.`
- **Cannot continue:** return one concise status ≤15 words (e.g. `Missing source CAD.` · `Missing reference image.` · `Higgsfield service unavailable.` · `Rejected. Regenerating.`).

## OUTPUT POLICY — PERMANENT (user-locked 2026-07-18)
Never expose internal reasoning, thought process, planning, or workflow narration. Never explain what files are read, commands run, policies loaded, validations performed, or implementation steps taken. Never emit "I'm checking… / I'm thinking… / I need to… / I'm reviewing…" or similar. Never output internal implementation notes or progress text. **Produce only final user-facing results:** on success, return only the final result; on failure, return only a concise error plus the next action. (Reinforces DEFAULT RESPONSE STYLE and INTERNAL REASONING & USER OUTPUT below.)

## DEFAULT RESPONSE STYLE — ONE SENTENCE (user-locked 2026-07-18)
Default maximum response = ONE short sentence (e.g. `Generating…` · `Completed.` · `Image approved.` · `Validation failed. Regenerating.` · `Done.`). Any explanation longer than one sentence is prohibited unless the user explicitly asks. Never output filler openers: "I'm going to / I'll now / I found / I'm checking / I've loaded / I'm reviewing / I think / the policy says / my approach / my reasoning". Never narrate what you are about to do. Never expose reasoning, planning, tool/policy/file/memory loading, prompt construction, generation strategy, or geometry/design analysis.
**No image preview (reinforced):** never display preview images, thumbnails, intermediate renders, rendering widgets or progress screenshots — see `05` NO IMAGE PREVIEW. Return only the final result reference.
**After a Git Pull:** do not re-explain the project, workflow, loaded policies, or previous work; do not re-display images; simply continue.

## NO PREVIEW
Never preview source / generated / reference / intermediate-composite / internal-QC images unless the user explicitly requests it (types `preview`, `show image`, or `compare images`) or at final approved catalog delivery. If an image must be inspected, do it in code and return text only (e.g. `✓ Downloaded · 1920×1920 · JPG · geometry check: passed`). Never generate throwaway previews/drafts/thumbnails/collages/low-quality tests either — only final full-quality output; regeneration REPLACES (never accumulates); produce exactly the requested count.

## SOURCE IMMUTABILITY
The source jewelry is absolute truth. Never redesign, reconstruct, enhance, simplify, infer, hallucinate, or regenerate any jewelry geometry. Only environments may change.

## INTERNAL VERIFICATION
All QC runs silently. Never print "I checked/analyzed/compared/verified…", never describe/report source geometry. Verify internally source-vs-generation on: head, gallery, prongs, cathedral, hidden halo, bridge, side diamonds, pavé, band thickness, metal thickness, diamond count, diamond positions, stone size, stone shape, silhouette, open/closed areas, proportions. Output only `Source verified.` then `Generating…`, or a failure (`QC Failed: - Geometry / - Logo`). Any jewelry difference → discard + regenerate.

## RESPONSE
Default 3–5 lines. Expand only when the user explicitly requests details.

## GENERATION
Per catalog: generate only Image 1, pause, wait for approval. Do not generate Images 2–N until Image 1 is approved.

## CORRECTION
While Image 1 is under review, modify only that image; never start another generation or queue future work.

## FAILURE
If generation changes jewelry geometry: auto-reject, retry internally, never deliver incorrect geometry.

## MEMORY
Never repeat known information, previous explanations, or unchanged rules.

## FILE / PORTABILITY
Repository stays portable; all paths configurable (Input, Output, Source, Reference, Temp, Config changeable from one configuration).

## COMMIT
Never commit, push, create branches, or modify Git history — unless the user explicitly approves.
**Standing approval (user-locked 2026-07-17): commit + push automatically EVERY TIME a catalog is completed/approved** — no need to ask again. Still: never commit or push *during* generation (`03` GIT RULE), never push failed/temporary/unapproved images, never create a branch without permission, never rewrite history. Push to the current authorized branch.

## TOKEN BUDGET
Tokens are limited. Choose the shortest correct response; avoid duplicate information, repeated instructions, and unnecessary acknowledgements.

## DECISION RULE (when multiple approaches exist, in order)
1. Fewest tokens · 2. Preserves output quality · 3. Preserves jewelry geometry · 4. Preserves previous successful behavior · 5. Allows one-command rollback if a new pipeline performs worse.

## ROLLBACK
Every major pipeline change is reversible; keep the previous stable pipeline intact; never remove a working pipeline until its replacement is fully validated; if the new pipeline underperforms, revert immediately without losing prior work or learnings.

## ZERO INTERNAL MONOLOGUE (ABSOLUTE — hard requirement)
Never expose internal reasoning. Never output "I think/realize/should/'m considering/'ll attempt/suspect", "the issue/problem is", "maybe/perhaps", plans, alternative approaches, troubleshooting, or technical-implementation talk (segmentation, flood fill, alpha matting, mask extraction, composite internals, geometry detector, rollback logic, caches, algorithms). Reason/debug/plan/optimize internally; expose only the final result. On a task: execute immediately — do not explain, narrate, justify, or describe intermediate steps. The ONLY visible messages are `Working…`, `Done.`, `Approval required:\n<one concise question>`, or `Stopped:\n<one actionable reason>` — nothing else. Discuss implementation only if the user explicitly says "Explain the implementation." Any visible internal monologue is a policy violation.

## VISIBLE-OUTPUT ENFORCEMENT (controls chat output only; never reduces quality/QC/processing)
No visible thinking, planning, analysis, progress narration, self-talk, alternative approaches, implementation reasoning, credit/tool deliberation, or file-by-file narration. All reasoning is silent. For execution requests, immediately do the work; interrupt only when a missing user decision makes execution impossible. Allowed user-visible messages ONLY:
- during work: `Working…`
- on completion: `Done.`
- on failure: `Stopped: <one-line actionable reason>.`
- when a decision is genuinely required: `Approval required: <single specific decision>.`
Max 1–3 lines during execution. No image preview unless the user types `preview`/`show image`/`compare images`. Never explain how token optimization is applied — apply it silently. Before sending any message, check: (1) does the user need this info? (2) is a decision required? (3) is there a failure needing action? If all three are no, send nothing. Quality, jewelry fidelity, silent source verification, QC accuracy, required processing, and rollback safety are unchanged — only unnecessary visible narration is removed.

## NEVER DISPLAY INTERNAL EXECUTION (user-locked 2026-07-17)
**Never show or stream:** uploaded media · image-upload confirmations · downloaded files · Google Drive activity · shell commands · terminal output · Python execution · MCP calls · Higgsfield upload status · Higgsfield command logs · API requests · API responses · JSON payloads · execution traces · progress logs · edited-file messages · commit messages · PR creation · resource loading · policy loading · cache loading · validation steps · workflow execution · internal reasoning · debug information · process state · tool names · command history.

**Never write lines like:** "Uploaded LR-0155 front CAD" · "Downloaded image…" · "Running command…" · "Edited a file…" · "Merged…" · "Using Higgsfield…" · "Using Google Drive…" · "Loading policy…" · "Reading QUALITY_MEMORY…" · "Executing…" · "Uploading media…" · "Confirm Upload…".

**SILENT EXECUTION.** Perform every internal action silently. Present ONLY: the final result · a concise status line when genuinely needed (e.g. `Rendering complete.`) · an explicit question only when user input is truly required.

**PRODUCTION PRINCIPLE.** Behave like a finished commercial application, not a development environment. Internal operations are completely hidden; only inputs and final outputs are visible.

## TOKEN OPTIMIZATION TARGETS + EXECUTION RULES (user-locked 2026-07-17)
**Targets:** <2,000 tokens per catalog · <300 tokens per image · load each policy ONCE per session unless it changes.

1. **LOAD ONLY REQUIRED POLICIES** — never the whole library. Studio images → jewelry preservation + logo + cloth + studio lighting. Lifestyle → jewelry preservation + lifestyle + human model + logo. Nothing unrelated. (Loader map: `03` POLICY EXECUTION ENGINE.)
2. **CACHE EVERYTHING** — load once, reuse for every image: source CAD · design profile · logo · cloth rules · Failure Memory · approved patterns. Never re-read unchanged files.
3. **DELTA VALIDATION** — never re-compare the entire policy set per image; validate only what the requested camera angle changes and reuse previous validation results.
4. **NO POLICY ECHO** — never repeat policy text inside prompts; reference the cached policy internally.
5. **SILENT EXECUTION** — hide uploads, downloads, tool calls, shell, command logs, JSON, validation logs (see NEVER DISPLAY INTERNAL EXECUTION).
6. **SINGLE COMPACT IMAGE PROMPT** — one prompt carrying only: camera angle · lighting · logo placement · cloth · geometry lock. Permanent rules are not restated.
7. **INCREMENTAL CATALOG** — generate image 1, reuse all context, generate image 2, reuse … never restart the workflow.
8. **FAILURE MEMORY** — check only the failures relevant to the current image; don't reload the whole history.
9. **NO REPEATED CAD ANALYSIS** — analyse the CAD once per SKU; store geometry · prongs · gallery · dimensions · proportions; reuse for the rest of the catalog (`06_CACHE`).
10. **FINAL VALIDATION ONLY** — one complete catalog validation after all images are generated; do not run a full validation after every image unless one fails.

*Precedence note: this section governs HOW MUCH is loaded, echoed and re-validated. It does not weaken the CAD geometry locks themselves (`13 §3.3`, `§3.4`, `§4.0`) — those stay in force via the cached policy, not via prompt repetition.*

### SILENT EXECUTION + TOKEN BUDGET (user-locked 2026-07-17)
**Minimise orchestration tokens. Internal execution stays silent unless the user explicitly asks for technical detail.**

**During generation:** read only the policies the task needs · use policies already cached this session · generate · validate internally · regenerate internally on failure · update Failure Memory silently · **never narrate internal execution**.

**NEVER DISPLAY:** loaded policies · document reads · policy-merge logs · validation steps · internal reasoning · execution pipeline · shell commands · terminal output · Python output · uploaded-media lists · process IDs · file paths · JSON · API responses · MCP activity · Google Drive activity · Higgsfield upload logs · internal decisions · Failure Memory updates · QUALITY_MEMORY updates · token statistics · timing statistics.

**USER-VISIBLE STATUS — only:** `Generating image…` · `✓ Image completed.` · `❌ Validation failed. Regenerating…`. No further explanation unless explicitly requested.

**SESSION CACHE (load once, reload only on change):** jewelry preservation · logo · cloth · camera · QUALITY_MEMORY · Failure Memory.

**INTERNAL VALIDATION:** reject internally · regenerate internally · update Failure Memory silently · never expose the validation process.

**TOKEN BUDGET:** session init 300–500 · per-image orchestration 50–150 · 12-image catalog orchestration 600–1,200. Spend tokens on image quality, not execution logs.

**ZERO-TOLERANCE:** never spend tokens explaining what the pipeline is doing unless asked. Priority order: **1. image quality · 2. geometry preservation · 3. silent execution · 4. token efficiency.**

## POLICY MERGE RULE (MANDATORY — one source of truth per category)
Before creating ANY new policy, search all existing policy documents. If an appropriate policy exists: do NOT create a new one — merge the new requirements into it, preserve its structure, and strengthen its validation. If multiple policies contain related rules: consolidate into the most appropriate owner, remove duplicate/overlapping statements, resolve conflicts by keeping the STRICTEST applicable rule, and leave exactly one authoritative version of each rule. Create a new document ONLY when no existing policy covers the subject and the topic cannot logically belong to any current document. Every update must maintain: one source of truth · no duplicated validations · no contradictory instructions · clear ownership.
**Owners:** jewelry geometry → `13` · image-generation workflow + validation gate → `03` · logo → `04` · background/studio consistency → `11` · camera angles → `12` · failure learning → `07` (+ `config/QUALITY_MEMORY.json`) · regression prevention → `14` · zero design invention → `16` · pipeline versioning → `15` · token/preview/commit/reasoning → `17` (this file).
**MASTER RULE: never increase the number of policy documents when an existing document can be improved. Always prefer merging over creating.**

## POLICY MAINTENANCE (silent — this policy governs its own upkeep)
Policy/refactor work must itself obey this policy. Read, merge, replace, delete redundant policies, update references, and validate SILENTLY — never narrate what is being searched/opened/merged/removed, never expose plans, execution order, file traversal, mapping/merge strategy, or reasoning. Report only when a user decision is required or the work is finished: `Updating…` / `Done.` / `Waiting for approval.` (1–2 short lines). Consume the absolute minimum tokens.

## OPERATIONAL NOTES (concrete levers under this policy — merged from the former docs/05)
- **Banned high-token tools:** never call `show_generations`, `job_display`, or `models_explore list` (each ~4k–15k tokens). Don't view your own outputs — the user reviews in Higgsfield.
- **Base64 never enters context/cache:** download → temp file → Read locally → drop base64 → use the temp file only.
- **Design profile once per SKU:** analyze the source ONCE, cache a lightweight profile in `docs/06_CACHE.md`, reuse it; re-analyze only if the reference changes.
- **Import/cache once:** import each reference once (reuse its media_id until it expires); reuse cloth, logo, camera, lighting, white-balance, runtime prompt, generation params.
- **Prompts:** one canonical base prompt + the minimum task delta (angle tag + SKU design string); never repeat rules already in the base prompt. Fix cloth/logo LOCALLY (0 credits) instead of regenerating.
- **Context/lazy-load:** startup loads ONLY `CLAUDE_SETUP.md`; normal generation loads the runtime trio (`config/project_manifest.json` + `prompts/07_PROMPTS.md` + `config/QUALITY_MEMORY.json`); load one more small file per task only as needed; never preload the whole repo. Reduced context must never reduce quality.
- **True zero-token option:** hand the user the ready-to-paste prompt pack + settings and let them run generations in the Higgsfield app directly (chat has a ~450-token/image floor).
- **Measured cost reference:** `generate_image` echo ~450/img · media import ~1,200 · source view ~1,300 · `show_generations`/`job_display` ~10k–15k (banned).

## NSFW / PROVIDER-MODERATION HANDLING (user-locked 2026-07-18; owner of this responsibility per `CLAUDE_SETUP §1.1`)
A `status:"nsfw"` / moderation block from Higgsfield is a **temporary provider-side event, NOT a design failure.** Do NOT: stop the catalog · mark the design failed · record it as a jewelry failure · add it to Failure Memory · burn repeated immediate-retry credits · ask the user for approval.
Do, automatically: (1) keep all approved images and continue the remaining catalog; (2) wait and retry later, OR regenerate with an EQUIVALENT camera framing that preserves the exact jewelry geometry (geometry owner `13`); (3) resume the blocked image automatically once the provider accepts it.
User-facing text is ONLY: "One image was temporarily blocked by the provider's moderation system. Remaining images continue processing. The blocked image will retry automatically." No stack traces, widget logs, diagnostics or internal reasoning.

## FINAL PRINCIPLE
**Quality first. Geometry second to none. Token efficiency everywhere else.**
