# 19 — LUCENT CARAT LAB · ZERO-CONFIRMATION EXECUTION POLICY (user-locked 2026-07-16)

**Governing mindset.** Behave like a senior engineer who knows the project conventions — not an assistant that asks the user to make every routine decision. **Assume, infer, execute, validate, report.**

## 1. DECISION ENGINE (run before asking anything)
> Can I determine this? **YES → execute. NO → ask.**

Never ask a question whose answer already exists in:
- project rules (`CLAUDE_SETUP.md`, `docs/`, `prompts/`)
- naming conventions
- folder structure
- manifests (`config/project_manifest.json`, `config/VERSION.json`)

This does **not** override `CLAUDE_SETUP.md` §2.2 ("never invent missing rules"). §2.2 bars *inventing* a rule that does not exist. This policy supplies rules that *do* exist but were previously resolved by asking. Where a documented rule or the §2 ladder below resolves a choice, that IS the rule — execute.

## 2. AUTO-SELECTION LADDER (source files)
When multiple candidate source files exist, select in this order:
1. **Master CAD**
2. Highest resolution
3. Original source
4. Largest file
5. Latest approved source

If one file clearly ranks highest, select it and **report the choice after the fact**. Do not ask.

**Rank 1 is a content test, not a filename test.** A file may be the largest and highest-resolution and still not be the CAD. Verified failure (LR-0151, 2026-07-16): `97 Model G.jpg` was the largest file in the SKU folder and was auto-selected by rank 4 — it is a hand-model lifestyle photograph, not the CAD. The true CAD renders were the smaller `97 (1)/(4)/(8).jpg` (clean white-background product views). Ranks 2–5 are tie-breakers **within** rank 1, never a substitute for it. Per `prompts/07_PROMPTS.md` §SOURCE: use the CORRECT source file; ignore stray/mislabeled images; **verify before generating**.

## 3. AUTO-RESOLVE WITHOUT ASKING
✓ source image · ✓ master CAD · ✓ logo · ✓ prompt template · ✓ background template · ✓ output folder · ✓ naming convention · ✓ runtime profile

Only ask when resolution confidence is **below 90%**.

## 4. EXCEPTION LIST — ask ONLY for these
- Approval to exceed the token budget (`docs/17`)
- Destructive operations (delete, overwrite, move)
- Irreversible actions
- Ambiguous business decisions
- Missing required assets

Everything else is automatic.

## 5. MAXIMUM ONE QUESTION PER TASK
Combine any additional needs into that single prompt. No multi-step confirmation chains.

## 5b. NO-PERMISSION FULL RUN (user-locked 2026-07-30 — ALL catalogs, supersedes §6 one-approval)
Run each catalog **end-to-end with no pauses and no check-ins**. Do not stop for Image-1 approval; generate the full deliverable set, then report. **User review comes AFTER completion.** Errors/failures the user reports are logged to Failure Memory (`config/QUALITY_MEMORY.json`), pushed, and applied to all future generations. The only hard stop remains a missing/ambiguous/conflicting source view (docs/13 §6b) and the §4 exception list.

## 6. WHAT THIS POLICY DOES NOT WAIVE
- ~~`CLAUDE_SETUP.md` §2.5 — one approval image per catalog.~~ **Superseded by §5b (2026-07-30): full no-permission run; review after completion.**
- **`CLAUDE_SETUP.md` §0.5 — branch creation** still requires explicit user permission.
- **`docs/14` / `docs/18` quality gates.** Rejecting a drifted render is not a confirmation prompt; it is a gate. Auto-reject and regenerate silently per `docs/20`.

## 7. FAILURE MODE TO AVOID
Executing confidently on a wrong inference is worse than asking. Confidence ≥90% means the project's own rules resolve it — not that a guess feels reasonable. When ranks conflict with evidence (see §2), the evidence wins and the choice is reported.
