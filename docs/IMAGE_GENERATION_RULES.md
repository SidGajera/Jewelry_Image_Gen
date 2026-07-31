# IMAGE GENERATION RULES (LOCKED)

Scope: pipeline & output mechanics. (Design approval = APPROVAL_GATE; Jewelry = JEWELRY_PRESERVATION;
Lifestyle theme/scenes = DELIVERABLES_PER_CATALOG.) User-locked 2026-07-31.

## Mandatory verification (highest priority, every image, every catalog)
- Before delivering ANY image, verify the jewellery and scene are GEOMETRICALLY, LOGICALLY, and PHYSICALLY correct. Mandatory for every future catalog.
- Reject and regenerate if anything is geometrically wrong, logically impossible, or physically impossible.

## Hand & placement logic (HARD — every image)
- Hands 100% realistic, anatomically correct: EXACTLY 5 fingers per hand — never 6, never 4, no extra/missing/fused/duplicated fingers; natural joints, knuckles, nails, proportions.
- Ring on ONE finger ONLY. NEVER across two fingers or spanning the gap — physically impossible.
- Ring seated at the base of one finger, correct real-life size, natural pose.
- Validate before output: 5 fingers/hand, ring on ONE finger, no impossible anatomy/placement.

## Resolution (HARD)
- EVERY image 2K — no compromise.

## Auto run & permissions
- Take ALL permissions ONCE at start, then run fully AUTO across all images/catalogs. Never re-ask per image/catalog. (App-controlled popup; user sets "Always allow" once.)

## NO HIGGSFIELD WIDGETS (HARD)
- STRICTLY never render/open any Higgsfield widget or gallery in chat.
- Never call: show_marketing_studio_generations, job_display / "Display Result", show_generations, media_upload_widget, or any tool that opens a gallery/grid/preview/widget.
- Do not review/list/fetch generations via a widget. If a URL/ID is needed, take it directly from that generation's own result already in hand.
- User previews results in Higgsfield directly; deliver only a short final status line.

## Pipeline (HARD)
- Higgsfield pipeline ONLY for ALL image generation.
- NO Python/PIL or any local compositing/image-editing to build deliverables (scrap — floating rings, fake look).
- Method: Higgsfield IMAGE-TO-IMAGE with the source CAD as a STRONG structure-lock reference — the exact ring preserved while Higgsfield renders the scene. Feed the matching source CAD angle as the reference for each shot.

## Preserve mode — Higgsfield only (HARD)
- Preserve mode = Higgsfield ONLY. Never Python/PIL at any step.
- Use the Higgsfield subject-preserving edit/reference model to keep the EXACT source ring (shape, stones, claws) while changing the scene (held the exact pointed hexagon for LR-0198 — primary method).
- If i2i/preserve still can't hold geometry at scene scale (emerald-drift): transfer only via Higgsfield's own edit/inpaint/reference tools — never Python.

## Emerald-drift fallback (decision order)
1. Preserve-model first (works — exact hexagon on 0198).
2. If a SKU still drifts to emerald on ALL Higgsfield models: deliver only the 4 exact-source OFFICE velvet angles and SKIP lifestyle for that SKU.
3. NEVER approve local/Python pixel-compositing.
4. NEVER accept the emerald look — wrong diamond shape is never acceptable.

## No AI-redraw of jewellery (HARD)
- Ring preserved from source CAD, never invented from the model's prior (fails ~99.99% — defaults to emerald/wrong stones). Source-lock via Higgsfield i2i so shape/stones/prongs/band stay exact.
- If exact design isn't available at the needed angle/scale, STOP and re-check source. Never fill the gap with an imagined ring.
- Only camera angle + background/scene change.

## Output
- No watermark, logo stamp, text, signature, label, or overlay. Clean image only.
- Deliver only the single final photo — no before/inset/thumbnail/split-frame/reference box.

## Silent operation
- No code, commands, JSON, tool output, logs, widgets, or in-chat image previews. User previews in Higgsfield.
- Do not re-download/decode/read large CAD files each run — view once, save SOURCE_SPEC, reuse; use the CAD only as the Higgsfield reference input. Avoid big base64/JSON/URL dumps and verbose retries.
- Reply only with a short final status line.

## Physical & anatomical plausibility
- Correct number of people; each arm/hand traces to the correct body/shoulder; no extra/missing/contradictory limbs; exactly 5 natural fingers per hand; ring on ONE finger (never spanning two); plausible ring-hand position; consistent perspective, gravity, light direction.
- Ring band structure physically possible — one continuous shank (or exactly source); never extra/duplicate bands.
- Everything natural/real — nothing artificial/AI-looking.
- Jewellery is the sole focus (esp. lifestyle): ring/diamond sharpest; people/background softer (shallow DOF). Natural sparkle without changing the stone.
- Impossible poses/anatomy = REJECT.

## Validate BEFORE generation
- Run ALL checks at the planning stage, before generating — never generate first and reject after.
- Load all policies + Failure Memory + approved benchmarks; self-check against every past instruction. Never repeat a corrected mistake. Record any new failure.
