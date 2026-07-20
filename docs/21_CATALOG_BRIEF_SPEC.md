# 21 — CATALOG BRIEF SPEC (user-locked 2026-07-20)

> **AUTHORITATIVE OWNER (see `00` POLICY INDEX):** the INPUT spec for a generation run — required brief fields, per-category fields, the run order, and batch CSV shape. What each slot contains is owned by `20`; how the images are judged is owned by `03`/`11`/`12`/`13`/`18`.

## The principle
A catalog brief is a **data handoff, not a conversation.** If the brief is complete, the pipeline runs without asking anything. Every question the agent has to ask means a field was missing from the brief.

Anything the agent has to *infer* — metal, carat, clasp type, whether it's a pair — is a place where the render can silently diverge from what actually ships. The brief's job is to leave nothing inferable.

## 1. UNIVERSAL FIELDS — required for every category
| Field | Example | Why it's required |
|---|---|---|
| `sku` | `LCL-RND-2CT-0142` | Drives the theme-rotation hash — no SKU, no deterministic theme (`20` §0) |
| `category` | `ring` \| `bracelet` \| `necklace` \| `earring` | Selects preservation block + slot map. **Fail loudly if absent** (`20` §9.3) |
| `source_cad` | `cad/LCL-0142_4view.png` | The only source of truth. No CAD = no render |
| `metal` | `14K yellow` | Per-listing parameter since `03` §C — never assume |
| `centre_stone` | `Round, 2.00CT, E, VVS2` | Cut / carat / colour / clarity |
| `accent_stones` | `Round, 0.22 TCW, 1.2mm, 18 pcs` | Or `none` |
| `certification` | `IGI` + path to the real scan | Slot 6 composite needs the actual file (`20` §2.6) |
| `listing_title` | Exact live Etsy title | Cross-check: the title's metal must equal the `metal` field |
| `season` | `bridal` \| `cool` \| `autumn` \| `festive` | Theme palette, Pool D (`20` §4). Use `festive` for Oct–Nov |

## 2. CATEGORY-SPECIFIC FIELDS

**RING — add**
```
ring_size_shown   : 6.5          (which size the render depicts)
setting_type      : solitaire | halo | three-stone | bypass | cathedral
prong_count       : 4 | 6
band_width_mm     : 1.8
band_thickness_mm : 1.6
pave              : yes/no + count + size
```

**BRACELET — add**
```
length_in     : 7.0            (and which lengths the listing offers)
clasp_type    : lobster | spring ring | box | toggle
link_style    : paperclip | tennis | cable | curb
link_count    : 18
chain_gauge_mm: 2.4
adjustable    : yes/no + extender length
```

**NECKLACE / PENDANT — add**
```
chain_length_in : 18           (and all lengths offered)
chain_style     : cable | box | rope | figaro
chain_gauge_mm  : 1.0
pendant_drop_mm : 12.5
bail_type       : fixed | hinged | integrated
clasp_type      : lobster | spring ring
```

**EARRING — add**
```
quantity        : PAIR         (state explicitly, always)
backing_type    : push back | screw back | lever back | hoop closure
drop_length_mm  : 0 for studs, else measured drop
carat_per_stone : 1.00CT each  (NOT total — state which)
total_carat_tw  : 2.00CT TW
```

## 3. THE BRIEF TEMPLATE — copy, fill, send
```
CATALOG BRIEF — [SKU]
category      : bracelet
source_cad    : cad/LCL-BRC-0007_4view.png
metal         : 14K yellow
listing_title : Round Lab Grown Diamond Paperclip Bracelet, 14K Solid Gold...
season        : festive
centre_stone  : n/a
accent_stones : Round, 0.45 TCW, 1.3mm, 22 pcs, bezel set
certification : IGI — certs/LCL-BRC-0007.pdf
length_in     : 7.0   (offered: 6.5 / 7.0 / 7.5)
clasp_type    : lobster
link_style    : paperclip
link_count    : 18
chain_gauge_mm: 2.4
adjustable    : yes, 1" extender
Slots        : full 10 + video, bracelet slot map (docs/20 §9.2)
Skip         : slot 9 (single metal listing)
Deliver      : config/deliveries/LCL-BRC-0007.json
```

## 4. RUN ORDER

**Before generating**
1. Load all policies (`13`, `03`, `04`, `20`, quality memory, failure memory, benchmarks)
2. Resolve `category` → preservation block + slot map. **Halt on unknown category** — never fall back to ring
3. Verify `metal` in the brief matches the karat in `listing_title`. **Halt on mismatch**
4. Verify `source_cad` and the certificate scan both exist on disk
5. Compute theme rotation from `sku` + `season`

**While generating**

6. Slots 1–3 on the locked white cotton cloth (`11` / `20` §4.0) — pools do not apply
7. Slots 4–5 use Pool A/B/C rotation
8. Slot 6 → scene only with a blank document plate; **the real cert is composited downstream, never generated**
9. Slots 7 / 9 / 10 pulled from the template asset library, not re-rendered
10. **Generation count per slot — see the OPEN COST ITEM below.** `17` currently governs: one image per angle, up to 2 attempts *on failure*.

**Before delivering**

11. Validate against source CAD, preservation policy, logo workflow, failure memory, benchmarks
12. Category-specific checks: earrings are a mirror-accurate pair · bracelet clasp present and correct type · necklace chain style unchanged · try-on body part matches category (`07` CATEGORY AUTO-REJECTS)
13. Reject internally and record any new failure with cause + prevention rule
14. Write the delivery JSON with `metal` and `category` pinned for reproducibility

> **⚠ OPEN COST ITEM — step 10.** The brief as written says *"generate `count: 2` per slot, keep the stronger frame."* `17` says the opposite in two places: line 22 "exactly one image per angle … max 2 attempts per angle" (an attempt is a **retry after a validation failure**, not a speculative pair), and line 92 "produce exactly the requested count … never generate throwaway drafts/tests." Speculative pairs double the credit line by design: 6 unique slots × 200 listings = 1,200 generations becomes 2,400. Until decided, `17` governs (strictest wins, `17` POLICY MERGE RULE). Pending user decision.

## 5. PER-CATEGORY GOTCHAS TO STATE EXPLICITLY
- **Ring** — state the depicted ring size. A 2CT stone reads differently on a size 4 vs a size 9 finger, and the try-on scale must match.
- **Bracelet** — state whether the length is inner circumference or end-to-end including clasp. These differ by ~1cm and it is the single most common bracelet return reason.
- **Necklace** — state whether `chain_length_in` includes the pendant drop. An "18 inch" necklace with a 15mm drop sits differently than a buyer expects if the drop was counted in.
- **Earring** — always write `quantity: PAIR` even when it seems obvious, and state whether carat is per stone or total weight. "2CT earrings" is ambiguous, and the ambiguity ends up in the listing title.
- **All** — `listing_title` is not decoration. It is the cross-check that catches metal, carat and category mismatches before a full set is rendered against the wrong spec. This is exactly the check that would have caught `BRACELET.json` rendering at 18K under a 14K title.

## 6. BATCH BRIEFS
For scaling to 200 listings, drive from a CSV rather than one brief at a time:
```csv
sku,category,metal,cut,carat,length_in,clasp,backing,season,cad_path,cert_path
LCL-RND-2CT-0142,ring,14K yellow,Round,2.00,,,,festive,cad/0142.png,certs/0142.pdf
LCL-BRC-0007,bracelet,14K yellow,Round,0.45,7.0,lobster,,festive,cad/0007.png,certs/0007.pdf
LCL-EAR-1CT-0031,earring,14K white,Round,1.00,,,push back,festive,cad/0031.png,certs/0031.pdf
```
One row = one catalog. The pipeline reads the row, resolves the category template, and runs. **Empty cells are only valid where the category does not use that field** — a bracelet row with an empty `clasp` must fail validation, not default silently.
