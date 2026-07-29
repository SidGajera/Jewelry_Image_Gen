# LR-0101 (Dutch Marquise) — Source Spec

**Product:** Three-stone engagement ring, 18k YELLOW GOLD. Dutch-marquise center + 2 trapezoid step-cut sides, hand-engraved shoulders.

## Geometry locks (verified against ALL 8 source angles — gloves 1-6 + on-hand 1-2, 2026-07-29)
1. **Center = DUTCH MARQUISE cut diamond.** Elongated marquise silhouette, SHARP point at BOTH top AND bottom (long axis vertical); antique/old-mine "crushed-ice" faceting with broad flat central facets and stepped points (NOT a clean modern brilliant marquise, NOT a modern cushion/oval, NOT an emerald, NOT a hexagon). Faint warm/champagne-white tint. Two sharp points must be visible every render.
2. **Two SIDE stones = EMERALD-CUT rectangles** (step-cut, cropped corners), one flanking each side of the center, 4-prong set. NOT trapezoids, NOT baguettes, NOT kites, NOT rounds. (Front macros foreshorten them to look trapezoidal — the 3/4 gloves-4 and profile gloves-6 views show clean emerald-cut rectangles.)
3. **Center prongs = SIX total:** double V-claw cradling the TOP point, double V-claw cradling the BOTTOM point, and one prong at each side belly (widest points). Yellow gold.
4. **Gallery:** openwork / pierced scroll basket under the center (visible gloves 3 + gloves 5).
5. **Shoulders/shank:** hand-ENGRAVED scroll/filigree pattern running along the top face AND down BOTH sides of the shank, with milgrain edges (gloves 4, 6). NOT a plain shank.
6. **Band:** thin, high-polish 18k yellow gold, low-medium profile. Single warm gold tone.

## Source angle inventory (all real pixels — deliver ONLY these angles, never invent)
- Front macro (points to camera): gloves 1, gloves 2
- 3/4 top: gloves 4
- Back 3/4 / gallery: gloves 3
- Profile / side elevation: gloves 5, gloves 6
- Top-down on bare finger: on-hand 1, on-hand 2

## DUTCH-MARQUISE RULES (mandatory)
- Center MUST show TWO sharp points (top + bottom) and the elongated marquise outline in every render.
- Keep the antique crushed-ice faceting — do NOT redraw as a sleek modern marquise or flatten to emerald/hexagon.
- NEVER shoot a pure flat side profile that hides the points — use a 3/4 or top-down angle so both points + trapezoid sides stay visible.
- Validate "pointed top + pointed bottom + 2 trapezoid sides + engraved shoulders + yellow gold" BEFORE delivering; reject + regen on any drift.

## Source: main folder = Lucentcaratlab.zip (clean CAD studio renders, 160MB — NOT yet pulled) + worn refs (ON HAND ×2, GLOVES ×6) + watermark/ subfolder (ignored). Spec built from GLOVES(1) front macro, ON HAND(1), GLOVES(5) profile.

## Delivery: iterate Image 1 (velvet hero, 3/4) to approval → lock master → batch rest (4 office velvet + 6 lifestyle, distinct angles/poses, 100% natural). marketing_studio_image source-locked. Save to deliveries/LR-0101/.

## FAILURE MEMORY (re-read before every gen)
- **2026-07-29 REJECT (Image 1, marketing_studio_image i2i):** the model REDREW the jewelry — center Dutch marquise came out as a rounded modern cushion/oval (lost both sharp points + antique crushed-ice faceting) and the emerald-cut sides became different step stones. Cause: marketing_studio_image / any i2i regenerates the whole ring = prohibited AI redraw. Also I had only studied 3 of 8 source angles and mis-called the sides "trapezoid." Fix: (a) study ALL source angles before any gen; (b) NEVER redraw/regenerate the jewelry — preserve REAL source ring pixels (cutout/composite), only build the scene around it; (c) deliver only angles that exist in source.
