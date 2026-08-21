# Lucent Design Studio — AI-assisted jewelry design tool

Turn **market trends → design parameters → manufacturable CAD → render → cost**, for fine jewelry.

## The one architectural rule

> **AI decides *parameters*; a parametric engine *builds* the geometry.**
> Never let a model freehand-draw the final geometry — that's how you get wrong prong
> counts, drifted hexagons, and un-manufacturable meshes. (Learned the hard way on the
> Lucent image-generation project.) Every design is a **design-DNA** parameter set that is
> manufacturable *by construction*.

## Pipeline (industry flow, augmented)

```
① Trend Intelligence → ② Design-DNA (parameters) → ③ CAD build (Rhino/Grasshopper)
        → ④ Render/preview → ⑤ Manufacturability + cost → (⑥ cast · set · polish)
```
"Matrix / MatrixGold" is step ③ (it *is* the CAD software, built on Rhino). This tool adds
①Trend Intelligence at the front and ⑤Manufacturability+cost at the back.

## What's in here (MVP)

| Path | What it is | Status |
|---|---|---|
| `web/configurator.html` | **Live parametric configurator** — sliders regenerate the ring, spec + cost live, exports design-DNA. Open in a browser. | ✅ working |
| `schema/design-dna.schema.json` | The **core contract** — JSON Schema every design conforms to. | ✅ |
| `schema/cut-ratios.json` | L:W ranges per cut (mirrors `docs/13 §3b`). | ✅ |
| `schema/pricing.json` | Heuristic pricing constants (indicative). | ✅ |
| `cad/manufacturability.py` | **Runnable** rules engine + cost estimator (pure Python, no deps). | ✅ |
| `cad/rhino_build.py` | RhinoPython stub: design-DNA → `.3dm`/`.stl`. Parameter→geometry map documented. | 🔧 stub |
| `trend/taxonomy.json` | Attribute taxonomy for tagging market pieces. | ✅ |
| `trend/trend_engine.py` | Scaffold: aggregate → tag → rank → propose parameter sets. | 🔧 stub |
| `examples/*.json` | 4 real design-DNA files (Duality, Solstice, Meridian, Aurora). | ✅ |
| `docs/ARCHITECTURE.md`, `docs/ROADMAP.md` | The 5-layer design + phased plan. | ✅ |

## Quick start

```bash
# 1. Open the configurator
open design-tool/web/configurator.html          # or double-click it

# 2. Price + validate any design-DNA (pure Python, no install)
python design-tool/cad/manufacturability.py design-tool/examples/lr-0200-duality.json
```

## Roadmap in one line
Phase 1 trend dashboard → Phase 2 parametric generator (this) wired to Rhino →
Phase 3 close the loop (trends auto-propose designs) → Phase 4 customer customizer.
See `docs/ROADMAP.md`.

*This scaffold currently lives inside the image-gen repo for convenience; extract it to its
own repository when it grows past MVP.*
