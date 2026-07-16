# Golden regression set (docs/14 §4)

Permanent reference rings the no-regression harness runs on every pipeline change.

## How to add a reference ring
For each entry `id` in [`config/golden_catalog.json`](../../config/golden_catalog.json),
create a folder here and drop two real images (never fabricated):

```
workspace/golden/<id>/
  source.png   # the source-CAD ring on a plain / near-white background
  scene.png    # an AI-generated scene (cloth for studio, hand for lifestyle/closeup)
```

(Or point `source_ring` / `scene` at explicit paths in the catalog entry, like the
`SMOKE-halo-yg` row does using repo assets.)

Rows without both images are **skipped** (not failed), so the harness runs before the
full set exists. Aim for the full matrix: halo · solitaire · infinity/twist · emerald
eternity · pavé · three-stone · hidden halo, across yellow / white / rose gold.

## Run the harness (from `tool/backend`, venv)
```
python -m lib.pipeline.regression                  # run + compare to baseline
python -m lib.pipeline.regression --update-baseline # accept current as the baseline
```
Exit code is non-zero on any hard fail or a drop vs the baseline — the signal to roll
the change back (a gated step; the harness never rewrites git history itself).
