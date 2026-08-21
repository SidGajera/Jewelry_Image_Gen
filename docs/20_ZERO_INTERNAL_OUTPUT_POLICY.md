# 20 — LUCENT CARAT LAB · ZERO INTERNAL OUTPUT POLICY / PRODUCTION MODE (user-locked 2026-07-16)

**Production mode is customer mode.** Highest output priority — **overrides every documentation, debug, development, verbose, diagnostic, reasoning and QC output mode.** Applies to every image generation, QC step, recovery, composite, and pipeline execution.

Supersedes the response-length and preview clauses of `docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md` for pipeline work. `docs/17` remains the single authority on token *budget* and loading. On any conflict about what may be *displayed*, this file wins.

## 1. NEVER DISPLAY (user-locked 2026-07-16)

Never output: bash commands · python code · curl commands · URLs · file paths · API requests · HTTP status · JSON · internal variables · reconstruction methods · timestamp logic · download logic · cache logic · retry logic · tool names · MCP internals · background task details · execution traces · preview operations · technical debugging · internal reasoning · image previews · "Generating..." narration beyond the single allowed line · intermediate images · job ids · request ids · model names · provider names · credits · pipeline names · prompt text · QC reports · self-evaluation · recovery strategy · implementation notes · installation suggestions · next-action suggestions · source-code references.

**Never explain HOW you are executing. Never narrate the execution process. Never expose implementation details while a task is running.** Execution stays completely silent from start to completion.

**Preview/display tools are barred outright** (`show_generations`, `job_display`) - reinforcing `CLAUDE_SETUP.md` §2.6. The user will never allow a generation result to be displayed.

If additional information is genuinely required, report it in **one sentence only**.

## 2. THE ONLY ALLOWED OUTPUTS (user-locked 2026-07-16)

```
Generating...
```
then
```
Done.
```
or
```
Stopped: <verified concise error>
```
Nothing else. No previews, no technical detail, no job ids, no model names, no narration.

**`Done.` may only be reported after ALL of:**
1. Higgsfield render completed (`docs/21` §8 - visible and retrievable, not merely submitted).
2. Official preserved logo printed naturally on the cloth (`docs/04` §7, §8).
3. Jewelry unchanged (`docs/18` reject-on-drift).
4. Final QC passed.
5. Final image saved.

A Higgsfield render finishing is **not** job completion. The job completes only when the delivered file carries exactly one official preserved logo printed on the cloth.

## 3. NO PREVIEW
Never call preview/display tools (`show_generations`, `job_display`) as part of normal generation. Reinforces `CLAUDE_SETUP.md` §2.6.

## 4. ERROR HANDLING
On a verified error: retry automatically per the recovery policy (`docs/15`), then report **only the final verified error** after retries are exhausted. One line. No reasoning, no fix suggestions, no strategy.

## 5. WHAT SILENCE DOES **NOT** MEAN
Silence covers **process**, never **truth about outcomes**.
- Never report `SUCCESS` for an image that failed a gate. `docs/18` (zero-tolerance QC) and `docs/04` (preserved logo) reject and regenerate **internally and silently**, before the user sees anything. A rejected image is never delivered and never announced.
- Never fabricate success. Never ship a known-failed image to satisfy the output format.
- A blocker that requires user action is a **verified error** → report once as `STOPPED`, then stop repeating it on subsequent turns.
- If the user **explicitly asks** for detail ("why", "give me fixes", "explain"), answer fully — the ask suspends this policy for that turn only, then it resumes.

## 6. TOKEN RATIONALE
Spend tokens on image quality, not explanations. Narration and diagnostics are pure cost in a customer-facing pipeline.
