# 27 — D2D PIXEL-PERFECT CHANGEOVER (PREPARED, NOT ACTIVE)

**Status: prepared, awaiting authorization.** Production is unchanged. Nothing in
`policy/registry.json`, `config/engines.json` or `run_catalog.py` has been switched by this
document. Written 2026-08-21 on the user's decision that *pixel-perfect D2D wins* over
"every delivered pixel is generated".

To activate, the user must give the exact sentence from `docs/21` §1a:

> **Change the image generation pipeline.**

Nothing else authorizes it — not this document, not a menu selection, not a quality
complaint. That ceremony exists so the production path never moves on inference.

## 1. What the user asked for

> "Jewelry must not redesign or redraw with AI; jewelry from source image must be
> pixel perfect d2d design." — 2026-08-21

Also restated: every stone clear, natural and real.

## 2. Why the current pipeline cannot deliver it

| rule | status | says |
|---|---|---|
| `ENGINE_ORDER` | **active** | ALL delivered pixels come from Higgsfield `generate_image`; Python may not composite or write pixels; geometry enforced by catch-and-retry |
| `STONE_EQUALITY_LOCK` | **aspirational** | every stone equals its source counterpart — never enforced |
| `GEOMETRY_FROM_SOURCE` | superseded | *"Text-to-image cannot hold stone-size ratios (proven LR-0203/0206/0211, 3%–53% framing); this path makes geometry exact by construction."* |

Catch-and-retry narrows drift; it cannot eliminate it. The registry already records the
evidence — three catalogs measured between 3% and 53% framing error. "Pixel-perfect" and
"100% generated" are mutually exclusive claims, and the honest reading is that the current
pipeline delivers *approximate* geometry with gates, which is why the equality rule was
parked as aspirational rather than enforced.

## 3. What activation would change

**The jewellery layer stops being generated and starts being placed.**

* Higgsfield still renders 100% of the scene — velvet, cloth, hands, skin, wardrobe,
  environment, light, shadow. Engine 1 does not change, its call shape does not change.
* The jewellery is composited from the **source CAD cutout** by whole-asset affine transform
  only — scale, rotate, translate. Never redrawn, never generatively filled inside the
  jewellery bounds, no per-stone edits.
* Tooling already present and verified importable on 2026-08-21:
  [`scripts/composite_ring_into_scene.py`](../scripts/composite_ring_into_scene.py)
  (`composite(scene, ring, scale, pos, key, feather, shadow, match_white)`) and
  [`scripts/_cv_lib.py`](../scripts/_cv_lib.py); numpy 2.5.1 + pillow 12.3.0 installed.
* Provenance returns: each delivery carries its source cutout name + sha256 and asserts
  whole-asset affine only — the retired `G19_COMPOSITE_PROVENANCE` discipline, whose text is
  preserved on `ENGINE_ORDER.superseded_learning`.

## 4. What it costs — state this plainly before activating

1. **`ENGINE_ORDER` must be superseded**, because it forbids Python writing delivered pixels.
   Its successor keeps everything else verbatim (frozen call shape, catch-and-retry, engine-2
   rules) and carries all 10 failure_cases plus `superseded_learning` forward — enforced by
   `policy/check.py` 1d.
2. **`STONE_EQUALITY_LOCK` becomes enforceable** and should move `aspirational` → `active`,
   since compositing is what makes it true by construction.
3. **Pixel-perfect applies to the jewellery only.** Scene, light and shadow remain generated,
   so a composite still has to pass the realism gates — a perfectly-placed ring in an
   implausible scene is still a reject.
4. **Lighting match is the new failure mode.** The old composite path's failures were
   `cutout_hash_mismatch` and `missing_provenance`, not geometry — that risk moves from
   "wrong shape" to "right shape, wrong light". `neutral_gain` / `match_white` exist for this.
5. The pipeline was reversed once before (2026-07-21, "use only Higgsfield", "do not ask
   again"). Activating reverses that reversal, so it should be a deliberate, recorded choice.

## 5. Activation checklist (do not run without the sentence)

1. User gives: **"Change the image generation pipeline."**
2. New registry rule on key `generation.engine`, superseding `ENGINE_ORDER`, carrying its
   failure_cases + `superseded_learning` (check 1d enforces this).
3. `STONE_EQUALITY_LOCK` → `active`, wired to gate `G21_STONE_RATIO`.
4. `config/engines.json` — engine 1 record gains the composite stage; `no_compositing: true`
   in `call_constraints` becomes false for the jewellery layer only.
5. Re-enable provenance sidecars (cutout name + sha256) and the G19 assertion.
6. `run_catalog.py` — composite stage between generation and the render gates.
7. Full verification: `policy/check.py` 0 STOP, `scripts/engine.py --check`, both gate suites,
   then one pilot SKU end-to-end before any batch.
