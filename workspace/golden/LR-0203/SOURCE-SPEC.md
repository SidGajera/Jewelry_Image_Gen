# LR-0203 — SOURCE-SPEC (geometry lock)

Source: Drive folder "LR- 0203" (main folder only), 4 webp views in `source/`.
Corrected 2026-07-29 from user-supplied authoritative source image. Re-read before EVERY generation. Never redraw the stone; transfer exact source geometry (i2i preserve). This ring is a PLAIN solitaire — do NOT confuse with LR-0204 (which is a hidden-halo ring).

## Ring identity (AUTHORITATIVE)
- **Type:** classic OVAL solitaire, plain — NO halo of any kind.
- **Centre stone:** OVAL brilliant, **north–south** (long axis vertical), single centre stone. Elongated.
- **Head / prongs:** exactly **4 PLAIN slender claws, compass-set** (one at each compass point gripping the oval). Plain rounded claws — NOT split, NOT double, NOT fluted.
- **Hidden halo:** **NONE.** ZERO pavé under the head. No pavé collar, no basket diamonds, no accent stones beneath the crown. The area under the stone is plain metal only.
- **Basket / gallery:** plain metal basket — no diamonds set in it.
- **Shank:** **SINGLE row** of pavé. Count-locked **18–20 MICRO stones per side** (each ~1/10 band width), tightly packed near-touching, uniform, minimal metal between. **Flush French/micro-bead set** — level with band surface; NO raised channel, NO thick beads, NO metal rail below stones. Coverage runs from head **DOWN PAST THE SHOULDER** toward the lower shank (front ~two-thirds of shank), NOT stopping at the shoulder. Does NOT wrap under the shank. Plain rounded back.
- **Band profile:** THIN, uniform width shoulder→base, round/knife-edge. NO taper, NO flat top, NO widening at shoulders, NO cathedral rise.
- **Scale:** centre-stone width ≈ **4.5× band width at the shoulder**. Do NOT enlarge centre relative to band.
- **Format:** 1:1 SQUARE, exactly 2048×2048 native. Portrait/landscape = auto-reject before visual review.
- **Metal:** WHITE — white gold / platinum. No yellow gold.

## Locks (do not violate)
- OVAL, north–south, single centre — never round/marquise/3-stone.
- Exactly 4 PLAIN slender compass-set claws — never double/split/fluted, never 6, never bezel.
- ABSOLUTELY NO halo, NO hidden halo, NO pavé under head, NO basket diamonds.
- Shoulder pavé = SINGLE row only, shoulders only, per source spacing.
- White metal only. Preserve exact source geometry (i2i), never redraw.

## FAILURE MEMORY (re-read before each gen)
```
MISTAKE: hidden halo pavé added beneath center stone.
CAUSE: model applied category prior (oval solitaire -> hidden halo default).
RULE: LR-0203 has ZERO halo. No pave under head. No basket diamonds. Reject on sight.

MISTAKE: prongs rendered as double/split fluted claws.
CAUSE: AI restyling of prong geometry.
RULE: exactly 4 plain slender claws, compass-set. No splitting, no fluting.

MISTAKE: shoulder pave rendered as double row wrapping shank.
CAUSE: AI embellishment.
RULE: single row pave, shoulders only, per source count/size/spacing.

MISTAKE: shoulder pavé UNDER-COUNTED — ~10 stones/side vs source ~18–20 (slot 03, 2026-07-30).
CAUSE: model chose its own pavé count/size instead of matching source pixels.
RULE: single row, EXACTLY 18–20 micro stones/side, never fewer. Count-lock in prompt; do not let model choose.

MISTAKE: pavé rendered oversized + widely spaced (slot 03).
CAUSE: AI scaled stones up, added gaps.
RULE: MICRO pavé, each ~1/10 band width, tightly packed near-touching, uniform, minimal metal between.

MISTAKE: pavé coverage stopped at shoulder (slot 03).
CAUSE: AI shortened the pavé run.
RULE: coverage runs head → DOWN PAST SHOULDER (front ~2/3 of shank), never stopping at shoulder.

MISTAKE: pavé set as raised channel with thick beads + flat metal edge (slot 03).
CAUSE: AI restyled setting.
RULE: flush French/micro-bead, level with band. NO channel, NO thick beads, NO metal rail below stones.

MISTAKE: band widened/flattened/tapered (slot 03).
CAUSE: AI restyled band profile.
RULE: thin uniform round/knife-edge, no taper/flat/widening/cathedral.

MISTAKE: centre stone oversized vs thin band (slot 03).
CAUSE: AI enlarged centre.
RULE: centre width ≈ 4.5× band width at shoulder; do not enlarge relative to band.

MISTAKE: delivered PORTRAIT instead of 1:1 square (slot 03).
CAUSE: format not gated before visual review.
RULE: 1:1 exactly 2048×2048; any non-square = discard + regenerate BEFORE visual review.
```
Rejected renders:
- img 04 (macro head) — added hidden halo + split claws + double-row pavé + invented basket. Cause: category prior + AI embellishment. Fix: strengthen negative locks (no halo / no basket / plain single-row / plain 4 claws) in every 0203 prompt.
- slot 03 (velvet_upper_3q) — 7 deviations: pavé under-count, pavé oversized/spaced, coverage stops at shoulder, raised-channel setting, band widened/tapered, centre oversized vs band, delivered portrait. Fix: MANDATORY PROMPT LOCKS below.

## MANDATORY PROMPT LOCKS (append to EVERY slot prompt — user-locked 2026-07-30)

**FORMAT (auto-reject gate, checked BEFORE visual review)**
- 1:1 SQUARE, exactly 2048×2048 px, native. Any portrait/landscape/non-square = discard + regenerate; do not review.

**CENTER STONE** — ONE oval brilliant, elongated, standard oval brilliant facets. Width ≈ 4.5× band width at shoulder. Do NOT enlarge centre relative to band.

**PRONGS** — exactly 4 plain slender claws, compass-set (12/3/6/9). NO double/split/fluted claws, NO 5th prong.

**UNDER-HEAD** — plain polished basket. NO hidden halo, NO diamonds under head, NO basket pavé, NO peekaboo stones.

**SHOULDER PAVÉ (count-locked — do not let model choose)** — SINGLE row/side, exactly 18–20 stones/side, never fewer. MICRO (each ≈1/10 band width), tightly packed near-touching, uniform, minimal metal between. Coverage head → DOWN PAST SHOULDER (front ~2/3 of shank), not stopping at shoulder. Flush French/micro-bead, level with band. NO raised channel, NO thick beads, NO metal rail below. NO second row, NO band-edge/under-gallery pavé.

**BAND** — thin, uniform width shoulder→base, round/knife-edge. NO taper/flat top/widening/cathedral.

**METAL** — white gold/platinum, high polish. No yellow, no rose, no two-tone.

**NEGATIVE PROMPT (verbatim, always include)**
```
hidden halo, halo, diamonds under center stone, basket pave, peekaboo diamonds,
double prong, split prong, fluted prong, 5 prongs, 6 prongs,
double row pave, second pave row, large pave stones, widely spaced pave,
channel set, thick bead setting, metal rail under pave, pave stopping at shoulder,
tapered band, wide band, flat band, cathedral shoulders,
second ring, extra ring, duplicate jewelry, watermark, text, logo overlay,
portrait format, landscape format, non-square crop
```
