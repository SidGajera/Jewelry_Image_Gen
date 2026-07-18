# 14 — NO-REGRESSION POLICY (production quality ratchet)

User-locked 2026-07-16. Quality may only go UP. Every change is measured against the last approved output; if any change reduces fidelity, realism, or consistency, it is rejected and rolled back. This is what lets the pipeline improve over time without ever silently degrading what already works.

## 1. NEVER REGRESS
- The **last approved pipeline + configuration** is the baseline (recorded per SKU in `config/deliveries/LR-XXXX.json`; pipeline defaults in `tool/backend/lib/pipeline/`).
- Every change runs the fixed **golden regression suite** (§4) before it is kept.
- Results are compared to the previous version. **If even one critical metric gets worse → reject the change and roll it back.**

## 1.5 GLOBAL REGENERATION LOCK + MASTER DESIGN LOCK (user-locked 2026-07-18, applies to EVERY image of EVERY catalog)
Before every generation: load this policy + `config/QUALITY_MEMORY.json` (approved patterns + failure memory) + all recorded failures for the current design, and validate the plan against every recorded failure first. If any prior failure would repeat, reject internally and regenerate automatically. Every rejected image permanently records **Failure / Root Cause / Prevention Rule**; the same failure must never reappear in any future image of this design or any later catalog.

**MASTER DESIGN LOCK** (jewelry geometry) is owned by `docs/13_JEWELRY_PRESERVATION_SPEC.md` — see it for the full component list and the "AI may only change camera/lighting/environment, never geometry" rule. This section owns only the *process* that enforces it: load → validate-against-failures → reject-and-regenerate → record.

**CONTINUOUS-LEARNING LOOP (user-locked 2026-07-18; this section owns the loop; owners below own the rules):** after every generation — approved OR rejected — compare the output against the source CAD and each owning policy (geometry `13`, logo `04`, cloth `11`, camera/lighting `03`/`12`, plus Quality Memory + Failure Memory), scanning every axis: jewelry geometry, hidden structure, side/rear fidelity, diamond proportions, prongs, gallery, band profile, cloth, logo, lighting, materials, physics, render quality. For each NEW issue: find the root cause → check which owner already covers the topic → **update only that owner** (never copy the rule elsewhere); create a new policy only for a genuinely new responsibility. Record the failure once in Failure Memory (`config/QUALITY_MEMORY.json`, schema in `07`): `Failure ID · Root Cause · Prevention · Affected Policy · Status`. Apply every learned prevention forward to the next image, the rest of this catalog, and every future catalog/project. A solved failure must never reappear; if it does, treat it as a **regression** and STRENGTHEN the existing prevention rule — never add a duplicate. Goal: each generation improves the next, each catalog improves the next, while keeping one source of truth per policy.

**STRUCTURAL CONSEQUENCE (must be acknowledged, not silently violated):** Higgsfield in-model generation *re-synthesizes* the jewelry every render — it cannot literally reuse the master's pixels, so on any angle where geometry drift is visible (side / rear / three-quarter / elevation) it will always risk failing this lock. The ONLY method that satisfies "AI must not generate the jewelry geometry" by construction is **compositing the real source-ring pixels** (§2 — geometry guaranteed by provenance), which is currently BANNED by `15` §0 Higgsfield-only. Therefore, under Higgsfield-only, the compliant outcomes for a geometry-critical angle are: (a) use it only where face-on drift is negligible and validates (hero top-down, front 45°, front worn macros), or (b) **SKIP** the side/rear/three-quarter angle (`15` §5 skip-don't-invent). Delivering an in-model side/rear render as CAD-exact is not achievable — do not claim it. Reconcile the two locks with the user before promising CAD-exact side geometry.

## 2. PASS/FAIL METRICS (checked automatically before delivery)
Split by how each is actually verified — because the composite pipeline uses the REAL source-ring pixels, every ring-geometry metric is **guaranteed by construction** (provenance), and only scene-level metrics need vision/manual review.

Guaranteed by composite provenance (deterministic — `lib/pipeline/qc.qc_final`):
- ✅ Ring geometry unchanged · ✅ Stone shape unchanged · ✅ Stone orientation unchanged · ✅ Stone size unchanged · ✅ Metal thickness unchanged (all = source pixels)
- ✅ Output 1:1 + ~2K

Verified per-shot (params / vision / approval gate):
- ✅ Ring scale on finger correct (placement defaults + first-image approval)
- ✅ Logo physically printed (studio; provenance flag + fabric-print realism, docs/04)
- ✅ Cloth realism · ✅ Lighting consistency · ✅ No AI artifacts (scene-level; approval gate / optional vision)

**If any metric fails → do NOT deliver.**

## 3. INCREMENTAL IMPROVEMENTS ONLY
Never change prompt + pipeline + preprocessing + compositing + logo system + masking + QC all at once. **Change one thing, run the suite, keep it only if it improves (and regresses nothing).** One variable per commit so a regression is attributable.

## 4. GOLDEN REFERENCE CATALOG (permanent regression dataset)
A fixed set of reference rings every change must pass — covering the design space that has drifted before: **Halo · Solitaire · Infinity/twist · Emerald eternity · Pavé · Three-stone · Hidden halo**, across **yellow / white / rose gold**. Target 10–20 SKUs. Defined in `config/golden_catalog.json`; source images live under `workspace/golden/` (operator-provided real CAD views — never fabricated). The harness (`lib/pipeline/regression.py`) runs the pipeline over all of them and asserts the guarantees in §2.

## 5. ROLLBACK ON REGRESSION
If the suite's success rate drops below the previous version: **revert the change, restore the previous configuration, and keep investigating in an isolated branch/workspace until it's actually better.** The revert is a gated step (a human/agent runs it after reading the diff) — the repo does not auto-rewrite history on a metric threshold. `main` always holds the last non-regressing version.

## 6. QUALITY-FIRST WORKFLOW (per catalog)
Unchanged from the locked catalog-approval workflow (`docs/10`, CLAUDE_SETUP §2.5): generate ONLY Image 1 → correct until the user approves → then auto-generate the rest with the SAME validated settings. Exactly one approval per catalog.

## 7. STABLE REPOSITORY
`main` always stays runnable: fresh clone → configure `.env` → one setup command (`scripts/setup.*`) → start (`scripts/start.*`) → generation-ready. `scripts/health-check.*` verifies structure + locked-asset checksums without spending a credit. **No experimental change may make the main workflow worse** — if it does, it does not belong on `main` (§5).

## 8. RELATED
`docs/13_JEWELRY_PRESERVATION_SPEC.md` (geometry + QA checklist) · `config/QUALITY_MEMORY.json` (`no-regression-policy`, `geometry-immutable-auto-fallback`, `catalog-approval-workflow`) · `tool/backend/lib/pipeline/` (composite pipeline + regression harness) · `config/golden_catalog.json`.
