# CAD build — Rhino + Grasshopper (Matrix)

The layer-3 engine. **MatrixGold / RhinoGold are built on Rhino**, so Grasshopper is the
programmable way to turn a `design-DNA` JSON into real NURBS CAD deterministically.

## Recommended definition graph

```
[JSON in]  ── GhPython/Colibri ──▶ read design-DNA
     │
     ├─▶ Stone loader   (cut → /stone-library/<cut>.3dm, scale to carat+lw, orient)
     ├─▶ Head builder   (prong array  OR  bezel offset+extrude+seat)
     ├─▶ Composition     (solitaire / hidden-halo array / bypass / three-stone rail)
     ├─▶ Shank sweep     (profile curve by band.profile, width, along rails)
     └─▶ Assemble        (boolean union, seat subtract, fillet)
                              │
        ┌─────────────────────┼─────────────────────┐
     [.3dm]                 [.stl]                [render]
   NURBS master         print / cast          KeyShot / V-Ray
```

## Why parametric, not mesh-from-image
- A GhPython node reads the JSON and drives clean **NURBS** solids → real stone seats,
  correct prong counts, castable walls. Manufacturable **by construction**.
- Image→3D (photogrammetry / `generate_3d`) yields **meshes**, not production NURBS with
  seats — fine for a quick visual, not for the bench. Keep that path out of the critical flow.

## Bridge options
- **Inside Rhino:** `RunPythonScript ../rhino_build.py design.json` (see that file's map).
- **Headless-ish:** `pip install rhino3dm` for geometry I/O; drive Grasshopper via
  `GH_CPython` / `hops` / Rhino.Compute for a server.
- **Commercial reference:** Gemvision **CounterSketch** already does JSON-ish parametric
  style→CAD→render for retailers. Study it; our edge is the trend engine feeding parameters.

## Next task
Author `ring.gh` with the graph above, exposing every `design-DNA` field as a GH input,
and a `cook(json)->{'3dm','stl','png'}` entry point.
