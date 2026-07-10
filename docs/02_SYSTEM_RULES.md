# 02 — SYSTEM RULES (permanent)

Every permanent rule currently in force, in **priority order**. Higher number on the list = lower priority; when two rules conflict, the higher-priority (earlier) rule wins.

## PRIORITY ORDER

### P0 — BRAND LOGO PRESERVATION (overrides everything)
- The official logo is a LOCKED ASSET (`assets/logo/logo_official.png`). Never regenerate, redraw, interpret, verify-by-reading, enhance, vectorize, recreate, OCR, "fix", or hallucinate it.
- The logo is NEVER rendered by the AI model. It is composited from the locked file AFTER generation.
- The logo must ALWAYS appear on studio cloth, looking **physically printed** (not a watermark/sticker/overlay). Partial crop / fold distortion / jewelry occlusion (60–90 % visible) is acceptable and preferred.
- Never ask the user to verify whether the logo is correct.

### P1 — JEWELRY DESIGN FIDELITY
- The ring must be 100 % identical to the SOURCE — design, shape, band, every stone, stone count, prongs, side settings, gallery, setting, metal. Change NOTHING (not even 0.00000000000000001 %) without explicit permission.
- Always VIEW the correct source file before generating. Ignore stray/mislabeled source images.
- Never add, remove, resize, restyle, or recolor stones. Green emeralds stay green; baguettes stay baguettes; halos keep their exact shape (round vs cushion — never swap).

### P2 — DIAMOND / GEM RENDERING
- Every stone renders like a REAL photographed stone: one clean facet pattern, natural mix of bright-white AND dark grey/black facet reflections, crystal clear.
- NO doubled/mirrored/ghost facets, NO CGI kaleidoscope, NO glassy flat dots, NO plastic/opaque/blown-out stones.
- Small pavé as crisp and faceted as the center, just smaller.
- Benchmark = LR-0156 studio shot (rendering reference only, not a design change).

### P3 — LOCKED BACKGROUND (cloth)
- Locked cloth material (reference pouch fabric); never substitute another material.
- Pure neutral/bright luxury white every time; never cream/ivory/beige/yellow/warm/off-white/gray/blue/pink. No warm lighting on cloth.
- Same texture, softness, grain, fold style, wrinkle character, premium look, consistent across all images.

### P4 — NATURAL LIGHT & REALISM
- Natural, realistic light and sparkle only. No over-lighting, artificial light, exaggerated sparkle, CGI glow, starburst/lens flare, or rainbow fire. Real DSLR macro look.

### P5 — OUTPUT FORMAT
- ALL images 1:1 aspect and 2K resolution. Ring tack-sharp; only background blurs.
- Model: Higgsfield `nano_banana_2`, `resolution:"2k"`. (Server may label the multi-image edit path `nano_banana_flash` internally; the controllable that matters is `resolution:"2k"`.)

### P6 — LIFESTYLE THEME
- Cozy warm US-home; consistent theme; different pose each shot; natural hand with exactly five fingers, natural skin, neutral manicure. NO laptops/desks/offices. No invented logo in lifestyle/closeups.

### P7 — TOKEN OPTIMIZATION (never at the cost of P0–P6 quality)
- Reuse cached assets; no duplicate work; batch generations; no preview tools; compact full-quality prompts. See `docs/05_TOKEN_OPTIMIZATION.md`.

### P8 — COMMUNICATION / CREDITS
- Never use preview tools (`show_generations`, `job_display`). User reviews in Higgsfield.
- Report count only; brief replies; take permission once per batch.
- Do NOT spend Higgsfield credits fixing our own mistakes — fix locally (0 credits) wherever possible.
- 2 credits per 2K image; confirm inputs before firing a full batch on a novel/risky design.

## THINGS THAT MUST NEVER CHANGE
1. The logo is never AI-generated and never altered — only the locked asset is composited.
2. The jewelry design is never modified relative to the source.
3. The cloth material and neutral-white color are locked.
4. Output is always 1:1 / 2K.
5. Operate only as `lucentcaratlab@gmail.com`.
6. Local (0-credit) fixes are preferred over paid regeneration for cloth color and logo.

## HARD-WON LESSONS (do not repeat)
- Model garbles any logo it tries to render → "ELLYREID". Never let it render the logo.
- Doubled center diamond appears on large worn/lifestyle angles → enforce single facet pattern.
- Wrong lifestyle theme (hand on laptop) → force cozy home, forbid desks/laptops.
- `generate_image` needs explicit `resolution:"2k"` (default is 1k) and `params.model:"nano_banana_2"`.
- Higgsfield `media_id`s expire across sessions → durable cache is the Drive file IDs (re-import when a call rejects an id).
- Use the correct source file; ignore strays (LR-0167 "Copy of 7/4" were from another ring).
