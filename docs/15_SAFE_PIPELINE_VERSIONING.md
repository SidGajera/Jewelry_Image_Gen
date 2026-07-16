# 15 — SAFE PIPELINE VERSIONING + ZERO-LOSS LEARNING

User-locked 2026-07-16. The composite pipeline is a **reversible upgrade** — it never permanently replaces the working pipeline until it proves better. Improvements are reversible; validated learning is permanent; failed experiments are recorded, not repeated.

## 1. PRESERVE THE CURRENT PIPELINE
- Git tag **`pipeline-stable`** marks the last proven-good commit (`config/pipeline_versions.json` → `stable_commit`).
- Each version's full profile (prompts, provider routing, QC, geometry, compositing) is stored per-version in `config/pipeline_versions.json` — a complete, restorable snapshot.
- The stable pipeline (`legacy`) always remains runnable and is never overwritten or deleted.

## 2. VERSIONED PIPELINES
`config/pipeline_versions.json` registers named versions:
- **`legacy`** — the incumbent prompt-based MCP workflow (full-AI scene + ring; geometry may drift). Current **stable default**.
- **`composite-v1`** — AI generates only the scene; the real source-CAD ring is composited in → geometry identical by construction. **Experimental** until it wins shadow testing (§4).
- Future: `composite-v2`, … (add a version block; never edit an existing one in place).

Select the active pipeline with **one value** — no source edits:
```
PIPELINE_MODE=composite-v1        # env overrides everything (shadow tests / CI)
```
or persist it in the registry's `active` (what rollback sets). Resolver: `lib/pipeline/mode.py`.

## 3. ONE-CLICK ROLLBACK
```
Windows:  .\scripts\rollback-pipeline.ps1 legacy
macOS/Linux: ./scripts/rollback-pipeline.sh legacy
```
Sets the active mode (restoring that version's prompt/provider/QC/geometry/compositing profile from the registry) and verifies every pipeline module still imports. The previous pipeline is usable immediately — no manual reconstruction.

## 4. SHADOW TESTING BEFORE REPLACEMENT
The new pipeline is **not** the default on arrival. For the same source, run both and compare (`dispatch.shadow_test`, `POST /shadow-test`) across: product geometry · stone shape/size/orientation/spacing · ring scale · prongs/gallery · natural placement · lighting/shadows · logo realism · overall photographic quality.
- Geometry-family categories are decided automatically (composite = guaranteed identical; legacy raw = unverified).
- Scene-family categories return **needs_human** — promotion requires that sign-off; the harness never auto-promotes on aesthetics.
- **composite-v1 may become `stable` only when it is equal-or-better in EVERY critical product-fidelity category.** If worse in any, keep `legacy` active.

## 5. AUTOMATIC FALLBACK
`dispatch.generate` (`POST /generate`) per shot: run the selected pipeline → QC → if it fails the geometry gate, fall back to the version's `fallback_to`. Direction is toward the **geometry-safe** pipeline (`legacy` raw render → `composite-v1` rescues the real ring); `composite-v1.fallback_to = null` (geometry already guaranteed). Never deliver below the approved baseline (§8). The delivering pipeline is recorded in the result trail.

## 6. LEARNING MUST NEVER BE LOST (shared, versioned store)
Learning is kept **separate from pipeline code** so rolling back code never rolls back learning:
- **Validated store:** `config/QUALITY_MEMORY.json` — read by BOTH pipelines; holds validated fixes (corrections, geometry/orientation/logo/cloth rules, prompt improvements, working composite params, QC verdicts). Approved deliveries: `config/deliveries/`.
- **Candidate store:** `config/learning_candidates.json` — new, not-yet-proven learning.
Rolling back a pipeline version must NOT delete or revert validated learning.

## 7. LEARNING PROMOTION RULE
Two stages:
- **Candidate** (`learning_candidates.json`) — a new correction/rule enters here first; it does NOT modify global production rules yet.
- **Validated** (`QUALITY_MEMORY.json`) — promoted only after it improves an output or gets explicit user approval.
If a candidate causes worse results, **disable it but keep its history + failure evidence** (`status: "disabled"` with the reason) — recorded, not repeated. Never silently delete a candidate.

## 8. APPROVED BASELINE (per SKU/catalog)
The approved first image is the catalog baseline. Each `config/deliveries/LR-XXXX.json` preserves: source files, approved first image, exact pipeline version, prompt hash, provider + model, seed (where supported), geometry profile, camera/lighting/cloth/logo profiles, user corrections, and the QC report. **Never deliver a later output that scores below this baseline on critical fidelity checks.** Schema template: `config/deliveries/_TEMPLATE.json`.

## 9. GIT SAFETY
`main` stays production-stable (repo policy = main only; risky work is isolated by the `PIPELINE_MODE` feature flag + versioned modules, not branches — no destructive change to the stable implementation). Before activating a new pipeline as stable: commit the stable state, tag it, run the golden regression suite (`docs/14`, `lib/pipeline/regression.py`), test rollback, verify both pipelines import, push all non-secret files. The old implementation is never deleted after activation.

## 10. FINAL PRINCIPLE
Improvements are reversible · validated learning is permanent · failed experiments are recorded, not repeated · the stable pipeline always remains available · no new pipeline becomes default unless it performs equal-to-or-better than the previous approved pipeline.

## RELATED
`config/pipeline_versions.json` · `lib/pipeline/{mode,dispatch,pipeline,qc,fallback,regression}.py` · `scripts/rollback-pipeline.*` · `docs/14_NO_REGRESSION_POLICY.md` · `config/QUALITY_MEMORY.json` · `config/learning_candidates.json` · `config/deliveries/`.
