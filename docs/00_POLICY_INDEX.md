# 00 — POLICY INDEX (SINGLE SOURCE OF TRUTH — user-locked 2026-07-18)

This index is the **authoritative map**: exactly ONE owner doc/section per topic. Where any other document repeats or overlaps a topic, the OWNER below wins and the other mention is subordinate/historical detail. Load the owner before every relevant task; never act on a subordinate copy that conflicts with its owner.

| Topic | AUTHORITATIVE OWNER | Subordinate / see-also |
|---|---|---|
| Jewelry geometry / CAD preservation (D2D, prongs, gallery, band, per-angle) | **`13` JEWELRY PRESERVATION SPEC** (+ `16` zero-invention) | `03` §A, `18` §10 |
| Diamond rendering + clarity/appearance parity across all shots | **`03` DIAMOND CONSISTENCY POLICY** (master quality reference = office) | `03` §B, `18` §4 |
| Metal colour (18K yellow gold lock, reflections-only) | **`03` MASTER METAL COLOUR** | `03` §C LOCKED 18K GOLD, `18` §5 |
| Photorealism / anti-CGI | **`03` PHOTOREALISM POLICY — MASTER / ANTI-CGI** | `03` ULTIMATE PHOTOGRAPHIC REALISM |
| Cloth (premium pure-white cotton, weave, white balance, consistency) | **`11` MASTER CLOTH & LOGO PRESERVATION** + CLOTH VALIDATION | all earlier `11` cloth sections are subordinate; `18` §6 |
| Logo printing (embedded textile ink, jewelry-first, matte, artwork lock) | **`04` §14.1b MASTER FABRIC PRINTING** + §14.1c NATURAL CLOTH LOGO + §14.0 OFFICIAL LOGO LOCK | `04` §1–§15 subordinate; `11` LOGO VALIDATION; `18` §8 |
| Camera angle uniqueness (one image per angle, yaw/pitch/roll, camera memory) | **`12` MASTER CAMERA UNIQUENESS** (≤20% bar) | `18` §1–§3 |
| Lifestyle set (3 close-up + 4 close-framed; human model; geometry match) | **`03` LIFESTYLE SET COMPOSITION + HOUSE LIFESTYLE POLICY** | `03` LIFESTYLE GEOMETRY MATCH, `13` §4.1 |
| Pipeline (Higgsfield-only; CAD/Python banned) | **`15` §0 THE ONLY PIPELINE — HIGGSFIELD** | `project_named_pipelines` memory |
| Silent execution / token optimization / no-preview / one-sentence output | **`17` MASTER TOKEN OPTIMIZATION POLICY** | `05` token detail |
| Catalog consistency gate (pre-gen + final validation across the set) | **`18` MASTER CATALOG CONSISTENCY POLICY** | routes to owners above |
| Failure Memory + Quality Memory (all rejections, prevention rules) | **`07` QUALITY_MEMORY** (+ `config/QUALITY_MEMORY.json`) | `14` no-regression |
| Approval / commit / git workflow | **`03` CATALOG APPROVAL & LEARNING WORKFLOW** + `15` §8.5 CATALOG GIT RULE | `feedback_*` memory |
| Source fetch (SKU main folder only; gold default) | **`03` / `feedback_source_main_folder_only`** | per-catalog delivery record |
| Per-catalog delivery record (recipe, reference IDs, angle map) | **`config/deliveries/LR-XXXX.json`** | `15` §8 baseline |

**Precedence rule:** newest user-locked date wins within an owner; a "MASTER"/"ZERO TOLERANCE" section outranks an older general one on the same topic. Subordinate copies are retained for history and must not be edited to contradict their owner. When adding a new rule, append it to the OWNER only and, if needed, add a see-also pointer elsewhere — never duplicate the rule body.
