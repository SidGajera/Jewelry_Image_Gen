# 18 — LUCENT CARAT LAB · ZERO-TOLERANCE JEWELRY QC POLICY (user-locked 2026-07-16)

**Governing mindset.** The jewelry is the product being sold. Act as a **quality-control inspector whose primary job is to REJECT any generation that changes the jewelry** — not as a helper trying to make a nicer picture. Never "improve," soften, or accept a drifted ring. If there is any uncertainty, **regenerate instead of modifying the jewelry.** A missing/rejected image is acceptable; a redesigned ring is not.

This policy sits ABOVE aesthetics and ties together the existing locks (`docs/13` preservation spec, `docs/16` zero-invention, `prompts/00` master prompt, `QUALITY_MEMORY`). On any conflict, preserve the jewelry.

## Automatic rejection conditions
Discard the image and regenerate if ANY of these differ from the source:
silhouette · halo shape/size · center-stone shape · diamond proportions · prong count · prong position · prong thickness · gallery geometry · basket geometry · shoulder geometry · band width · band thickness · stone count · stone spacing · pavé layout · open spaces · negative spaces · curves · loops · symmetry · camera angle (unless a different angle was explicitly requested).

## Camera lock
Do not estimate the camera angle — match the uploaded reference exactly. Front = Front, Side = Side, 45° = 45°, Top = Top. Never rotate the ring unless explicitly instructed.

## Structural lock
Treat the ring as a rigid, immutable object.
- **Allowed to change:** background · cloth · lighting · reflection · contact shadow · environment · depth of field.
- **Forbidden to change:** geometry · metal · diamonds · structure · CAD · dimensions · the perspective of the ring itself.

## Review-first workflow (every request — do NOT just "generate an image")
1. **Analyze** the source ring first.
2. **List** the critical geometry that must be preserved (prongs/basket/gallery/shoulders/pavé/stone count/proportions/camera).
3. **Lock** that geometry internally (short, measurable OBJECT-LOCK constraints — not long prose; short beats verbose for the model).
4. **Generate** only the new scene.
5. **Compare** the output against the source on every locked item.
6. **Deliver only if the comparison passes.** Otherwise regenerate. Repeat; do not return the first imperfect result.

## Self-verification checklist (before delivery)
Same silhouette? · same gallery? · same basket? · same prongs? · same shoulders? · same pavé? · same stone count? · same proportions? · same camera angle? — if any answer is **No → regenerate.**

## Honest limitation + how verification actually runs here
The image model may still alter details; this review-first loop **catches obvious deviations and triggers another attempt** rather than shipping the first flawed output — over many SKUs it is far more reliable than prompt wording alone, but it is not a guarantee.
- **Verification mechanism:** the sandbox cannot download Higgsfield's output CDN (403), so step 5 runs via the **Drive read-back verify loop** (`QUALITY_MEMORY#drive-readback-verify-loop`: render lands in `LR_Verify_Inbox`, Claude downloads + compares) **or**, for an approval-gated first image, the user's visual check. Never mark step 6 "passed" without one of these actually happening — do not assume a pass.
- **Pipeline:** Higgsfield remains the active generator (`QUALITY_MEMORY#higgsfield-production-generator-lock`). Do not change the pipeline until the user instructs. On repeated drift, tighten the OBJECT-LOCK prompt and re-run on Higgsfield; the composite path is documented but not activated unless the user says so.

## AUTOMATED QC — SUSPENDED BY USER INSTRUCTION (2026-07-16)

**Do not run automated QC. Do not add it back until the user explicitly approves.** The user accepts/rejects every image manually.

- Generate → composite the preserved logo → neutralise cloth → deliver. No QC gate, no automated reject, no drift analysis, no QC report.
- Never withhold an image pending an internal check. Deliver it and let the user judge.
- Do not narrate QC, do not mention QC, do not re-propose it.

**Nothing in this file is deleted** — the standards below remain the record of what "correct" means and why. They are simply not enforced automatically. When the user says QC may return, this section is removed and the policy resumes unchanged.

**Why:** the user is the inspector. Automated QC was rejecting images before the user could see them, and the user prefers to make that call. Manual acceptance is a legitimate QC role, not the absence of one.

**Retained regardless** (these are not QC, they are hard rules): the logo is never AI-drawn (`docs/04` P0), and the preserved-logo composite remains a mandatory production stage (`docs/04` §8). Suspending QC does not authorise shipping a model-drawn logo.
