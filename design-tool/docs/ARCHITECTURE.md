# Architecture — 5 layers

The whole tool is one idea repeated: **structured parameters flow forward; nothing
downstream re-invents geometry.** `design-DNA` (see `schema/design-dna.schema.json`) is
the contract that ties the layers together.

```
        ┌───────────────────────────── design-DNA (JSON) ─────────────────────────────┐
        │                                                                              │
 ① TREND        ② GENERATOR            ③ CAD BUILD          ④ RENDER       ⑤ VALIDATE
 aggregate      parameters +           Rhino/Grasshopper    KeyShot /      rules + cost
 tag · rank     rules → variations     → .3dm / .stl        WebGL / AI     → retail
 → propose                                                  concept
   params
```

## ① Trend Intelligence  (`trend/`)
Scrape Pinterest/IG/TikTok/Etsy/retailers/Google-Trends → CV+NLP normalise each piece to
`taxonomy.json` attributes → rank momentum → **propose** hot, buildable `design-DNA` that
fills gaps in the current catalog. `trend_engine.py` is the scaffold; adapters are TODO.

## ② Parametric Generator  (`web/configurator.html` today)
A `design-DNA` set + a rule system. The configurator is the interactive front of this:
every control is a parameter; the geometry regenerates live. Because outputs are valid
parameter sets, they are manufacturable by construction. (Future: batch-generate variant
families by nudging the DNA; score with an engagement predictor.)

## ③ CAD Build  (`cad/`)
`design-DNA` → **Rhino + Grasshopper** (the engine under MatrixGold) → clean NURBS →
`.3dm` (master) + `.stl` (print). `rhino_build.py` documents the exact parameter→geometry
map; `cad/grasshopper/README.md` sketches the definition graph. **This is the deterministic
step — geometry is *constructed*, never drawn** — the core lesson carried over from the
image-generation project (where letting a model draw geometry caused endless drift).

## ④ Render / Preview
Three views of the same design at increasing fidelity:
- **Configurator SVG** (now) — instant schematic, zero cost.
- **AI concept render** (Higgsfield) — photoreal mood, for marketing; needs credits.
- **CAD render** (KeyShot/V-Ray) or a WebGL turntable — true geometry, rotatable.

## ⑤ Manufacturability + Cost  (`cad/manufacturability.py`)
Runnable now. Rules (min wall, prong Ø, band width, ratio-vs-cut drift) + a cost estimate
(metal weight × spot + stones + labour → ×multiplier retail). Turns a pretty design into a
**business decision** and gates it before casting.

## Feedback loop
Render candidates → score engagement/virality → shortlist winners → feed the winning
attribute combos back into ① as raised weights. The system learns what sells.

## Non-goal (for now)
Auto-converting an arbitrary sketch or AI image into clean parametric CAD. Image→3D gives
meshes, not production NURBS with stone seats. Stay parametric-first; treat sketch→CAD as a
later R&D module.
