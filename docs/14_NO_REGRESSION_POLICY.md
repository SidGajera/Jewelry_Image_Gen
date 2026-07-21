# 14 — NO-REGRESSION POLICY (production quality ratchet)

User-locked 2026-07-16. Quality may only go UP. Every change is measured against the last approved output; if any change reduces fidelity, realism, or consistency, it is rejected and rolled back. This is what lets the pipeline improve over time without ever silently degrading what already works.

## 1. NEVER REGRESS
- The **last approved pipeline + configuration** is the baseline (recorded per SKU in `config/deliveries/LR-XXXX.json`; pipeline defaults in `tool/backend/lib/pipeline/`).
- Every change runs the fixed **golden regression suite** (§4) before it is kept.
- Results are compared to the previous version. **If even one critical metric gets worse → reject the change and roll it back.**

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

## REGRESSION PREVENTION (PERMANENT, user-locked 2026-07-16)

**A previously rejected mistake must NEVER reappear in any future catalog.** Every rejected image becomes a permanent regression test. Before approving or delivering any image, compare it against the checklist below. If ANY previous failure is detected: reject internally, fix, regenerate, never deliver the known failure again.

**Regression prevention outranks prompt execution.** A prompt that produces a known failure is not "executed correctly" — it has regressed.

### CHECKLIST

**JEWELRY** — geometry identical to source · no AI redesign · no gallery changes · no prong changes · no band changes · no stone-proportion changes · no added/removed diamonds · camera change only.

**LOGO** — the EXACT official logo, rendered IN-MODEL by Higgsfield (2026-07-21; local composite retired) · never garbled/recreated/redrawn/approximated/simplified/duplicated · single instance · BLACK tagline · no background wireframe · jewelry the sharp hero.

**CLOTH** — logo physically printed · cloth weave visible through the print · print follows fabric folds, perspective, lighting and cloth deformation · no floating overlay · no sticker effect · no watermark effect · no artificial opacity · no incorrect metallic finish · no isolated logo layer.

**SCENE** — ring naturally contacts the cloth · logo naturally occluded where the ring covers it · shadows consistent · lighting consistent · perspective consistent.

**OUTPUT** — compare against every previously rejected image; the same mistake reappearing is an automatic reject.

### LEARNING RULE
Once rejected, a mistake becomes a permanent production rule. That exact failure must never appear again in the current catalog, future catalogs, future sessions, or future pipeline revisions. The system must actively verify every known failure has been eliminated before delivering any image.

### RELATIONSHIP TO THE QC SUSPENSION (docs/18)
`docs/18` currently suspends automated QC at the user's instruction. **This policy requires automated verification before delivery, so for the regression checklist above, verification is ACTIVE.** The suspension covers discretionary QC judgement; it does not license shipping a known, previously-rejected failure. Where the two conflict, this policy wins.

### STRUCTURAL FINDING (verified 2026-07-16, LR-0151)
Two checklist items **cannot be satisfied by generation**, no matter the prompt:
- *"Geometry identical to source / no AI redesign"* — a diffusion model re-synthesises the ring on every render. Five prompt variants were tried on LR-0151; each drifted somewhere different (gallery/head, prong angle, stone proportions, pavé size, band thickness). Only compositing the source-CAD pixels satisfies it.
- *"Logo physically printed / weave visible through print / follows folds"* — the model can paint a flat logo on top of the cloth. Held IN-MODEL by strong prompting + QC + regenerate (2026-07-21; local composite retired) — reject any flat/overlay/pasted/duplicate logo and regenerate on Higgsfield.

Any pipeline where Higgsfield draws the ring or the logo will fail this checklist by construction. Recorded so no future session rediscovers it by burning credits.
