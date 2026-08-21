# From Zero → AI Auto-Jewelry-Design Tool
## Requirements analysis + start-to-end build playbook (for a non-jeweler using AI to build it)

You do **not** need to be a jeweler. You need (a) the handful of jewelry words below, (b) a
clear spec, and (c) the discipline to make an AI coding tool build it **one small piece at a
time**. This doc gives you all three.

---

## PART 0 — Jewelry basics you must know (10-minute primer)

You only need this much vocabulary to write requirements:

**Ring anatomy**
- **Shank / band** — the round part around the finger.
- **Head / setting** — the part that holds the main stone.
- **Prongs (claws)** — little metal fingers gripping the stone (usually 4 or 6).
- **Bezel** — a metal rim hugging the stone instead of prongs.
- **Gallery / basket** — the openwork under the stone.
- **Halo** — a ring of tiny stones around the main stone. **Hidden halo** — that ring sits
  *under* the stone, only seen from the side.

**Stones**
- **Cut / shape** — round, oval, emerald, hexagon, marquise, pear, cushion, princess…
- **Carat (ct)** — the stone's *weight* (not size). Bigger carat ≈ bigger stone.
- **mm** — the actual measured size. You convert carat→mm with formulas (already in our code).
- **L:W ratio** — length ÷ width. A round is 1.0; a marquise is ~2.0 (long and pointed).
- **Lab-grown vs natural** — same look, lab is cheaper. Assume lab-grown.

**Metal**
- **Gold karat** — 18k / 14k (purity). Colors: **yellow / white / rose**. Also **platinum**.

**Making it (why "manufacturable" matters)**
- Industry flow: **sketch → CAD (3D model) → render (photo) → cast (make it in metal) → set stones → polish.**
- **CAD file types:** `.3dm` (Rhino), `.stl` (for 3D-printing/casting), `.step` (universal CAD).
- **Casting** needs minimum metal thicknesses or it breaks — that's what our
  `manufacturability.py` checks.

That's genuinely enough to build the tool. Everything else the code handles as numbers.

---

## PART 1 — What we are building (vision + scope)

**Vision (one sentence):** an always-on tool that studies market trends, invents new ring
designs, and outputs a sketch + 3D file + photoreal render + price for each — automatically —
so a human only picks the winners.

**The auto flow:** `Trends → AI designs → recipe → sketch → 3D → render → price → files → keep best → repeat.`

**Who uses it:** you (the operator) run batches and approve; later, retailers embed the
customizer; shoppers customize + buy.

**In scope for v1:** rings only, one recipe format ("design-DNA"), 6 common cuts, auto
sketch + 3D (STL) + render + price, a simple dashboard to run batches and review.

**Out of scope for v1:** earrings/necklaces, AR try-on, live diamond inventory feeds,
multi-tenant SaaS, payments. (All are later phases.)

---

## PART 2 — Requirements analysis

### 2.1 Functional requirements (what it must DO)

Grouped by module. Each is testable.

**Trend module**
- FR-1 Pull trend signals (shapes/settings/metals/price bands) from data sources.
- FR-2 Rank attributes by momentum; output "hot" combos.
- FR-3 Propose new **design-DNA** recipes that are hot AND not already in the catalog.

**Generator (recipe)**
- FR-4 Represent every design as a **design-DNA** JSON validated against a schema.
- FR-5 Create variations by nudging parameters (family from one seed).

**Sketch**
- FR-6 Render a 2D concept sketch (top + side) from a design-DNA.

**3D build (the critical one)**
- FR-7 Build an exact, watertight 3D model from a design-DNA (band + head + stone seats).
- FR-8 Export `.stl` (print/cast) and `.step`/`.3dm` (CAD) + a parts/BOM list.
- FR-9 Geometry is *constructed from parameters*, never AI-drawn (guarantees correctness).

**Render**
- FR-10 Produce a photoreal image (and 360° turntable) of the 3D model.
- FR-11 Support quality tiers: fast preview → 2K → up to 8K hero.

**Price + manufacturability**
- FR-12 Estimate metal weight, stone cost, labour → make cost → suggested retail.
- FR-13 Check castability (min wall, prong size, band width, ratio-vs-cut) and flag/auto-fix.

**Output + review**
- FR-14 For each design, save a bundle: DNA + sketch + STL/STEP + render + price sheet.
- FR-15 Score each design (trend-fit, cost, appeal) and rank a batch.
- FR-16 Human approve/reject; approved designs feed learning back into FR-2.

**Orchestration + UI**
- FR-17 "Auto Generate N designs" runs the whole flow unattended and returns a batch.
- FR-18 A dashboard: run batches, browse results, approve, download files.

### 2.2 Non-functional requirements (how WELL)

- **NFR-1 Cost control:** rendering (esp. 8K) is the big GPU cost → cache by config-hash;
  render preview by default, 8K only on request.
- **NFR-2 Speed:** a preview design (DNA→sketch→3D→2K render→price) in under ~2 min.
- **NFR-3 Reliability:** a bad design fails gracefully (skips, logs) without killing the batch.
- **NFR-4 Reproducibility:** same recipe → same geometry (deterministic build).
- **NFR-5 Scalability:** render/build run as queued workers you can add more of.
- **NFR-6 Auditability:** every output traces back to its exact design-DNA + params.
- **NFR-7 Usability:** the operator needs zero CAD skill — it's buttons + a gallery.

### 2.3 Data requirements
- **design-DNA schema** (done: `schema/design-dna.schema.json`).
- **Cut/ratio table** (done), **pricing constants** (done) → later swap for live data.
- **Stone models library** (per-cut 3D stones) — you'll need/generate these for FR-7.
- **Trend data** — start seeded (done), later real feeds.

---

## PART 3 — Research: where to start & what to pick

### 3.1 The key decision: make the WHOLE pipeline CODE (so an AI can build it)

Professional shops use **Rhino + Grasshopper / MatrixGold** (paid, GUI, needs a jeweler).
For a **non-jeweler building with AI**, choose a **code-based, open-source, scriptable stack** —
because an AI coding tool can write code, not click a CAD GUI.

**Recommended AI-buildable open stack**

| Job | Pick | Why |
|---|---|---|
| Parametric 3D (recipe→model) | **CadQuery** or **build123d** (Python code-CAD) | free, scriptable, an AI can write it, exports STL/STEP |
| Photoreal render | **Blender** headless via its `bpy` Python API | free, scriptable, up to 8K, real gems |
| Web 3D preview | **three.js** (glTF) | shows the model in a browser |
| Backend/orchestration | **Python + FastAPI** | pairs with the design-tool code you already have |
| DB / queue | **PostgreSQL + Redis** | catalog + job queue |
| Storage | S3-compatible + CDN | store STL/renders/bundles |
| Frontend dashboard | React + TypeScript | run batches, review gallery |

Keep Rhino/Matrix as an *optional pro path* later. Start all-code.

### 3.2 De-risk the hardest thing FIRST
The riskiest step is **FR-7 recipe→3D** (a valid, watertight, seated ring). Do a tiny
**spike** on day one: get CadQuery to build *one* round solitaire (band + 4 prongs + a stone
seat) and export an STL you can open in a free viewer. If that works, the whole plan is real.
Everything else (trends, render, UI) is comparatively normal software.

### 3.3 What to procure/learn
- **Learn:** basic Python, a weekend of CadQuery tutorials, a day of Blender-Python basics.
- **Procure later:** a diamond price feed (Nivoda/RapNet API), GPU render machines (rent
  spot GPUs), live metal spot price API.

---

## PART 4 — How to instruct an AI tool to build this

This is a skill. Follow these rules and an AI coding agent (Claude Code, etc.) will build it well.

### 4.1 Golden rules
1. **Never say "build the whole tool."** Decompose into one module / one file at a time.
2. **Give it the spec, not vibes.** Point it at `schema/design-dna.schema.json`, the relevant
   FR number, and 1–2 example inputs/outputs.
3. **Work in vertical slices:** get one design fully through the pipeline (round solitaire)
   before adding cuts/features.
4. **Demand a test / a runnable check** with every task ("include a test that builds
   examples/…json and asserts the STL is watertight").
5. **Keep a `CLAUDE.md`/spec** in the repo so the AI has standing context every session.
6. **Review + iterate:** run what it makes, paste errors back, ask for the fix. Small loops.
7. **One source of truth:** the design-DNA schema is the contract every module reads/writes.

### 4.2 Copy-paste task prompts (per module)

> **3D spike (do first):**
> "Using **CadQuery** in Python, write `cad/build_ring.py` that reads a design-DNA JSON
> (schema in `schema/design-dna.schema.json`) and builds a **round solitaire only**: a plain
> band of `band.width_mm`, a head with `centre.prongs` prongs, and a cylindrical seat for the
> stone sized from `centre.carat`. Export `<sku>.stl`. Add a test that builds
> `examples/lr-0202-meridian.json` and asserts the mesh is watertight. Ignore all other cuts
> for now."

> **Add cuts:** "Extend `build_ring.py` to support `oval` and `hexagon` centre cuts by
> swapping the seat/stone profile. Keep round working. Add each to the test."

> **Render:** "Write `render/render_blender.py` run headless by Blender's `bpy`: import an
> STL, apply a gold PBR material + an HDRI, place a camera, and save a 2K PNG. Add a
> `--res` flag supporting 2000 and 8000. Cache output by a hash of (stl, material, camera)."

> **Price:** already built — `cad/manufacturability.py`. Tell the AI "reuse it as the pricing service."

> **Trend real data:** "Implement `trend/aggregate()` to pull the newest N listings from
> <one source> and return `[{attributes, engagement, ts}]`. Just that one adapter, with a
> saved sample fixture for tests."

> **Orchestrator:** "Write `run_batch.py` that: calls trend.propose(n) → for each DNA:
> sketch, build_ring, render(2K), price, bundle into `out/<sku>/`. Log failures and continue.
> Return a JSON manifest of the batch."

> **Dashboard:** "React page: a 'Generate N' button hits `POST /batch`, then shows a gallery
> of result cards (render, name, price, trend score) with Approve/Reject and a Download-files
> button."

### 4.3 Anti-patterns to refuse
- Asking AI to *draw* the final 3D/geometry (it drifts — build it parametrically).
- One giant prompt for everything (you'll get a mess you can't debug).
- No tests (you won't know when it broke).

---

## PART 5 — Start-to-end build order (milestones + "done" tests)

| M | Milestone | Deliverable | Done when… |
|---|---|---|---|
| 0 | Setup | repo, Python env, `CLAUDE.md`, schema (mostly done) | `manufacturability.py` runs on examples |
| 1 | Recipe + price | design-DNA + pricing/mfg (**done**) | 4 examples price + PASS |
| 2 | **3D spike** | `build_ring.py` round solitaire → STL | STL opens + is watertight |
| 3 | More cuts + export | oval/hexagon/marquise/pear; STEP export + BOM | each example builds valid STL/STEP |
| 4 | Render | Blender headless → 2K + 8K, cached | a design renders to PNG + 360 |
| 5 | Sketch | 2D sketch from DNA (extend configurator SVG logic) | sketch saved per design |
| 6 | Trend real data | one live adapter + ranking + propose | proposals come from real listings |
| 7 | Orchestrator | `run_batch.py` end-to-end bundles | "Generate 10" → 10 folders of files |
| 8 | Dashboard | web UI: run, review, approve, download | operator runs a batch with zero CLI |
| 9 | Learn loop + polish | approvals raise trend weights; cost caps | approved styles bias next batch |
| 10 | (later) SaaS/AR/feeds | multi-tenant, embed widget, AR, live pricing | per the configurator blueprint |

**Golden path to a demo:** M2 + M4 + M7 = press a button, get real 3D files + renders + prices
for a batch of AI-invented rings. That's the whole pitch, and it's a few focused weeks.

---

## PART 6 — Team, budget, timeline, risk

- **Solo + AI:** feasible to a strong demo (M0–M7) if you can run Python and iterate with an
  AI agent. Budget mostly your time + modest GPU render bills.
- **Small team (faster):** 1 backend/CAD-scripting dev, 1 full-stack, 0.5 3D/graphics.
- **Cost drivers:** GPU render minutes (cache hard), later data feeds + CAD licenses if you
  add the Rhino pro path.
- **Top risks:** (1) recipe→3D quality — *de-risk with the M2 spike first*; (2) render cost —
  *tiers + caching*; (3) trend data access — *start seeded, add feeds later*.

---

## PART 7 — Your first week (concrete)

1. **Day 1:** install Python + CadQuery; run our `manufacturability.py` on the examples.
2. **Day 2–3:** the **M2 spike** — AI builds `build_ring.py` for a round solitaire → open the
   STL in a free viewer (e.g. the online 3D Viewer). *This proves the whole idea.*
3. **Day 4:** add oval + hexagon cuts.
4. **Day 5:** Blender headless render of one STL to a 2K PNG.
5. **Day 6:** `run_batch.py` chaining propose → build → render → price → folder.
6. **Day 7:** wrap a tiny web page with a "Generate 5" button and a results gallery.

At the end of week one you have a working, if rough, **auto-designer**. Then iterate outward
using Part 5.

---
*Everything references the existing scaffold in `design-tool/`. The design-DNA schema is the
contract that ties every module together — start there, keep it central.*
