# 20 — MASTER IMAGE PROMPT LIBRARY (10 ETSY SLOTS + 1 VIDEO)

> **AUTHORITATIVE OWNER (see `00` POLICY INDEX):** Etsy slot map + per-slot prompt text + theme rotation → this doc.
> This doc owns **WHAT to ask for per slot**. It never overrides the locked owners: geometry `13`/`16` · cloth `11` · logo `04` · camera uniqueness `12` · realism/metal/diamond/lifestyle `03` · pipeline `15` §0 (Higgsfield only) · consistency gate `18`.

Every prompt below is a *scene* prompt only. The ring is supplied as source reference at max weight; AI may change **only** camera, composition, cloth folds, background, lighting, reflections, shadows, depth of field. Zero geometry invention (`16`).

---

## 1. SLOT MAP — 10 IMAGES + 1 VIDEO (fixed order)

Etsy shows slot 1 as the thumbnail and the video last. Each slot is a **reserved camera orientation** — used exactly once per catalog (`12` ONE IMAGE PER ANGLE, ≤20% similarity bar).

| # | Slot | Type | Reserved camera | Purpose |
|---|---|---|---|---|
| 1 | Hero Front | Studio | 0° yaw, ring height, 0–5° tilt | Thumbnail; instant recognition |
| 2 | Front 45° Left | Studio | ~45° yaw L, 30–35° pitch | Setting depth, side stones |
| 3 | Front 45° Right | Studio | ~45° yaw R, 30–35° pitch | Opposite side, band profile |
| 4 | True Profile | Studio | 90° yaw (or 75–80° per rotation), ring height | Basket, gallery, cathedral, setting height |
| 5 | High Three-Quarter | Studio | ~30° yaw, ~60° pitch (never 90° overhead) | Complete architecture |
| 6 | Rear / Gallery | Studio | 135–180° yaw, 20–30° pitch | Under-gallery, finish quality |
| 7 | Diamond Macro | Detail | Raked oblique macro, light skimming facets | Brilliance, clarity, cut proof |
| 8 | Craft Macro | Detail | Low near-table ~10–15°, tight on shoulder→head | Prong work, metal finish, scale |
| 9 | On-Finger Hero | Lifestyle | Ring-level close, hand as stand | Fit and real-world scale |
| 10 | Lifestyle Story | Lifestyle | Theme-dependent (see §3) | Emotional/context sale |
| V | Video | 8–10 s | Slow orbit or focus pull | Motion proof of brilliance |

Slots 1–8 use the locked studio setup (white cloth + printed logo, `11`/`04`). Slots 9–10 are the only frames where the cloth/logo may be absent.

---

## 2. PROMPT BLOCKS

### 2.0 SHARED PREAMBLE (prepend to every slot 1–8)
```
Professional luxury jewelry product photograph of the EXACT ring in the reference
images. Ring geometry, proportions, stone count, prong count and metal colour are
100% identical to the reference — do not redesign, smooth, simplify or reinterpret
any element. Studio scene: premium pure-white cotton cloth, naturally draped, the
brand logo printed into the weave and following every fold. Bright neutral-white
daylight, correct white balance, no warm or colour cast. Real macro photography —
genuine shallow depth of field with soft falloff, believable specular highlights,
natural cloth folds caused by gravity. Ring centered horizontally and vertically,
framed large, whole ring visible, nothing cropped. Not CGI, not a render, not a
CAD screenshot.
```

### 2.1 Slot 1 — Hero Front
```
Camera straight on at ring height, 0° yaw, 0–5° downward tilt. The full face of
the setting and the centre stone face the lens with maximum brilliance. Cleanest,
most symmetrical e-commerce hero composition.
```

### 2.2 Slot 2 — Front 45° Left
```
Camera yawed 45° to the LEFT of front and raised to 30–35° above ring height.
The setting is clearly seen from the left-front and above: centre-stone depth,
side stones, gallery and band all readable. Clearly a different viewpoint from
the hero.
```

### 2.3 Slot 3 — Front 45° Right
```
Mirror of the previous frame: camera yawed 45° to the RIGHT, raised 30–35°.
Shows the opposite side of the setting and the band profile from that side.
```

### 2.4 Slot 4 — True Profile
```
True side view at ring height. Basket, gallery, prongs, under-gallery, cathedral
and side-stone setting in clean profile. The top of the centre stone is NOT
visible as a face. The customer should understand exactly how the ring is built.
```

### 2.5 Slot 5 — High Three-Quarter
```
Camera high at roughly 60° above the table, yawed about 30°. Top and one side
seen together, revealing the complete architecture. Never a 90° overhead flat-lay:
the crown, prongs and band depth must stay visible with natural lens perspective.
```

### 2.6 Slot 6 — Rear / Gallery
```
Camera behind the head looking forward, 135–180° yaw, 20–30° above ring height.
Shows the rear of the setting and the under-gallery finish — the craftsmanship a
buyer normally never sees. Ring still centered and fully in frame.
```

### 2.7 Slot 7 — Diamond Macro
```
Raked oblique macro, light skimming across the facets. Fill the frame with the
centre stone and its immediate setting while keeping prongs whole and uncropped.
Show real fire and scintillation — sharp facet edges, crisp reflections, a true
focal plane on the table facet with soft falloff behind.
```

### 2.8 Slot 8 — Craft Macro
```
Low near-table angle, 10–15° above the cloth, tight on the shoulder-to-head
transition. The stone towers over the band. Show prong tips, metal polish,
milgrain or detailing, and the real thickness of the shank. Extreme close focus,
background dissolving into soft white.
```

### 2.9 Slot 9 — On-Finger Hero
```
The exact ring from the reference worn on a well-groomed hand, natural skin,
short neutral nails. Camera at ring level, close in — the ring is the subject and
the hand is only a stand, NOT portrait-style hand photography. Ring occupies the
centre of the frame, geometry identical to the reference, soft natural window
light, background softly blurred.
```

### 2.10 Slot 10 — Lifestyle Story
Scene per the catalog's rotated theme (§3). Constant clause:
```
The exact ring from the reference, worn or resting, in the scene above. Ring
centered, framed large, the clear focal point — the eye must land on it within
one second. Environment softly blurred and never sharper than the ring. Natural
light, real photography, no props competing with the jewelry.
```

### 2.11 Slot V — Video (8–10 s, 24–30 fps)
Pick ONE per catalog, rotating between SKUs:
- **Slow orbit** — camera arcs 0°→60° around the ring on the studio cloth, constant height, constant light; brilliance shifts naturally as facets catch the light.
- **Focus pull** — static camera, focus travels from the shank to the centre stone; shallow DoF throughout.
- **Light sweep** — ring static, a soft key light travels across the stone, igniting fire facet by facet.
- **Hand reveal** — hand enters frame and settles; ring holds the centre for the final 4 s.
No cuts, no text overlays, no zoom punches. Geometry stays locked across every frame.

---

## 3. THEME ROTATION — THE ANTI-"AI LOOK" RULE

Repeating the same 11 setups across every SKU is what makes a shop read as AI-generated. **Each new catalog draws a different theme** for slots 9–10 (and a different video style), and rotates *specific* camera geometry within slots 1–8 per `12` §A1.

**Theme pool (rotate, never two consecutive SKUs on the same theme):**

| Theme | Slot 9 setting | Slot 10 scene |
|---|---|---|
| A · Morning Light | Hand by a bright window | Hand around a coffee mug on a linen table |
| B · Marble & Gold | Hand resting on pale marble | Ring beside a stem of dried florals on marble |
| C · Reading Nook | Hand on an open book | Hand turning a page, warm lamp bokeh |
| D · Desk & Work | Hand resting near a laptop edge | Hand on a notebook with a pen, clean office light |
| E · Evening Occasion | Hand at the neckline of a silk blouse | Hand on a dark velvet surface, single soft key |
| F · Garden Daylight | Hand holding a single flower | Hand on a stone ledge, foliage far out of focus |
| G · Gift Moment | Hand lifting the ring from a box | Ring box open on cloth, hand just leaving frame |

**Rotation record:** log the theme + the video style + the specific camera geometry variants used, in that SKU's `config/deliveries/LR-XXXX.json`. Before starting a new catalog, read the previous two records and pick a theme neither used.

**Within slots 1–8, rotate the *flavour* per `12` §A1** — e.g. this SKU's profile at a 10–15° yaw instead of dead-flat 90°, next SKU's high three-quarter from the opposite corner, a gentle handheld tilt on one frame. The slot's *role* is fixed; its exact camera is not.

---

## 4. PRE-DELIVERY CHECKLIST (per catalog)

- [ ] All 10 slots present, in order, each a distinct reserved orientation (`12`, ≤20% similarity)
- [ ] Geometry identical to source on every frame (`13`, `16`) — fall through the `12` §A3 ladder if not
- [ ] Same cloth, same logo treatment, same white balance across slots 1–8 (`11`, `04`)
- [ ] Slots 9–10 use this catalog's rotated theme, unused by the previous two SKUs
- [ ] Video style differs from the previous SKU's
- [ ] Ring is the instant focal point in all 11 assets (`12` §A2)
- [ ] Theme + camera variants written to `config/deliveries/LR-XXXX.json`
