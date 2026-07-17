# 07 — QUALITY MEMORY

Dedicated memory layer for continuous improvement. Machine-readable store: [`config/QUALITY_MEMORY.json`](../config/QUALITY_MEMORY.json) — this file is its structure and rules. Loaded before EVERY generation (docs/03 generation order, step 2).

## Approved Benchmarks
- Approved jewelry renders
- Approved logo benchmark
- Approved cloth benchmark
- Approved lighting benchmark
- Approved camera benchmark

## Failure Memory
- Jewelry failures
- Physics & logical failures
- Logo failures
- Cloth failures
- Lighting failures
- Camera failures
- Logo placement & catalog composition failures

### Catalog 0150 — Head & Shank Geometry Drift — REJECTED (2026-07-17)
**Reference:** approved Image 1 (hero front) = the locked jewelry benchmark for Catalog 0150.

**Observed errors in the rejected output:** centre diamond enlarged · halo diameter enlarged · head wider and heavier · centre-stone-to-halo proportion differs · halo diamond size/spacing/arrangement altered · twisted split-shank geometry changed · shank crossing points don't match · open spaces inside the twisted shoulders differently shaped · left/right shoulder curves inconsistent · head-to-shank connection altered · ring balance and silhouette no longer match.

**Locked approved benchmark** — every future 0150 image preserves exactly: centre diamond size and proportion · halo diameter and thickness · halo diamond count, size, spacing and placement · four-prong position and shape · twisted split-shank curves · shoulder crossing locations · open-space geometry within both shoulders · head-to-shank connection · overall silhouette and proportions. **Only camera angle, ring orientation and natural photographic composition may change.**

**Prevention rule — before delivering every 0150 image:** (1) compare directly against approved Image 1 · (2) check centre-stone and halo scale · (3) trace BOTH twisted shoulders head→shank · (4) compare every crossing point and open space · (5) confirm the complete silhouette matches · (6) reject if any geometry is enlarged, simplified, shifted or reinterpreted. **The engine must PHOTOGRAPH the exact approved 0150 ring — never generate a similar twisted halo ring.**

**No-repeat rule:** the enlarged centre stone, enlarged halo and modified twisted-shank geometry must never appear again; any future 0150 output repeating them is rejected automatically before delivery.

### Logo Placement & Catalog Composition — REJECTED (2026-07-17)
**Observed failure:** the ring was positioned directly over the printed logo, hiding a significant portion of it; only the lower part of the logo remained visible, making the branding look incomplete.

**Root cause:** the composition prioritised ring centring without validating complete logo visibility; the framing did not reserve sufficient space for the full printed logo beneath the jewelry.

**Prevention rule (before finalising composition):** predict the ring footprint · predict the logo footprint · ensure the ring does NOT cover the primary logo · reposition the ring or camera if necessary · keep the complete printed logo naturally visible. **The logo may be partially cropped only by the IMAGE BOUNDARY, never by the jewelry itself.**

**Composition validation (before approval):**
- [ ] Complete logo visible · [ ] diamond icon visible · [ ] "LUCENT" fully visible · [ ] "CARAT LAB" fully visible · [ ] tagline visible unless intentionally cropped by the image edge · [ ] ring does not overlap the printed logo · [ ] logo remains naturally printed on the cloth · [ ] composition looks like a real product photoshoot

**Expected result:** the jewelry remains the primary subject while the official printed logo is fully readable and naturally integrated into the same cloth — the logo enhances the composition without competing with, or being obscured by, the ring.

**Learning:** future office photoshoots must automatically reserve adequate space for the complete printed logo during camera composition. If the logo is obscured by the ring → reject · record · regenerate with corrected framing. (Owner detail: `04` LOGO COMPLETENESS VALIDATION.)

## Learning Rules
- Every rejected image automatically records:
  - Failure
  - Cause
  - Prevention Rule
- Every future generation loads this file before generation.
- Previously recorded failures must never repeat.
- Approved benchmark images become the new reference standard.

## Continuous Learning System (user-locked 2026-07-17)
The system must continuously improve from every rejected image so that identical or substantially similar mistakes never recur.

**Automatic failure recording** — whenever an image is rejected, automatically record: failure category · affected component · root cause · violated policy · prevention rule · validation rule · correct expected behaviour. **No rejected image is discarded without updating QUALITY_MEMORY.**

**Pre-generation learning** — before EVERY new generation: load the complete QUALITY_MEMORY · apply every previously recorded prevention rule · validate the new image against every historical failure before delivery.

**Duplicate failure prevention** — compare each new image against ALL previously recorded failures. If a similar failure is detected: reject immediately · do not deliver · apply the recorded prevention rule · regenerate automatically. **The same failure must never require manual reporting twice.**

**Learning priority** — previously recorded failures outrank generation preferences. Proactively prevent known mistakes instead of repeating them.

**Regression prevention** — every successful correction becomes part of QUALITY_MEMORY. Future generations preserve successful corrections while preventing previous failures. **No solved issue may reappear.** (See `14_NO_REGRESSION_POLICY`.)

**Per-decision recording (user-locked 2026-07-17)** — for EVERY approval, correction or rejection record: result (Approved / Rejected) · successful element · failure or requested change · root cause · prevention rule · correct expected result · applicable policy section. Never create duplicate rules — merge a learning into the existing relevant policy only when it creates a permanent generation requirement (`17` POLICY MERGE RULE).

**Per-catalog learning chain** — each subsequent image must learn from: successes of previously approved images · failures of rejected images · user corrections · existing Failure Memory · Approved Benchmarks.

**FINAL CATALOG LEARNING (after a catalog is fully approved)** — review all successful images · review all rejected images · consolidate duplicate learnings · store final successes as **Approved Benchmarks** · store final failures + prevention rules here · preserve only permanent, reusable learnings · never rewrite or duplicate locked policies. Only then are commits/pushes made (`03` GIT RULE, `15`).

**MASTER LEARNING RULE** — image quality must improve continuously throughout the project. Every rejection makes the system more accurate; every approved image strengthens the approved benchmark; every future generation must show measurable improvement by avoiding all previously solved mistakes. **A mistake already identified, corrected and recorded must not appear again unless the user explicitly changes the source design or requirements.**
