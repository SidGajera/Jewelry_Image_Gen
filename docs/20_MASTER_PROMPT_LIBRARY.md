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


## 2. SLOT_PROMPT — THE 10 SLOTS + 1 VIDEO (user-supplied, 2026-07-20)

Etsy shows slot 1 as the thumbnail and the video last. Each slot is a **reserved viewpoint/purpose** — used exactly once per listing (`12` ONE IMAGE PER ANGLE, ≤20% similarity bar).

| # | Slot | Type | Notes |
|---|---|---|---|
| 1 | ⭐ White Hero | Product | THUMBNAIL — most important image in the business |
| 2 | Side Profile | Product | Full silhouette, stone height, gallery, band taper |
| 3 | Top-Down Face-Up | Product | Face-up appearance at 70–75° (see §2.3) |
| 4 | ⭐ Hand Try-On | Lifestyle | HIGHEST CONVERTING image |
| 5 | Lifestyle / Proposal Scene | Lifestyle | Where theme rotation matters most |
| 6 | IGI Certificate Flat-Lay | Documentary | Real scanned cert only — never AI-generated |
| 7 | Carat Size Reference | Template | Build once per cut shape (8 total) |
| 8 | Sparkle Macro | Detail | Dramatic gemmological macro |
| 9 | Metal Variations | Template | Build once per design; skipped for single-metal listings (§2.9) |
| 10 | Packaging & Brand | Template | Build once, reuse everywhere |
| V | Video | 5–15 s | 360° turntable — **ask before generating** |

### 2.1 ⭐ Slot 1 — White Hero (THUMBNAIL)
```
Three-quarter angle hero shot of the ring standing upright, tilted 30 degrees
toward camera so the centre stone catches light and the band profile stays
visible. Ring fills 80 to 85 percent of the square frame, perfectly centred.
Background: locked white cotton cloth + printed logo (§3). Lighting: [POOL B],
neutral variants only.
Clean soft contact shadow directly beneath the ring. No props, no text,
no distractions. Absolute clarity on the centre stone facets and prongs.
```
*Rotation note: bright and clean is what buyers scanning search results respond to — the locked white cloth already delivers that, so the hero never takes a dark or textured surface. Save the dramatic B5 for slot 8. (Your original note reserved A1/A2/A4 for the hero; superseded by the §4.0 scoping decision, which keeps product slots on cloth.)*

### 2.2 Slot 2 — Side Profile
```
Perfect 90 degree side elevation of the ring, standing upright, camera at
exact band height. Full silhouette visible: stone height above the finger
line, cathedral or basket rise, gallery detail, band taper from shoulder to
shank. Background: locked white cotton cloth + printed logo (§3).
Lighting: [POOL B], neutral variants only.
Emphasise the profile outline crisply against the background.
```
*Physics check (`12` §B): an upright pose needs a believable support — a cloth fold, riser or contact point. Never a floating ring.*

### 2.3 Slot 3 — Top-Down Face-Up
```
Near-overhead view at 70 to 75 degrees, stone facing camera. Shows full
face-up appearance: table, crown facets, halo or pavé arrangement, prong
placement and symmetry, shoulder stone layout.
Background: locked white cotton cloth + printed logo (§3). Lighting: [POOL B],
neutral variants only.
Even illumination across the entire stone table, no blown-out highlights.
```
*Resolved 2026-07-20: 70–75°, not 90° orthographic. `12` CAMERA VALIDATION stands unamended. Orthographic + 90° is literally how a CAD viewport renders — flat stone, band as a perfect circle, no lens perspective, no crown depth: the exact render look this library exists to eliminate, already recorded as the LR-0157 failure. At 70–75° the slot still delivers table, crown facets, halo/pavé layout and prong symmetry, plus the perspective convergence that makes it read as a photograph.*

### 2.4 ⭐ Slot 4 — Hand Try-On (HIGHEST CONVERTING)
```
The ring worn on the ring finger of a natural adult female hand, hand relaxed
in a soft elegant pose, fingers slightly separated, viewed from a natural
three-quarter angle. Realistic skin texture with visible pores and natural
tone variation, short neutral manicure, no jewellery on other fingers.
The ring must sit at true scale for its stated carat weight — do not enlarge
or shrink the ring relative to the finger.
Background: soft neutral bokeh, [POOL A] tones. Lighting: [POOL B].
```
*Skin tone rotation (important for the US market): cycle `fair` → `light olive` → `medium tan` → `deep brown` across the catalogue — varied models make the shop feel photographed, not generated.*

**⚠ Manual check on every single one:** five fingers · correct joints · no fused or extra digits · natural nail beds · believable ring scale. Reject and regenerate on any failure. (Matches the `07` LR-0141 lifestyle failure: worn shots multiplied prongs and drifted stone size — count prongs here too.)

### 2.5 Slot 5 — Lifestyle / Proposal Scene
```
Editorial lifestyle still life. The ring positioned as the clear hero subject
in the left or right third of the frame, styled with [POOL C].
Surface: [POOL A]. Lighting: [POOL B]. Palette: [POOL D].
Shallow depth of field, f/2.8, background softly out of focus, ring tack sharp.
Aspirational bridal editorial mood, warm and emotional, not clinical.
```
*This is the slot where theme rotation matters most — it is the most visually distinctive image, so repetition here is what makes a shop feel AI-generated. **Never repeat a Pool C prop within 10 consecutive listings.***

*Resolved 2026-07-20: thirds permitted here. `12` §A2 now carries a narrow carve-out for this slot only — centred stays mandatory on all ten other frames. Rationale: this is the one frame whose job is emotional and editorial, and centring it forces symmetrical prop staging, which is itself an AI tell. The ring is still the instant focal point, framed large, background never sharper.*

### 2.6 Slot 6 — IGI Certificate Flat-Lay
```
Overhead flat-lay composition. The ring placed to one side, a genuine IGI
diamond grading certificate document laid flat beside it, slightly angled,
partially in frame. Surface: [POOL A]. Lighting: [POOL B] — soft and even
across the paper with no glare on the document.
Natural paper texture, realistic document flatness with a faint fold crease.
Professional, trustworthy, documentary tone.
```
> **🚫 CRITICAL — composite a REAL scanned IGI certificate.** Never let AI generate certificate text, seals or numbers: a fabricated certificate is fraud and will end the shop. Blur or crop the certificate number when reusing one scan across listings. **The generated frame must contain no certificate at all** — leave the space empty and composite the scan afterwards. Note `15` §0 is Higgsfield-only and `04`'s local-composite steps are disabled; this slot needs a compositing route confirmed before it can ship.

### 2.7 Slot 7 — Carat Size Reference (TEMPLATE — once per cut shape)
```
Clean informational comparison layout on plain white background. The same
[CUT SHAPE] diamond shown at 1.00CT, 1.50CT, 2.00CT, 3.00CT and 4.00CT, in a
single evenly spaced horizontal row, all viewed face-up from directly overhead,
scaled accurately relative to one another.
Soft even shadowless studio lighting. Generous white margin around the row.
Leave clear empty space beneath each stone for a size label to be added later.
```
*Build 8 total: Round · Oval · Marquise · Dutch Marquise · Pear · Emerald · Radiant · Asscher. Add the mm labels afterwards in code or Canva — never let the model render text.*

### 2.8 Slot 8 — Sparkle Macro
```
Extreme macro close-up of the centre stone filling 90 percent of the frame,
shot at a slight angle to catch maximum fire. Visible spectral dispersion —
rainbow flashes of red, blue and green within the facets — alongside bright
white brilliance returns. Crisp facet edges and clean facet junctions.
Background: deep charcoal or black with soft falloff.
Lighting: B5 (single focused spot with dark falloff) or B7 (backlit rim light).
Dramatic gemmological photography, high contrast, jewel-like.
```
*`03` bans "random sparkle effects, artificial starbursts or fake rainbow dispersion" — the dispersion here must be real optical behaviour of the stone's facets, never an added effect layer.*

### 2.9 Slot 9 — Metal Variations (TEMPLATE — once per design)
```
Three identical copies of the same ring shown side by side in a single evenly
spaced horizontal row, all at the same three-quarter angle and identical scale.
Left: 14K yellow gold. Centre: 14K white gold with rhodium finish.
Right: 14K rose gold.
Background: pure white seamless. Lighting: B4 (overcast diffused, even).
Accurate metal colour differentiation, identical geometry across all three.
```
*Resolved 2026-07-20: `03` amended — metal is a **per-listing parameter**, not a global lock, defaulting to **14K yellow gold**. The declared metal is recorded in `config/deliveries/LR-XXXX.json` and locks that whole catalog. This slot renders only the metals the listing actually offers, and is **skipped entirely for single-metal listings** — never show a metal that is not for sale.*

### 2.10 Slot 10 — Packaging & Brand (TEMPLATE — build once, reuse everywhere)
```
Premium unboxing still life. The ring seated inside an open jewellery box,
accompanied by a folded premium white cotton cloth bearing the LucentCaratLab
logo, a pouch and a thank-you card. Surface: [POOL A]. Lighting: [POOL B].
Luxury gift presentation mood, warm and inviting.
The logo must appear naturally printed into the cotton weave, following the
fabric's folds and perspective, with correct colour, typography, spacing and
alignment. No sticker, overlay, floating, embossed or artificially applied
appearance. No white box behind the logo.
```
*Logo rules here are owned by `04` §14.0/§14.1b — official preserved asset only, never AI-drawn.*

**Best practice:** photograph the real packaging once with a phone and reuse that single real image across all listings. Real packaging beats generated packaging and sets honest delivery expectations.

### 2.11 ▶ Video Slot — 5 to 15 seconds
> **ASK BEFORE GENERATING.** No video is produced without explicit per-request permission from the user.
```
The ring rotating slowly and smoothly through 360 degrees on an invisible
turntable, centred in frame, against a clean [POOL A] background.
A soft light source sweeps across the stone during the rotation so the facets
flash and the fire animates. Constant camera position, no zoom, no cuts.
Smooth constant rotation speed, approximately 12 seconds per full revolution.
Photorealistic, no motion blur on the ring, no warping of geometry during
rotation.
```
*Etsy videos play silent — no audio needed. Once a real finished ring exists, film it on a cheap turntable and replace this; real sparkle video outperforms every generated asset.*

## 3. STUDIO SCENE CONSTANT (locked white-cloth frames)

Appended in place of a theme variant wherever the locked studio background is used — the studio setup is locked, not rotated (`11`, `04`). Under the 2026-07-20 slot map this covers slot 10 for certain, plus whichever product slots resolve to cloth (see the §4.0 open item):

```
Premium pure-white cotton cloth, naturally draped, folds falling where gravity
would really put them. The brand logo printed into the weave, following every fold
and the perspective of the surface — never a floating overlay. Bright neutral-white
daylight, correct white balance, no warm or colour cast.
```

Within these slots only the *flavour* of the camera rotates per `12` §A1 — e.g. this SKU's profile at 10–15° yaw instead of dead-flat 90°, next SKU's high three-quarter from the opposite corner. The slot's role is fixed; its exact camera is not.

---

## 4. THEME_VARIANT — THEME POOLS, THE ANTI-AI-LOOK ENGINE

### 4.0 SCOPE — LIFESTYLE SLOTS ONLY (decided 2026-07-20)

**Pools A/B/C apply to lifestyle slots only** — under the new slot map that is slots 4 and 5. Product frames keep the locked premium white cotton cloth + printed logo + neutral daylight (`11`, `04`, `03`). No change to `11` or `12` §A2.

Rationale, so this is not re-litigated: the uniform white-cloth-with-logo studio set is the brand signature, and real studios do shoot every product frame on the same sweep — uniformity across product shots reads as professional consistency, not as AI. The "AI look" comes from lifestyle frames with repeated props and identical staging, which is exactly where the pools belong. Rotating studio surfaces would also leave the printed logo (`04`) with no cloth to print into on the marble/concrete/acrylic variants.

Pool D (palette) may tint lifestyle frames only; it never overrides the studio white balance in `11:144`.

**Resolved 2026-07-20 — slots 1, 2 and 3 keep the locked white cotton cloth + printed logo, NOT Pool A.** Where a slot prompt says `Background: [POOL A]`, read it as the §3 studio constant on slots 1–3, 7 and 9. Pool A feeds slots 4 and 5 (and the surface of slot 6 / slot 10 staging). `11` MASTER BACKGROUND LOCK stands unamended.

Rotate ONE variant from each pool per listing. Never use the same combination twice in a row across the shop grid. Resolve deterministically: `index = hash(SKU) % pool_size`.

### Pool A — Surface / material (lifestyle product-on-surface frames)
| # | Variant |
|---|---|
| A1 | soft matte white seamless paper, gentle gradient falloff |
| A2 | warm ivory linen textured backdrop |
| A3 | pale honed Carrara marble slab |
| A4 | brushed off-white concrete micro-texture |
| A5 | cool light grey studio sweep with subtle vignette |
| A6 | natural raw silk fabric, soft folds |
| A7 | pale travertine stone with fine natural pitting |
| A8 | frosted acrylic riser on white, faint reflection |

### Pool B — Lighting mood
| # | Variant |
|---|---|
| B1 | large softbox from upper left, gentle fill right, soft shadow lower right |
| B2 | north-facing window daylight, cool neutral, long soft shadow |
| B3 | golden hour side light, warm 3200K, elongated soft shadow |
| B4 | overcast diffused light, near-shadowless, even and clean |
| B5 | single focused spot with dark falloff, dramatic and editorial |
| B6 | dual strip lights creating twin highlights on the metal band |
| B7 | backlit rim light with soft frontal fill, glowing stone edges |
| B8 | morning light through sheer curtain, faint dappled pattern |

*B3 / B5 / B8 carry warm or uneven colour temperature — permitted on lifestyle slots, never on slots 1–8 (`11:144`, the LR-0154 warm-cast rejection).*

### Pool C — Prop / styling (lifestyle shots)
| # | Variant |
|---|---|
| C1 | open navy velvet ring box, scattered white rose petals |
| C2 | cream silk ribbon loosely coiled, dried baby's breath sprigs |
| C3 | vintage brass tray, single blush peony, water droplets |
| C4 | folded ivory linen napkin, sprig of eucalyptus |
| C5 | antique mirror surface with soft reflection, pearl strand |
| C6 | open leather-bound book, pressed flower, warm lamp glow |
| C7 | white ceramic dish, morning coffee cup blurred behind |
| C8 | draped ivory tulle fabric, soft bokeh fairy lights far background |

*Props stay softly blurred and subordinate — the ring is still the instant focal point (`12` §A2). A prop that pulls the eye first is a reject regardless of pool.*

### Pool D — Season / palette overlay (rotate monthly for freshness)
| # | Variant |
|---|---|
| D1 | neutral bridal palette — ivory, blush, warm gold |
| D2 | cool minimal palette — white, grey, cool platinum tones |
| D3 | autumn palette — amber, terracotta, warm brass accents |
| D4 | festive palette — deep jewel tones, soft candlelight warmth (use Oct–Nov) |

### Pool S — Slot 9 / 10 scene pairing
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

Append to EVERY prompt.

```
Shot on Canon EOS R5 with 100mm f/2.8 macro lens, f/8, focus stacked, true
colour accuracy, natural micro-imperfections in metal surface, realistic
subsurface light behaviour in the diamond, no plastic or waxy rendering,
no oversaturation, no HDR halo, photorealistic commercial jewellery
photography, 3000x3000px, tack sharp.
```

**Negative prompt** (if the pipeline supports it):

```
cgi, 3d render, plastic, waxy, oversaturated, hdr glow, extra prongs, missing
prongs, deformed band, warped stone, wrong facet pattern, text, watermark,
logo, signature, blurry, distorted hands, extra fingers, fused fingers,
unnatural skin, mannequin hand, fake certificate
```

**Two usage notes (owners win, per `17` POLICY MERGE RULE):**
1. **Drop `logo` from the negative list on slots 1–8.** Those frames REQUIRE the brand logo printed into the cloth (`04` §14.1b). The term is there to block AI-invented marks — on studio slots that job is done by `04`'s official-asset lock instead. Keep `logo` in the negatives only for slots 9–10 and any frame with no cloth.
2. **`f/8, focus stacked, tack sharp` applies to the RING, not the frame.** `12` §A1(2)/§A2 still govern: real shallow depth of field, background softly blurred and never sharper than the ring. Read the tail as "the jewelry is fully sharp front-to-back"; it does not authorise an everything-in-focus flat image.

---

## 6. PRE-DELIVERY CHECKLIST (per catalog)

- [ ] All 10 slots present, in order, each a distinct reserved orientation (`12`, ≤20% similarity)
- [ ] Every prompt assembled as PRESERVATION + SLOT + THEME/STUDIO + QUALITY_TAIL
- [ ] Geometry identical to source on every frame (`13`, `16`) — fall through the `12` §A3 ladder if not
- [ ] Same cloth, same logo treatment, same white balance across slots 1–8 (`11`, `04`)
- [ ] Theme, pool variants (A/B/C/D/S) and video style resolved by `hash(SKU)`, not chosen ad hoc
- [ ] No pool variant applied to slots 1–8; no A/B/C combination repeated back-to-back across the shop grid
- [ ] Ring is the instant focal point in all 11 assets (`12` §A2)
- [ ] Resolved theme index + video index + camera variants written to `config/deliveries/LR-XXXX.json`

---

## 7. ANTI-"AI LOOK" CHECKLIST (user-locked 2026-07-20)

Run before uploading any listing set. Complements — never replaces — the pre-generation and final gates in `18` and `03`.

| Check | Why it matters |
|---|---|
| ☐ No two listings in the same shop row share a Pool C prop | Repeated props are the #1 tell of AI generation |
| ☐ Shadow direction is consistent within a listing, varied between listings ¹ | Real shoots have one light setup per session |
| ☐ Hand skin tone varies across the catalogue | Same hand on 200 listings looks synthetic |
| ☐ Metal shows fine surface micro-scratches, not mirror-perfect | Real gold is never flawless |
| ☐ At least one tiny natural imperfection per scene — a stray petal, a fabric crease, an uneven shadow edge | Perfect symmetry reads as fake |
| ☐ Colour temperature drifts slightly between listings ¹ | Real photography is never perfectly uniform |
| ☐ Prong count and band width match the CAD exactly | Legal and commercial requirement |
| ☐ Hand images: 5 fingers, natural joints, believable ring scale | Deformed hands destroy trust instantly |
| ☐ No AI-rendered text anywhere in any image ² | Garbled text is an instant giveaway |
| ☐ Certificate images use real scans only | Fabricated certificates are fraud |

**¹ Lifestyle slots only (4, 5).** Product slots keep the locked neutral studio setup: `11:115` requires every studio catalog to be shot "under identical neutral studio lighting, with no artificial colour grading or colour shift," and `11:144` rejects even a *subtle* warm cast (the LR-0154 rejection). Between-listing shadow and colour-temperature drift is exactly what those locks forbid on cloth frames — so vary it in the lifestyle scenes, where it genuinely reads as separate photo sessions, and keep product frames identical shop-wide. Within any single listing, `18` §7 already requires matched white balance, exposure, contrast and shadow density.

**² The printed cloth logo is not AI-rendered text** — it is the preserved official asset (`04` §14.0), which is precisely why this check passes. Any *other* text (carat labels on slot 7, certificate numbers on slot 6, watermarks) is added after generation in code or Canva, never by the model.

**Micro-scratches note:** consistent with `03` §METAL, which already demands "slight surface variation" and bans "mirror-like perfection." Read it against the MASTER METAL COLOUR line's "bright mirror polish" as: high-polish finish *with* believable micro-texture, not a flawless chrome surface.

---


---

## 8. PRODUCTION SUMMARY PER LISTING (user-locked 2026-07-20)

| Type | Count | Notes |
|---|---|---|
| Unique generations | 6 | Slots 1, 2, 3, 4, 5, 8 |
| Composite (not generated) | 1 | Slot 6 — real IGI scan laid into a generated empty flat-lay |
| Template reuse | 3 | Slots 7, 9, 10 — pulled from the asset library by cut shape / design |
| Video | 1 | Generated or filmed — **ask before generating** (`20` §2.11) |
| **Total Etsy assets** | **10 images + 1 video** | Fills every available Etsy slot |

*Slot 6 is listed separately because it is neither a fresh generation nor a library template: the frame is generated empty and the certificate is composited afterwards. Your original summary had 6 + 3 = 9 images against a 10-slot total; this row closes the gap.*

### Asset library — build once
| Template | Count | Rebuild trigger |
|---|---|---|
| Carat size chart (§2.7) | 8 — one per cut shape: Round · Oval · Marquise · Dutch Marquise · Pear · Emerald · Radiant · Asscher | New cut shape added |
| Metal variants (§2.9) | 1 per design that offers multiple metals — skipped for single-metal designs | New design, or a design's metal range changes |
| Packaging & brand (§2.10) | 1 universal — ideally a real photograph of the actual packaging | Packaging changes |

*Count check: 8 charts + 8 metal sheets (one per design, each showing 3 metals) + 1 packaging = **17**, not 24. 24 would be the number if metal variants were counted as 8 designs × 3 individual renders — but §2.9 is a single side-by-side frame, so it is one asset per design. Adjust if you meant 8 charts + 24 separate metal renders (= 33 total).*

### Throughput
- **~20 minutes per listing** at steady state
- **200 listings** ≈ 1,200 unique generations + 200 slot-6 composites + 200 videos
- ≈ **67 hours** ≈ 2 hrs/day over 6 weeks

*Cost note: `17` MASTER TOKEN OPTIMIZATION applies — reuse each `media_id` (cloth, logo, CAD, approved masters) across the six generations rather than re-uploading, and fix cloth/logo defects locally at 0 credits instead of regenerating a frame.*

---

