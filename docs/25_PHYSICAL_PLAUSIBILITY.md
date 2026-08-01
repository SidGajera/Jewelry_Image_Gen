# 25 — PHYSICAL PLAUSIBILITY (checked on EVERY image, every category, user-locked 2026-07-30)

Geometry gates ask "does it match the source?"; logic gates ask "could this exist?" **Both must pass.** An image can be pixel-accurate to the CAD and still physically impossible. Checked before any render is verified.

## L1 — WORN CONTINUITY (rings, bracelets, bangles) — CODE, BLOCKING
Segment the band; trace both arms from the centre element — both must terminate on the SAME finger/wrist segment. Band crossing an inter-finger gap = FAIL. Bracelet passing through the arm or not closing = FAIL. → `G15` (`ring_on_one_finger`: off-axis > 0.7× finger spacing = spans two fingers).

## L2 — PLACEMENT — CODE, BLOCKING
Ring centre between the MCP and PIP joints of one finger; at the webbing / over a knuckle / past the fingertip = FAIL. Earring at the lobe, pendant at the sternum, bracelet at the wrist. → `G15` (t∈[−0.4,1.4] between MCP–PIP).

## L3 — ANATOMY — CODE, BLOCKING
MediaPipe landmarks: exactly 5 digits, correct joint counts, detection confidence > 0.8. Fused fingers, extra/missing digits, impossible thumb angle, duplicated knuckles, elbow/wrist inversion = FAIL. → `G15` (`hand_anatomy_ok`): handedness score > 0.8; landmark topology sane. NOTE: the 21-landmark model always returns 5 fingers, so a 6th finger drawn as extra pixels is only partially detectable — L3 is code-assisted but the visual checklist still backstops digit count.

## L4 — SUPPORT & GRAVITY — VISUAL CHECKLIST (mandatory until automated)
Studio: the piece rests on the surface, not floating, not sinking. Contact shadow exists and matches the light. An upright ring needs the shank contacting the cloth.

## L5 — OCCLUSION — VISUAL CHECKLIST
Anything in front occludes what's behind, consistently. Fingers through metal, cloth through the band, a stone visible through an opaque prong = FAIL.

## L6 — LIGHT CONSISTENCY — VISUAL CHECKLIST
One dominant light direction across subject, background and shadows; specular highlights on metal agree with it. Shadow the wrong way = FAIL.

## L7 — SCALE — VISUAL CHECKLIST
Piece dimensions plausible against the body part. Ring wider than the finger, stone larger than a knuckle = FAIL. (Code proxy: `G9` scale, advisory.)

## L8 — REFLECTION SANITY — VISUAL CHECKLIST
Reflections in polished metal correspond to the actual scene. Invented interiors / mismatched environments = FAIL.

## ENFORCEMENT
- **L1–L3 = code, BLOCKING** (MediaPipe + band segmentation): `G15` (+ `G14`/`G16` for subject/skin). Any confident fail → auto-regenerate with the retry negatives.
- **L4–L8 = mandatory visual checklist on EVERY render** until automated — never skipped, never assumed. The completion line must not imply L4–L8 were machine-verified when they were reviewed visually.

## RETRY NEGATIVES (append on an L1–L3 fail)
`ring between two fingers, ring spanning two fingers, band crossing the gap between fingers, ring at the webbing, ring over a knuckle, floating ring, ring not encircling a finger, fused fingers, extra fingers, six fingers, missing finger, malformed hand, bracelet through the arm, open unclosed clasp`
