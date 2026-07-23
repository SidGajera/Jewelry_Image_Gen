# Roadmap

Ship value at every phase; each phase stands alone.

## Phase 0 — MVP scaffold  ✅ (this commit)
- Live parametric **configurator** (`web/configurator.html`).
- `design-DNA` **schema** + 4 example designs.
- **Manufacturability + cost** engine (runnable).
- Trend **taxonomy** + engine scaffold.
- CAD build **spec** (parameter→geometry map, GH graph).

## Phase 1 — Trend dashboard
- Implement `trend_engine.aggregate()` adapters (start: Etsy + 2 retailer "new-in" feeds + Google Trends).
- CV tagger (cut/setting/band/metal) + NLP on captions → `taxonomy` attributes.
- Momentum ranking with real counts + engagement; weekly report; **propose** shortlist.
- *Value:* know what to design before designing.

## Phase 2 — Parametric generator → real CAD
- Author `cad/grasshopper/ring.gh` consuming `design-DNA` → `.3dm` + `.stl`.
- Stone library (per-cut NURBS). Wire configurator "Build CAD" button via Rhino.Compute/hops.
- *Value:* one click from parameters to a printable file.

## Phase 3 — Close the loop
- Trend engine auto-proposes parameter sets → batch render (configurator SVG + Higgsfield concept) →
  score with an engagement/virality predictor → shortlist → cost-gate.
- *Value:* a pipeline that surfaces sellable, buildable, priced designs weekly.

## Phase 4 — Product
- More categories (pendants, studs, bands, tennis).
- Customer-facing customizer (the configurator, skinned) → live quote → order.
- Live metal spot + real stone-supplier pricing + shop rates in `pricing.json`.
- Extract `design-tool/` to its own repository.

## Guardrails (carried from the image project)
- Parameters drive geometry; **AI never draws the final geometry**.
- Source measurement wins over any generic ratio (`schema/cut-ratios.json`).
- Estimates are labelled estimates until wired to live pricing.
