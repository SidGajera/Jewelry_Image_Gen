# Blueprint — Web 3D Jewelry Configurator + Rendering Platform
### (feature-parity with i3djewel / iJewel3D class products)

**Goal:** a B2B SaaS where jewelers import CAD, get photoreal renders, and publish an
**embeddable 3D configurator** that shoppers customize (metal / gems / engraving) with
**live pricing + AR try-on**, exportable to **CNC/CAD** for manufacture.

**IP line:** match the *capabilities* below; write your own code, brand, UI and asset
library. Do not copy their code, name/logo, copyrighted 3D models, or patents.

**Your unfair advantage (don't skip):** i3djewel starts from a CAD file someone already
modeled. You already have the two layers upstream of that — a **trend engine** and a
**parametric design-DNA generator** (`design-tool/`). Bolt this configurator on top and you
sell *"designs the market wants, auto-generated, then configurable and shoppable"* — a
category above a pure renderer.

---

## 1. Feature inventory (what to match)

**A. 3D Studio (creator side — the jeweler)**
- CAD import: `.3dm .stl .obj .gltf/.glb .step` → auto-center, auto-scale, unit detect.
- Material authoring: PBR metals (18k/14k YG·WG·RG, platinum, silver, two-tone), gemstones
  with dispersion/refraction/IOR, enamel, pearl. Named material presets.
- Studio: HDRI environment lighting, camera rig (turntable, hero angles), depth of field.
- Auto-assign: detect metal vs stone parts (by mesh name/material) → apply libraries.

**B. Rendering**
- Real-time WebGL PBR preview (interactive).
- High-quality offline render → HD stills, 360° turntable **video**, transparent PNGs.
- Batch/queue rendering; watermark for trials.

**C. Configurator (shopper side — embeddable widget)**
- Real-time 3D: rotate / zoom / 360°.
- Options: metal, center-stone shape+carat+quality, accent stones, band width, engraving text.
- **Live price** updates per selection; ring-size selector.
- **AR virtual try-on** (WebXR / camera hand-tracking).
- Save / share design (link), add-to-cart / request-quote, lead capture.

**D. Commerce / catalog**
- Diamond & gemstone inventory (manual + feed import: RapNet/IDEX/Nivoda).
- Pricing engine: metal spot × weight + stone price + labour + margin rules.
- Product catalog, collections, variants.

**E. Manufacturing**
- Export selected config → `.3dm` / `.stl` for CNC/casting; BOM + weight + cost sheet.

**F. Platform / admin (retailer tools)**
- White-label: retailer branding, embed snippet (`<iframe>`/web component).
- Multi-tenant accounts, roles; catalog/material/pricing management.
- Analytics: views, configure-throughs, AR opens, quotes, conversion.
- Integrations: Shopify/WooCommerce, payment, CRM/email, inventory feeds.

---

## 2. Architecture

```
 Jeweler ──▶ CREATOR STUDIO (web)                 Shopper ──▶ CONFIGURATOR WIDGET (embed)
      │        three.js/babylon PBR                     │        three.js viewer + options UI
      ▼                                                 ▼
 ┌───────────────────────── API (REST/GraphQL) ─────────────────────────┐
 │  auth·tenants │ catalog │ materials │ pricing │ configs │ orders/leads │
 └───────┬───────────────┬───────────────┬───────────────┬──────────────┘
   Postgres          Object store       Render workers        Feeds
   (metadata)        (glTF/CAD/HDRI/     (GPU: Blender Cycles  (RapNet/Nivoda
                      renders, CDN)       / path tracer, queue) diamond prices)
```

- **Asset pipeline:** CAD (`.3dm/.step`) → tessellate/optimize → **glTF/GLB (Draco)** for web;
  keep original NURBS for manufacturing export. (Tools: `rhino3dm`, `assimp`, `gltfpack`.)
- **Real-time** in browser = glTF + PBR; **hero photoreal** = offline GPU render workers.

---

## 3. Tech stack (recommended)

| Layer | Pick | Why |
|---|---|---|
| Web 3D | **three.js** (or Babylon.js) + `KHR_materials_transmission` | mature PBR incl. gem transmission/refraction |
| Frontend | React + TypeScript; the widget as a **Web Component** | embeddable anywhere, framework-agnostic |
| AR | **WebXR** + fallback to model-viewer / 8thWall for hand try-on | no app install |
| Backend | Node/NestJS **or** Python/FastAPI | either; FastAPI pairs with your Python design-tool |
| DB | **PostgreSQL** (+ Redis queue) | relational catalog + pricing |
| Object store/CDN | S3-compatible + CloudFront/Cloudflare | serve glTF/renders fast |
| CAD I/O | **rhino3dm**, OpenCASCADE (`.step`), assimp | import + manufacturing export |
| Offline render | **Blender (Cycles) headless** on GPU workers, or a path-tracer (LuxCore) | photoreal stills/video, scriptable, no per-seat license |
| Pricing feeds | RapNet / Nivoda / IDEX APIs | live diamond inventory + price |

---

## 4. Module breakdown & rough effort

| # | Module | Key work | Effort |
|---|---|---|---|
| 1 | CAD import + web optimizer | 3dm/step→glTF, Draco, auto scale/center, part tagging | M |
| 2 | PBR material system | metal/gem shaders, dispersion, presets, auto-assign | M–L |
| 3 | Real-time viewer | three.js scene, HDRI, camera, turntable | M |
| 4 | Offline render service | GPU workers, queue, stills+360 video, watermark | L |
| 5 | Configurator widget | options UI, live geometry/material swap, share | M |
| 6 | Pricing engine | metal-weight calc, stone pricing, rules, quote | M |
| 7 | Diamond inventory | feed import + search/filter, manual entry | M |
| 8 | AR try-on | WebXR/hand-track, ring placement | M–L |
| 9 | Manufacturing export | config→3dm/stl, BOM, cost sheet | M |
| 10 | Admin / multi-tenant | accounts, catalog, branding, embed snippet | L |
| 11 | Analytics + integrations | events, Shopify/CRM, payments | M |

*Effort: S≈days, M≈2–4 wk, L≈1–3 mo for a small senior team.*

---

## 5. The photorealism pipeline (the make-or-break)

Two tracks, don't conflate:
- **Real-time (in browser):** glTF + three.js PBR. Gems use `transmission` + `ior≈2.4` +
  `dispersion` (Chrome supports it) + an HDRI. "Good enough to shop," 60fps.
- **Hero photoreal (offline):** render workers running **Blender Cycles** headless — real
  caustics/dispersion, studio HDRI, DoF → the marketing stills + 360 video. Queue + cache
  by (model, materials, camera) hash so identical configs don't re-render.

Gems are the hard part in real-time: fake it with transmission + a cubemap + a subtle
internal-reflection matcap; go to Cycles when the customer wants the "wow" render.

---

## 6. Data model (core tables)

```
tenant(id, brand, theme, embed_key)
product(id, tenant_id, name, base_model_asset, collection)
asset(id, kind[cad|gltf|hdri|render], url, meta)          -- object store
material(id, tenant_id, kind[metal|gem], name, pbr_params, price_ref)
option_group(id, product_id, type[metal|center|accent|band|engraving], ...)
option(id, option_group_id, label, material_id|stone_spec, price_delta, geometry_ref)
stone(id, tenant_id, cut, carat, color, clarity, price, feed_id)   -- inventory
config(id, product_id, selections_json, price, share_slug, ar_opens)  -- a saved shopper design
lead_order(id, config_id, contact, status)
```
Note: a saved `config.selections_json` is essentially the **design-DNA** from your
`design-tool/schema` — the same contract flows through render, price, and CAD export.

---

## 7. Hard parts → how to solve

- **Real-time gem realism** → transmission+dispersion PBR + HDRI; escalate to Cycles for hero.
- **CAD import robustness** (messy .3dm/.step) → normalize via rhino3dm/OpenCASCADE; require
  a naming convention for metal/stone parts, or a tag-parts step in the studio.
- **Live pricing accuracy** → pull metal spot daily + diamond feed; compute metal weight from
  mesh volume × density; margin rules per tenant. (You already have this heuristic in
  `cad/manufacturability.py` — productionize it.)
- **Embed performance** → ship the widget as a lazy-loaded Web Component; Draco-compress glTF;
  CDN + config-hash render cache.
- **AR** → WebXR where supported; hosted hand-tracking fallback; keep it optional.

---

## 8. Phased roadmap

- **MVP (8–12 wk):** CAD→glTF import, real-time viewer, metal+center-stone options, live
  price, save/share, one embeddable widget. (Skip AR, offline render farm, feeds.)
- **v1 (+8–12 wk):** offline photoreal render service (stills+360), diamond feed import,
  multi-tenant admin + branding + embed, Shopify integration.
- **v2:** AR try-on, manufacturing export + BOM, analytics, more categories, payments.

## 9. Team / timeline / cost (indicative)
- Team: 1 senior 3D/graphics eng, 1 full-stack, 1 backend, 0.5 design, 0.5 PM.
- MVP ~3 months; v1 ~6 months; v2 ~9–12 months.
- Infra: GPU render workers are the main variable cost — use spot GPUs + aggressive caching.

## 10. Build vs. buy
- **Buy/OSS:** three.js, Blender, rhino3dm, model-viewer, Draco — don't rebuild these.
- **Build:** your material/pricing/config data model, the widget, the trend+parametric layers.
- **Consider buying** a diamond-feed aggregator (Nivoda API) rather than integrating each.

## 11. Where you beat i3djewel
They render *existing* designs. You already generate the *designs* (trend engine →
design-DNA → parametric CAD). Sequence it: **trend → auto-designed collection → auto-CAD →
this configurator → shoppable + priced + manufacturable.** That's the moat: they sell a
viewer; you sell a design-to-storefront pipeline.

---

## 12. Parity checklist — i3djewel's highlighted features → our modules

| # | Their highlighted feature | Covered by | Type |
|---|---|---|---|
| 1 | Jewelry CAD Design | Parametric generator + Rhino/Grasshopper build (§CAD) — **auto** in our tool | software |
| 2 | Photorealistic 3D Rendering (up to **8K**) | Offline render service (Blender Cycles), 8K tier | software |
| 3 | Custom Ring Design | Configurator widget + design-DNA edits | software |
| 4 | Diamond Jewelry Design | Stone library + diamond feed + gem PBR | software |
| 5 | Jewelry Visualization | Real-time viewer + renders + 360° video | software |
| 6 | Product Rendering | Batch render queue (stills + video) | software |
| 7 | Manufacturing-Ready Designs | CAD export `.3dm/.stl` + BOM + manufacturability checks | software |
| 8 | Customization Support | Configurator options + save/share | software |
| 9 | Professional Design Service | Our **auto-generate** turns this into software; human-assist optional | service→auto |
| 10 | Online Jewelry Business Growth | Embed widget + Shopify + AR + analytics (conversion) | software+GTM |
| 11 | Website & Phone Support | Support desk / onboarding | **service (ops)** |
| 12 | Multiple Jewelry Design Options | Auto-mode **batch generation** — our strength | software |
| 13 | Up to 8K jewelry quality | Render pipeline max tier (see note) | software |

**8K render note:** 8K (7680×4320) stills are heavy — minutes of GPU per frame with real
caustics/dispersion. Offer it as a **top render tier** (real-time preview → 2K quick → 8K
hero on request), and **cache by config-hash** so an 8K is rendered once and reused.

**Read of their business:** i3djewel is a **software + done-for-you service** (they'll CAD +
render for you, with phone support). Items 9 and 11 are *services*, not code. Your wedge:
automate item 9 (auto-generate designs) so you're not selling human hours — you're selling a
machine that produces #1–8 and #12 at scale, then layer light human support (#11) on top.

---
*Sources: i3djewel.com · docs.ijewel3d.com · Rhino iJewel plugin announcement (Aug 2024).*
