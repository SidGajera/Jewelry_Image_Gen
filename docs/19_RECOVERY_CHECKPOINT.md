# 19 — RECOVERY CHECKPOINT (user-locked 2026-07-18)

Fresh pull of `desktop-pc` restores the full workflow automatically. Load `00` POLICY INDEX first; every rule below is already committed and active on pull — no re-prompting needed.

## Active permanent rules → where they live
- **Permanent Token Optimizer / targets** → `17` PERMANENT TOKEN-COST OPTIMIZATION (controlling summary) + PERMANENT TOKEN OPTIMIZATION + TARGETS (<3k/image, cache once, incremental).
- **Safe-optimization guardrails (never trade quality/geometry/pipeline for tokens)** → `17` SAFE-OPTIMIZATION GUARDRAILS — NON-NEGOTIABLE.
- **Token-report honesty (measured vs estimate, never fabricate)** → `17` TOKEN REPORTING — HONESTY.
- **Short-output policy (≤3 lines, one-sentence default)** → `17` DEFAULT RESPONSE STYLE + OUTPUT POLICY (PERMANENT).
- **Silent execution / no reasoning-planning narration** → `17` INTERNAL REASONING & USER OUTPUT + OUTPUT POLICY.
- **No bash/shell display, no tool-output narration** → `17` OUTPUT POLICY.
- **No thinking/progress narration** → `17` OUTPUT POLICY + NO EARLY TERMINATION progress-line rule.
- **No Higgsfield preview widget / silent generation** → `17` NO PREVIEW WIDGETS / SILENT GENERATION.
- **Full file path with drive name** → `17` FILE PATH REPORTING.
- **One image per angle / camera uniqueness (≤20%)** → `12` MASTER CAMERA UNIQUENESS + ONE IMAGE PER ANGLE.
- **Cached policies/CAD/logo/cloth/failure memory; never reload** → `17` SESSION cache + DIFFERENTIAL EXECUTION.
- **Retry budget (max 2 credited/angle, then skip)** → `17` RETRY BUDGET & CREDIT CONTROL.
- **Pipeline: Higgsfield only** → `15` §0.
- **Jewelry geometry / D2D / twist / head-shoulder / bottom-shank / no-invention** → `13` (+ `16`).
- **Diamond consistency, metal colour, photorealism/anti-CGI, lifestyle set, no-text/watermark** → `03`.
- **Cloth (pure white cotton) + benchmark** → `11`.
- **Logo: master lock (preserved artwork), embedded print, jewelry-first/subtle, visibility, matte params** → `04` §14.0–§14.2, §14.1b–§14.1g.
- **Catalog consistency gate (pre-gen + final validation)** → `18`.
- **Failure/Quality Memory (incl. FM-0163 ref-text, FM-0164 band artifact, LR-0159 F1–F4, twist recurrences)** → `07` + `config/QUALITY_MEMORY.json`.
- **Approval + catalog git rule** → `03` + `15` §8.5.

## Catalog state (delivered, `config/deliveries/`)
LR-0149, 0151, 0152, 0153, 0154, 0155, 0156, 0157, 0158, 0159, 0161, 0162, 0163, 0164, BRACELET-01. Parked: LR-0150.
Delivery records: `config/deliveries/LR-0159|0161|0162|0163|0164|BRACELET.json` (design profile, workflow, reference media IDs, angle map). Output PNGs live in `D:\Lucent Image generation\workspace\output\<SKU>` (gitignored → Drive); golden sources in `workspace/golden/<SKU>`.

## Branch rule
All work stays on `desktop-pc`; never merge/checkout/rebase/update `main`; push only to `origin/desktop-pc`. `main` and `desktop-pc` remain diverged by design (`00` / `project_policy_index`).
