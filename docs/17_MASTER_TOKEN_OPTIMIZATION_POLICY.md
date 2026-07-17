# 17 — MASTER TOKEN OPTIMIZATION POLICY (HIGHEST PRIORITY)

User-locked 2026-07-16. **This single policy overrides every previous token-saving, workflow, preview, commit, reasoning, memory, QC-narration, and generation-narration rule. If any prior rule conflicts, THIS policy wins.** It is the one precedence order — do not reason about which scattered rule applies; apply this. (The detailed entries in docs/05 and QUALITY_MEMORY remain as subordinate detail; this governs.)

Does NOT override the ABSOLUTE jewelry-preservation / geometry / logo / QC-fidelity rules (docs/02, 13, 16) — see FINAL PRINCIPLE.

## PRIMARY OBJECTIVE
Maximize output quality while minimizing tokens. Every generated token must directly improve the final result; if a token doesn't improve the output, don't generate it.

## ZERO WASTE / SILENT EXECUTION
Never spend tokens on: internal reasoning, chain-of-thought, self-reflection, planning, progress narration, image/source/geometry descriptions, repeated confirmations, policy reminders, previews, verbose logs, unnecessary summaries. Execute internally; never narrate what you are doing or checking; print only important user-facing results.

## DIFFERENTIAL EXECUTION
Never reload unchanged resources; reuse cached data; process only files that changed; never re-read source images unless modified; never repeat previous work.

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

## FINAL PRINCIPLE
**Quality first. Geometry second to none. Token efficiency everywhere else.**
