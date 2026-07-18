# 18 — MASTER CATALOG CONSISTENCY POLICY (user-locked 2026-07-18)

Every catalog must read as ONE uninterrupted professional photoshoot: unique angles, and identical jewelry / diamond / metal / cloth / logo / lighting across all images. Consolidates the angle-uniqueness, diamond-parity, cloth, logo and lighting locks; where a stricter number exists elsewhere, the strictest wins (`17` POLICY MERGE RULE — e.g. `12` uses a ≤20% similarity bar, tighter than the 90% floor below).

## 1. ONE UNIQUE CAMERA ANGLE = ONE IMAGE
One purpose per image. Never two images with nearly identical camera angle, 3/4 angle, zoom level, composition or ring orientation. Each image must clearly differ in camera position · height · rotation · distance · perspective. Similarity over the bar → reject and regenerate. (Detail + 20% bar: `12` ONE IMAGE PER ANGLE.)

## 2. CAMERA ANGLE LOCK
Before generating, compare against every previously approved image. If the angle already exists → reject and generate a different angle. Never deliver duplicate viewpoints.

## 3. CATALOG ANGLE MAP
Each required angle generated only once, then locked and never reused, e.g.: Hero Front · Hero 45° · Side Profile · Rear Profile · Top Close-up · Lifestyle 1 · Lifestyle 2 · Lifestyle 3 · Lifestyle 4. (Lifestyle set structure: `03` LIFESTYLE SET COMPOSITION — 3 close-up + 4 close-framed.)

## 4. DIAMOND APPEARANCE LOCK
Office photos are the MASTER REFERENCE for diamond appearance. Every lifestyle image must match: diamond brightness · facet sharpness · fire · contrast · clarity · white balance · sparkle intensity. Never cloudy · milky · gray · soft · blurry-facet · reduced-brilliance diamonds. (Detail: `03` DIAMOND CONSISTENCY POLICY.)

## 5. METAL COLOR LOCK
One gold tone for the whole catalog. Never yellow/orange/green shift, dark gold or pale gold. (Detail: `03` LOCKED 18K GOLD CONSISTENCY.)

## 6. CLOTH COLOR LOCK
The approved cloth is the catalog master: same white point · fabric · texture · weave · brightness. Only premium plain white cotton — never cream/ivory/yellow/gray/blue/warm/satin. (Detail: `11` CLOTH & LOGO LOCK MODE.)

## 7. LIGHTING CONSISTENCY
Every image matches white balance · exposure · contrast · highlight roll-off · shadow density. Never change lighting style between images.

## 8. LOGO CONSISTENCY
Load the approved logo once; every studio image uses the identical preserved logo (`assets/logo/logo_official.png` as a Higgsfield reference). Never regenerate, redraw, recolor or misresize. (Detail: `04` §14.0, `11`.)

## 9. CATALOG MEMORY
On approval of an image, store: camera angle · height · lens · distance · lighting · cloth · gold color · diamond appearance in `config/deliveries/LR-XXXX.json` (baseline, `15` §8). Every subsequent image references this baseline before generation.

## 10. PRE-GENERATION VALIDATION (gate)
Before generating each image, confirm: ✓ camera angle unique · ✓ jewelry matches CAD · ✓ cloth matches approved cloth · ✓ logo matches preserved logo · ✓ diamond appearance matches office photos · ✓ gold color matches previous images · ✓ lighting matches previous images. Any check fails → reject and regenerate. Final set gate: `03` CATALOG FINAL VALIDATION.
