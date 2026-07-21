# CLAUDE.md — LUCENT CARAT LAB IMAGE-GENERATION OPERATING INSTRUCTION

**Authoritative session instruction (user-locked 2026-07-21).** Read this first, then `CLAUDE_SETUP.md`. Follow it **autonomously**. Behaviour comes from the repository files below — never from chat history. All process decisions are already made and locked; **do not re-ask the user about them.**

---

## 1. ENGINE + PIPELINE — LOCKED (never change, never ask)
- **Generator: Higgsfield MCP only** (`docs/21`). Model `nano_banana_2`, `resolution:2k`, `aspect_ratio:1:1`, `count:1`. The server may route the edit path as `nano_banana_flash` — that is fine.
- **Pipeline: `legacy`** — Higgsfield renders the scene (`config/pipeline_versions.json` active=legacy). Do NOT change provider, model, source-loading, or lifecycle (`docs/15`, `docs/21`).
- **The logo is printed by the LOCAL COMPOSITE `scripts/print_logo_on_cloth.py` from the locked preserved asset** (user-locked 2026-07-21, LATEST — restored after in-model logo failed ~6× on LR-0180/0181). Higgsfield renders the ring on CLEAN cloth (no logo); the composite prints the ONE exact logo (BLACK tagline, single, printed-into-weave, jewelry the hero) with the approved params. Runs where the render is downloadable (desktop); this web sandbox blocks the CDN so it preps the base and hands off the composite (`docs/04` METHOD LOCK, `docs/22` §2).

## 2. BEFORE EVERY GENERATION — LOAD & ENFORCE (mandatory gate)
Load and enforce **`docs/22_PRE_GENERATION_GATE.md`** (the consolidated standing lock — §0 load-list of docs/03·04·11·12·13·14·16·21 + Failure Memory; source-jewelry lock · premium-cloth lock · official-logo lock · jewelry-first · failure memory · generation + final delivery gate) **plus the runtime trio** (`config/project_manifest.json`, `prompts/07_PROMPTS.md`, `config/QUALITY_MEMORY.json`). Do not generate until all are active.

## 3. IMAGE-GENERATION PROCEDURE (per SKU)
1. **Verify source.** Use the correct multi-view CAD (the SKU's main / 4-view CAD sheet; **gold by default**). Never use a stray, "Model", or lifestyle photo as the geometry source (`docs/19`, QUALITY_MEMORY `lr0151-source-file-selection`).
2. **Check what already exists — do not repeat (see §4).**
3. **Import** the source CAD (and the logo asset for the local composite) via `media_import_url`.
4. **New SKU →** generate ONLY image 1 (hero); verify against the gate; take the single per-catalog approval (`docs/10`). **Established standard →** go straight to batch.
5. **Batch** the remaining slots in one run, matched to the approved standard; inject every relevant failure-memory restriction into the compact prompt.
6. **Studio/packaging shots (1,2,3,10):** generate on **CLEAN cloth (no in-model logo, no background graphic)**, then print the ONE exact preserved logo with the LOCAL COMPOSITE `scripts/print_logo_on_cloth.py` (approved params; BLACK tagline, single, printed-into-weave, jewelry the hero). Runs where the render is downloadable (desktop). **Lifestyle/macro shots (4,5a,5b,6,7,8,9):** no logo. Closeup-lifestyle occupy slots 7 & 9.
7. **After each output** compare vs the source CAD, the logo benchmark, the cloth benchmark, and every recorded failure. Any mismatch → reject internally → record the failure → regenerate → never deliver it. Never claim success merely because generation completed (`docs/22` §5, `docs/21` §8).
8. **Record** each delivery in `config/deliveries/LR-XXXX.json`. Commit only on explicit catalog approval (`config/runtime.json` commit_policy).

## 4. NEVER REPEAT A PREVIOUSLY GENERATED IMAGE
Before generating any SKU or slot, check **all three**: the approved baseline (`config/deliveries/LR-XXXX.json`), the SKU's Drive folder (existing `hf_*` frames), and the Higgsfield gallery (`show_generations`). If a slot is already delivered/approved, **reuse it — do not regenerate**. Only generate **missing** or **explicitly-rejected** slots. Never re-run a completed catalog; never redo an approved image.

## 5. NEVER REPEAT A KNOWN FAILURE
`config/QUALITY_MEMORY.json` is the single Failure Memory. Before generating, load every **global** failure plus this SKU's failures, add their corrective instructions to the prompt, and block any output that repeats one. When the user rejects an image, record it **immediately** (schema in `failure_memory`) — increment `repeat_count`, never duplicate. A previously rejected mistake is never new, optional, or acceptable.

## 6. QUALITY ONLY RATCHETS UP (output never degrades)
`docs/14` + `docs/17`. The last approved output is the baseline; a change ships only if it is **equal-or-better and regresses nothing**. Never trade jewelry geometry, logo fidelity, cloth quality, QC depth, resolution, or reference strength for tokens. Output quality must not decrease from one image/session/day to the next.

## 7. AUTONOMY — DO NOT ASK + RESPONSE POLICY
Every process decision is locked in the docs.  **Execution/response contract: `docs/23`.** Execute silently; visible text ≤3 short lines; a generation run shows only `Generating...` → `Done.` (or `Stopped: <verified concise error>.`). Do not narrate reasoning/validation/model-routing. **Do NOT ask the user about** pipeline, provider, model, settings, logo method, cloth, focus/composition, source-loading, or "should I proceed / is this ok". Execute silently (`docs/19`, `docs/20`). Permissions granted once hold for the whole session. The **only** permitted pause is the single image-1 approval for a NEW SKU (`docs/10`) — and skip even that if the user has said to proceed. Ask **only** if the correct SOURCE genuinely cannot be identified.

## 8. STUDIO LOGO (LOCAL COMPOSITE, user-locked 2026-07-21 LATEST)
Studio/packaging shots carry the ONE exact preserved logo **printed by the local composite `scripts/print_logo_on_cloth.py`** from the locked asset — pixel-exact, BLACK tagline, single, printed into the weave, jewelry the sharp hero (the approved clean sample look). In-model logo is NOT used (it failed ~6× on LR-0180/0181). Higgsfield renders the ring on clean cloth (no logo); the composite prints the logo with the approved params. It needs the render downloaded, so it runs where the CDN is reachable (desktop/operator); a session whose egress blocks the Higgsfield CDN (this web sandbox, 403) generates the clean-cloth base and hands off the composite step.

---
**Precedence:** the ABSOLUTE jewelry/logo/cloth/QC locks (`docs/02`, `04`, `13`, `16`, `22`) outrank everything. `docs/22` is the consolidated gate; owning docs win on any detail. These rules are permanent for every catalog, image, session, and device.
