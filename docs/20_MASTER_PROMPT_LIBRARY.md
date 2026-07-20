# 20 — MASTER IMAGE PROMPT LIBRARY (10 ETSY SLOTS + 1 VIDEO)

> **AUTHORITATIVE OWNER (see `00` POLICY INDEX):** Etsy slot map + per-slot prompt text + theme rotation → this doc.
> This doc owns **WHAT to ask for per slot**. It never overrides the locked owners: geometry `13`/`16` · cloth `11` · logo `04` · camera uniqueness `12` · realism/metal/diamond/lifestyle `03` · pipeline `15` §0 (Higgsfield only) · consistency gate `18`.

---

## 0. HOW TO USE THIS

Every prompt is built in 4 parts:

```
[GLOBAL_PRESERVATION_BLOCK] + [SLOT_PROMPT] + [THEME_VARIANT] + [QUALITY_TAIL]
```

* **GLOBAL_PRESERVATION_BLOCK** (§1) — never changes. Locks CAD accuracy.
* **SLOT_PROMPT** (§2) — defines the camera angle / shot purpose. Never changes per slot.
* **THEME_VARIANT** (§4) — rotates per listing using the pools in §4. This is what kills the "AI-generated" feeling.
* **QUALITY_TAIL** (§5) — never changes. Camera/render realism.

**Rotation rule:** `theme_index = hash(SKU) % pool_size`. Same SKU always gets the same theme (consistent listing), different SKUs get different themes (varied shop grid). Write the resolved theme into that SKU's `config/deliveries/LR-XXXX.json` so re-runs reproduce it exactly.

The ring is supplied as source reference at max weight. AI may change **only** camera, composition, cloth folds, background, lighting, reflections, shadows and depth of field. Zero geometry invention (`16`).

---

## 1. GLOBAL_PRESERVATION_BLOCK (never changes)

> **No new policy here.** This is the prompt-ready wording of the existing locks — `03` §A SOURCE CAD (only camera may change) + §B JEWELRY PRESERVATION reject list, owners `13` / `16`, failures `07` F3/F4. If the owners change, re-render this block; never edit it to say something the owners don't.

Prepend to EVERY prompt. Non-negotiable.

```
Photograph of the exact ring shown in the reference CAD image. Reproduce the
geometry with absolute fidelity: identical band width, band thickness, ring
profile and silhouette, identical head, gallery, basket, cathedral and bridge
structure, identical setting type, identical prong count, prong shape, prong
thickness and prong position, identical centre stone cut, size, proportions,
table, crown and pavilion, identical side stone and pavé count, size, spacing
and placement, identical metal thickness, curvature and finish. Do not redesign,
restyle, stylise, simplify, embellish or reinterpret any element. Only the
camera angle, lighting and surrounding environment may change.
```

## 2. SLOT_PROMPT — 10 IMAGES + 1 VIDEO (fixed order)

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
| 10 | Lifestyle Story | Lifestyle | Theme-dependent (§4) | Emotional/context sale |
| V | Video | 8–10 s | Slow orbit or focus pull | Motion proof of brilliance |

Slots 1–8 use the locked studio setup (white cloth + printed logo, `11`/`04`). Slots 9–10 are the only frames where the cloth/logo may be absent.

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
The ring worn on a well-groomed hand, natural skin, short neutral nails. Camera
at ring level, close in — the ring is the subject and the hand is only a stand,
NOT portrait-style hand photography. Ring occupies the centre of the frame, soft
natural light, background softly blurred.
```

### 2.10 Slot 10 — Lifestyle Story
```
The ring worn or resting in the scene defined by the theme variant. Ring centered,
framed large, the clear focal point — the eye must land on it within one second.
Environment softly blurred and never sharper than the ring. No prop competes with
the jewelry.
```

### 2.11 Slot V — Video (8–10 s, 24–30 fps)
One style per SKU, selected by the same hash rule (`video_index = hash(SKU) % 4`):
- **Slow orbit** — camera arcs 0°→60° around the ring on the studio cloth, constant height, constant light; brilliance shifts naturally as facets catch the light.
- **Focus pull** — static camera, focus travels from the shank to the centre stone; shallow DoF throughout.
- **Light sweep** — ring static, a soft key light travels across the stone, igniting fire facet by facet.
- **Hand reveal** — hand enters frame and settles; ring holds the centre for the final 4 s.

No cuts, no text overlays, no zoom punches. Geometry stays locked across every frame.

---

## 3. STUDIO SCENE CONSTANT (slots 1–8)

Appended to slots 1–8 in place of a lifestyle theme variant — the studio setup is locked, not rotated (`11`, `04`):

```
Premium pure-white cotton cloth, naturally draped, folds falling where gravity
would really put them. The brand logo printed into the weave, following every fold
and the perspective of the surface — never a floating overlay. Bright neutral-white
daylight, correct white balance, no warm or colour cast.
```

Within these slots only the *flavour* of the camera rotates per `12` §A1 — e.g. this SKU's profile at 10–15° yaw instead of dead-flat 90°, next SKU's high three-quarter from the opposite corner. The slot's role is fixed; its exact camera is not.

---

## 4. THEME_VARIANT — THE ANTI-"AI LOOK" POOL (slots 9–10)

Repeating the same setups across every SKU is what makes a shop read as AI-generated. Resolve with `theme_index = hash(SKU) % 7`.

| idx | Theme | Slot 9 setting | Slot 10 scene |
|---|---|---|---|
| 0 | Morning Light | Hand by a bright window | Hand around a coffee mug on a linen table |
| 1 | Marble & Gold | Hand resting on pale marble | Ring beside a stem of dried florals on marble |
| 2 | Reading Nook | Hand on an open book | Hand turning a page, warm lamp bokeh |
| 3 | Desk & Work | Hand resting near a laptop edge | Hand on a notebook with a pen, clean office light |
| 4 | Evening Occasion | Hand at the neckline of a silk blouse | Hand on a dark velvet surface, single soft key |
| 5 | Garden Daylight | Hand holding a single flower | Hand on a stone ledge, foliage far out of focus |
| 6 | Gift Moment | Hand lifting the ring from a box | Ring box open on cloth, hand just leaving frame |

---

## 5. QUALITY_TAIL (never changes)

```
Real macro photography shot on a professional camera — genuine shallow depth of
field with soft gradual falloff, a true focal plane, believable specular
highlights, natural shadow gradients and gentle light falloff toward the frame
edges. Ring centered horizontally and vertically, framed large, whole ring
visible, nothing important cropped. Photorealistic, not CGI, not a 3D render, not
a CAD screenshot; no waxy over-smooth surfaces, no unnaturally even lighting, no
everything-in-focus flatness.
```

---

## 6. PRE-DELIVERY CHECKLIST (per catalog)

- [ ] All 10 slots present, in order, each a distinct reserved orientation (`12`, ≤20% similarity)
- [ ] Every prompt assembled as PRESERVATION + SLOT + THEME/STUDIO + QUALITY_TAIL
- [ ] Geometry identical to source on every frame (`13`, `16`) — fall through the `12` §A3 ladder if not
- [ ] Same cloth, same logo treatment, same white balance across slots 1–8 (`11`, `04`)
- [ ] Theme and video style resolved by `hash(SKU)`, not chosen ad hoc
- [ ] Ring is the instant focal point in all 11 assets (`12` §A2)
- [ ] Resolved theme index + video index + camera variants written to `config/deliveries/LR-XXXX.json`
