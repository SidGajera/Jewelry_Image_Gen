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
8. Assign 10 distinct angle deltas — 4 office (white velvet) + 6 lifestyle. One image per angle/pose, never repeated.
9. Set catalog theme — consistent within, distinct from every prior catalog. Non-generic models/wardrobe. Banned: beige knit + neutral couch.

## P3 — GENERATE
10. Fire all 10 in ONE batch. No prompt echo, no gallery widget, no agent.
11. Auto-retry concurrency caps / failures until all 10 land.

## P4 — VALIDATE
12. Script check: exists · size>0 · 2048×2048 · 1:1 · PNG.
13. Visual check vs SOURCE_SPEC (spot-check within budget): prong count/type · halo present/absent · pavé rows · facet pattern · band profile · one piece only · true-to-finger scale · logo integrity · no watermark · distinct angles · portrait/square lock.
14. Any fail = auto-regenerate that slot with a tightened negative. Never deliver a fail.

## P5 — DOWNLOAD
15. ONE bash call, in-thread, output to /dev/null. No agent, no subagent.

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

## BUDGET
≤15k tokens whole catalog. Savings come from what is DISPLAYED, never from source fidelity, prompt detail, or validation. See `docs/17`.
