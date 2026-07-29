# LR-0203 — SOURCE-SPEC (geometry lock)

Source: Drive folder "LR- 0203" (main folder only), 4 webp views in `source/`.
Corrected 2026-07-29 from user-supplied authoritative source image. Re-read before EVERY generation. Never redraw the stone; transfer exact source geometry (i2i preserve). This ring is a PLAIN solitaire — do NOT confuse with LR-0204 (which is a hidden-halo ring).

## Ring identity (AUTHORITATIVE)
- **Type:** classic OVAL solitaire, plain — NO halo of any kind.
- **Centre stone:** OVAL brilliant, **north–south** (long axis vertical), single centre stone. Elongated.
- **Head / prongs:** exactly **4 PLAIN slender claws, compass-set** (one at each compass point gripping the oval). Plain rounded claws — NOT split, NOT double, NOT fluted.
- **Hidden halo:** **NONE.** ZERO pavé under the head. No pavé collar, no basket diamonds, no accent stones beneath the crown. The area under the stone is plain metal only.
- **Basket / gallery:** plain metal basket — no diamonds set in it.
- **Shank:** **SINGLE row** of pavé on the shoulders only, matching source count/size/spacing. Does NOT wrap around/under the shank; shoulders only, plain rounded back. Thin delicate band.
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
```
Rejected render: img 04 (macro head) — added hidden halo + split claws + double-row pavé + invented basket. Cause: category prior + AI embellishment. Fix: strengthen negative locks (no halo / no basket / plain single-row / plain 4 claws) in every 0203 prompt.
