# 15 — SAFE PIPELINE VERSIONING + ZERO-LOSS LEARNING

User-locked 2026-07-16. The composite pipeline is a **reversible upgrade** — it never permanently replaces the working pipeline until it proves better. Improvements are reversible; validated learning is permanent; failed experiments are recorded, not repeated.
## 0. TERMINOLOGY + ACTIVE PRODUCTION PIPELINE (BINDING, user-instructed 2026-07-21)

**PRODUCTION = `legacy` = Higgsfield generates every frame, including the ring.** Set by explicit, repeated user instruction (2026-07-21: "use only Higgsfield", "do not ask again"), which **supersedes** the 2026-07-20 switch to `composite-v1`. The user wants Higgsfield to generate every shot — including worn lifestyle/close-up frames that `composite-v1` **cannot** produce (composite can only place the 2D-CAD ring at studio angles). The preserved logo is still composited locally (`print_logo_on_cloth.py`) and the cloth neutralised locally (`whiten_cloth.py`); neither is AI-drawn or AI-graded.

- **"Higgsfield"** = the only production generation ENGINE (`docs/21`). Under `legacy` it renders the scene AND the ring.
- **`legacy`** = Higgsfield generates scene + jewelry from the approved geometry-locked prompts. **THIS IS PRODUCTION.**
- **"Composite-first"** = `composite-v1`. Higgsfield renders only the scene; the CAD ring is composited in — geometry guaranteed by construction, but **studio angles only**. **Retained, NOT production.**
- **Logo is rendered IN-MODEL by Higgsfield** (user-locked 2026-07-21; the local composite is retired), held exact by prompt + QC + regenerate (`docs/04` override, `docs/22` §2).

Both versions call Higgsfield. The distinction is whether Higgsfield draws the **ring**.

**Geometry under `legacy` is NOT guaranteed by construction** — the AI draws the ring. It is held by: the strong approved geometry-lock prompt reused verbatim every shot ("EXACTLY 4 claw prongs … four not eight — count them", "pave INSIDE the lobes ONLY", "gallery/arms PLAIN POLISHED GOLD"), per-shot QC (`docs/18`, `docs/13`, `docs/16`), local logo/cloth compositing, and iteration. This is the accepted trade the user chose to get worn/close-up frames.

**Neither version may be switched automatically, in either direction.** Only an explicit user instruction changes `active`, and the pipeline choice must NOT be re-raised with the user (2026-07-21: "do not ask again"). See `config/QUALITY_MEMORY.json#composite-v1-production-lock` (updated 2026-07-21).

## 1. PRESERVE THE CURRENT PIPELINE
- Git tag **`pipeline-stable`** marks the last proven-good commit (`config/pipeline_versions.json` → `stable_commit`).
- Each version's full profile (prompts, provider routing, QC, geometry, compositing) is stored per-version in `config/pipeline_versions.json` — a complete, restorable snapshot.
- `composite-v1` always remains runnable and is never overwritten or deleted - retained for optional studio geometry-guarantee. Per §0 the `active` pointer is `legacy` (user-instructed 2026-07-21); the `stable` pointer remains `composite-v1`.

## 2. VERSIONED PIPELINES
`config/pipeline_versions.json` registers named versions:
- **`legacy`** — **PRODUCTION** (user-locked 2026-07-21, §0). Prompt-based Higgsfield workflow: Higgsfield generates the whole image INCLUDING the ring, from the approved geometry-locked prompts; the logo is rendered in-model. Fidelity held by prompt + QC + regenerate, not by construction.
- **`composite-v1`** — AI generates only the scene; the real source-CAD ring is composited in → geometry identical by construction, but studio angles only. **RETAINED, not production** (superseded 2026-07-21; it cannot produce worn lifestyle/close-up frames — §0/§5).
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

## 5. NO AUTOMATIC PIPELINE SWITCHING - QC GATES EVERY OUTPUT (superseded 2026-07-16 by §0)
**Accuracy over completeness.** `dispatch.generate` (`POST /generate`) runs composite-v1 → geometry + integrity QC. Legacy is **never** auto-run (both versions have `fallback_to: null`). If composite cannot produce a shot faithfully — a worn angle the 2D CAD can't cover, or a geometry/integrity QC fail — the pipeline does NOT fall back to AI generation. Order of preference (docs/16, hybrid policy):
1. Composite the preserved jewelry into the scene (studio, and any lifestyle angle the source supports).
2. If the angle can't be achieved faithfully → **request more source material** (additional CAD angles / a 3D CAD model → render the worn angle via FALLBACK 2, docs/13 §6).
3. If neither is possible → **SKIP that shot**. A missing image is preferable to a geometrically incorrect ring.

`deliverable=False` with `action_required` set means: do not ship, get more source, do NOT auto-run legacy. Every output must pass automatic geometry QC before delivery (§2 metrics). This reverses the earlier composite↔legacy auto-fallback — legacy redrawing the jewelry violates the ABSOLUTE jewelry-preservation rule (docs/02).

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
