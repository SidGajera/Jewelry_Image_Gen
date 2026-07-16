# 20 — LUCENT CARAT LAB · ZERO INTERNAL OUTPUT POLICY / PRODUCTION MODE (user-locked 2026-07-16)

**Production mode is customer mode.** Highest output priority — **overrides every documentation, debug, development, verbose, diagnostic, reasoning and QC output mode.** Applies to every image generation, QC step, recovery, composite, and pipeline execution.

Supersedes the response-length and preview clauses of `docs/17_MASTER_TOKEN_OPTIMIZATION_POLICY.md` for pipeline work. `docs/17` remains the single authority on token *budget* and loading. On any conflict about what may be *displayed*, this file wins.

## 1. NEVER DISPLAY
image previews · "Generating..." · live rendering window · intermediate images · job IDs · request IDs · API request IDs · model names · provider names · pipeline names · composite pipeline internals · Nano Banana · Higgsfield internals · Python scripts · local file paths · credits used · prompt text · debug logs · QC logs · QC reports · self-evaluation · internal reasoning · internal decisions · technical analysis · stack traces · progress narration · recovery strategy · implementation notes · installation suggestions · next-action suggestions · alternative solutions · source-code references

Do not explain what happened internally. Do not describe which model was selected. Do not explain pipeline decisions. Do not expose implementation details.

## 2. THE ONLY ALLOWED OUTPUTS
```
SUCCESS
Image generated.
```
or
```
STOPPED
<verified final error>
```
Nothing else.

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
