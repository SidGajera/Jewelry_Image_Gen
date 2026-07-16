# round-solitaire-pave-yg — proof SKU (2026-07-16 head-invention failure)

Round brilliant solitaire, 4-prong, pavé band, 18K yellow gold — the ring whose
legacy render invented a girdle support ring + reshaped gallery + thicker head.

To run the geometry-locked composite proof + shadow test, drop two files here:

```
workspace/golden/round-solitaire-pave-yg/
  source.png   # the CAD source ring on a plain/near-white background (image 1)
  scene.png    # an AI-generated hand/lifestyle scene to place the ring into
```

Then, from tool/backend (venv):
```
python -c "from lib.pipeline import dispatch; import json; \
  print(json.dumps(dispatch.shadow_test('../../workspace/golden/round-solitaire-pave-yg/source.png', \
  '../../workspace/golden/round-solitaire-pave-yg/scene.png', \
  '../../workspace/golden/round-solitaire-pave-yg/scene.png', \
  '../../workspace/temp/proof', shot_type='lifestyle', sku='round-solitaire-pave-yg'), indent=2))"
```
The composite output (real source ring in the scene) lands in workspace/temp/proof/;
the shadow report shows geometry auto-decided for composite-v1 vs the legacy render.
