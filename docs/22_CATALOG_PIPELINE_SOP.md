# 22 — CATALOG PIPELINE SOP (user-locked 2026-07-30 — SINGLE AUTHORITY for per-catalog execution order)

The authoritative end-to-end sequence for EVERY catalog. Gates fail = STOP. Detail for each topic lives in its owner doc (linked); this file owns only the ORDER and the gates. Runs under docs/19 §5b (no-permission full run) and docs/13 §6b (D2D pixel-perfect source read).

## P0 — GATES (fail = STOP, never proceed)
1. Load: `docs/13` JEWELRY_PRESERVATION · `docs/03` IMAGE_GENERATION_RULES · `docs/04` LOGO · `docs/11` BACKGROUND · `docs/19` APPROVAL_GATE · `docs/17` TOKEN · DELIVERABLES · ROMANTIC_POSES · `config/QUALITY_MEMORY.json` (Failure Memory + Approved Benchmarks). Any fails to load = STOP.
2. Read source CAD — every view, once, in-thread, D2D pixel-perfect. Missing / conflicting / non-CAD (model photo) view = STOP and ask.
3. Confirm one SKU, one ring. Two designs in source = STOP.

## P1 — SPEC
4. Write `LR-XXXX_SOURCE_SPEC.md` from source pixels only — full field list per docs/13 §6b. Zero inference, zero category priors.
5. Append SKU Failure Memory section (carry forward all prior global rules).

## P2 — PROMPT
6. Build master prompt: full geometry lock + explicit NEGATIVES from Failure Memory (NO hidden halo, NO added diamonds, NO double prongs, NO extra jewelry piece, exact scale).
7. Attach format lock: 1:1, 2K min, native, tack-sharp, sRGB, no watermark.
8. Assign the 10 slots by the LOCKED NUMERIC ANGLE MATRIX (docs/12 A-MATRIX) — 4 office + 6 lifestyle. Each prompt states azimuth + elevation + distance/crop as NUMBERS; filenames are labels only. Obey the SEPARATION RULE (no two within 20° azimuth AND 15° elevation; elevated 3/4 only in slot 04). One image per angle, never repeated.
9. Set catalog theme — consistent within, distinct from every prior catalog. Non-generic models/wardrobe. Banned: beige knit + neutral couch.

## P3 — GENERATE
10. Fire all 10 in ONE batch. No prompt echo, no gallery widget, no agent.
11. Auto-retry concurrency caps / failures until all 10 land.

## P4 — VALIDATE
12. Script check: exists · size>0 · 2048×2048 · 1:1 · PNG.
13. Visual check vs SOURCE_SPEC (spot-check within budget): prong count/type · halo present/absent · pavé rows · facet pattern · band profile · one piece only · true-to-finger scale · logo integrity · no watermark · 1:1 square lock (2048x2048).
13b. ANGLE VALIDATION GATE (docs/12 A-MATRIX): read each render's ACTUAL azimuth/elevation from the image (not the filename); reject any slot that mismatches its declared numbers; compare all 10 pairwise, reject the later slot of any pair within 20° azimuth AND 15° elevation, regenerate azimuth +30° / elevation re-forced; repeat until all 10 distinct. Never deliver a duplicate angle.
13c. ACCENT/PAVÉ COUNT GATE (docs/13 §6c, validate_render G2, MANDATORY every render): detect accent stones per run; reject if outside spec count ± tolerance; re-fire the SAME frozen call with the failed constraint appended to negatives (max 5). Diffusion cannot count — never deliver an unchecked render.
14. Any fail = auto-regenerate that slot with a tightened negative. Never deliver a fail.

## P5 — DOWNLOAD
15. Download all 10 to the SINGLE output store `deliveries/<SKU>/` (gitignored). ONE bash call, in-thread. No agent, no subagent.

## P6 — RECORD
16. Write `manifest_LR-XXXX.json`.
17. Log every rejection as MISTAKE / CAUSE / RULE → Failure Memory.
18. Log every pass as Approved Benchmark (ID + spec text, not the image).
19. Update `config/QUALITY_MEMORY.json`.

## P7 — HYGIENE
20. Safe-delete strays → `tmp/_trash/` (never rm -rf). Duplicates, temps, superseded manifests, empty dirs only. Never specs/memory/code.
21. Enforce `.gitignore`; untrack any tracked image (`git rm --cached`).

## P8 — PUSH (defines completion)
22. Commit `LR-XXXX: spec + failure memory + manifest` → push main. Images NEVER pushed. Push fails = catalog NOT complete = auto-retry.

## P9 — REPORT
23. ONE line: `LR-XXXX: 10/10 OK · pushed · repo clean · COMPLETE`

## DETERMINISTIC ENFORCEMENT (code — user-locked 2026-07-30, ALL categories)
Text prompts cannot count or hold ratios, so the guarantees are CODE, not wording. `run_catalog.py <SKU>` chains:
- **Source intake gate** — `scripts/validate_source.py` (blocking): required views per category (`config/view_requirements.json`), zero watermark (OCR/heuristic), one CAD design (focal pHash), skin <5%. Fail = STOP, names the missing item.
- **Machine-readable spec** — `specs/<SKU>.json` (category-agnostic schema). Every prompt is GENERATED from it by `scripts/build_prompts.py`; no hand-written geometry text anywhere. Null fields auto-skip their gates.
- **FROZEN generation call** — the Higgsfield call is unchanged: same tool/model, resolution 2k, aspect_ratio 1:1, count 1, ALL slots in one batch, medias order [pose/studio ref, SOURCE piece]. **No img2img, no denoise/strength, no compositing of the jewelry.** Every fix sits OUTSIDE the call. `run_catalog.py --emit-plan` emits the per-slot plan honoring these constraints.
- **Render gates G1–G11** — `scripts/validate_render.py` (blocking, every image; `config/angle_matrix.json` for angles). Any confident fail → **re-fire the SAME unmodified call for that slot with the failed gate's constraint appended to the prompt NEGATIVES** (no other change), max 5 retries, else STOP and report slot+gate.
- **Failure memory → regression** — `memory/failures.json` (machine-readable) + `tests/golden/cases.json` + `tests/run_gates.py`. Every rejection adds an entry + a case; a gate that stops catching a past failure fails the build. Deps: `requirements-gates.txt`.
Gate accuracy note: G2–G8/G10 are heuristic, calibrated against `tests/golden`; only a confident fail rejects (unmeasurable never blocks). G1/G9/G11-text are robust.

## BUDGET
≤15k tokens whole catalog. Savings come from what is DISPLAYED, never from source fidelity, prompt detail, or validation. See `docs/17`.
