# 16 — ZERO JEWELRY INVENTION POLICY + JEWELRY DIFFERENCE DETECTOR

User-locked 2026-07-16, after a raw render invented a pavé bridge + gallery diamonds and redesigned the basket beneath the center stone (source had a plain open cathedral basket). This is the **invention** subtype of geometry drift: the model ADDS luxury details that do not exist in the source. Sits under P1 / docs/13 Geometry Lock; this file names the specific failure and the QC gate that catches it.

## ZERO JEWELRY INVENTION POLICY
The AI is strictly prohibited from adding, removing, or modifying any jewelry component that is not present in the source.

**Forbidden modifications (any one = reject):** additional accent diamonds · hidden halo · pavé bridge · diamond bridge · gallery diamonds · "surprise" diamonds · extra prongs · extra galleries · additional metal supports · decorative elements · filigree · split shanks · cathedral conversion · basket redesign · stone-count changes.

The source CAD/render is the absolute truth. **If a feature is not visible in the source, DO NOT create it.** Missing information must remain missing. Never "improve" the jewelry, never add luxury details, never redesign the setting.

**The only allowed changes:** environment · lighting · camera · perspective · human hand/model · depth of field · shadows · reflections. Everything belonging to the jewelry itself remains identical. (Same allow-list as docs/13 §2 / GEOMETRY LOCK — invention is the same violation as redesign.)

## JEWELRY DIFFERENCE DETECTOR (mandatory QC gate)
Before ANY image is accepted, compare the rendered jewelry against the source and check:
- **diamond_count** — same number of stones (no added accents / no removed stones)
- **diamond_locations** — every stone in the same place (no new pavé rows/bridge)
- **gallery_structure** — same gallery/basket architecture (no redesign)
- **prong_count** — same number + placement of prongs
- **hidden_halo_presence** — present iff present in source (never invented)
- **pave_bridge_presence** — present iff present in source (never invented)
- **metal_silhouette** — same overall metal outline / basket height / head-to-shank relation

**If any check differs → reject the image automatically, before delivery.** Never surface an invented-component render for approval.

### How it runs
Implemented as `lib/pipeline/qc.jewelry_difference_detector(render, source, from_composite)`, folded into `qc.qc_final` (every verdict carries `invention:*` checklist keys):
- **Composite render (composite-v1):** invention is IMPOSSIBLE — the ring is the real source pixels, so no component can be added/removed. Auto-pass. **This is the reliable fix: use the composite pipeline and invention cannot occur.**
- **Raw render (legacy):** needs a VISION diff vs the source — run it via Claude vision in the generation session (the operator/agent comparing render↔source, exactly the manual check that caught this failure) or `ANTHROPIC_API_KEY` when set. Until the vision diff runs, the raw render is **UNVERIFIED** and must NOT be auto-accepted (`invented: None`). Classical CV cannot reliably count stones or spot a pavé bridge, so this never fabricates a pass.

## HEAD & GALLERY GEOMETRY LOCK (user-locked 2026-07-16)
The center-stone assembly is the single most-invented region (added girdle/support rings, gallery rails, extra bridges, thicker heads) and is inspected SEPARATELY. Observed failure: a raw render added a thick circular metal support ring below the center stone, reshaped the gallery support arms, increased head thickness + metal volume, and re-seated the diamond — the source had a plain clean open basket. Not lighting — a different setting.

**The center-stone assembly is immutable. Preserve exactly:** prong count · prong thickness · prong angle · prong position · basket geometry · gallery geometry · bridge geometry · under-gallery · head height · head width · head thickness · metal volume · every opening and negative space.

**Strictly forbidden — never ADD:** extra support ring · girdle rail · gallery rail · hidden support · metal collar · extra bridge · additional basket · thicker head · invented gallery (e.g. a triangular/V-shaped gallery under the stone) · invented support arms · any additional structural metal. **Never fill or close the source's open/negative spaces.** If any metal appears that does not exist in the source, the render fails QC automatically.

Second observed failure (2026-07-16): source = open basket with curved support arms, NO gallery directly beneath the center stone, clean open side profile. Legacy render INVENTED a triangular/V-shaped gallery + extra metal support under the stone, changed the head/basket architecture — "no longer the same ring." Trips `head:gallery_shape` · `head:support_arms` · `head:under_gallery` · `head:no_invented_gallery` · `head:open_spaces_preserved`.

### HEAD GEOMETRY QC (dedicated check group)
The Jewelry Difference Detector inspects the head separately (`HEAD_GEOMETRY_CHECKS`, surfaced as `head:*` keys in `qc_final`): prong_count · prong_thickness · prong_angle · prong_position · basket_shape · gallery_shape · bridge_geometry · under_gallery · head_height · head_width · head_thickness · metal_volume · no_added_support_ring · no_added_gallery_rail · no_extra_bridge. Any mismatch → reject before delivery. Composite render = all pass (head is source pixels, invention impossible); raw render = UNVERIFIED until a vision diff runs (never a fabricated pass).

## COMPOSITE INTEGRITY (user-locked 2026-07-16)
Geometry preservation is necessary but NOT sufficient: a composite can carry the exact source ring (geometry_guaranteed=True) yet still be a failed image. Observed: compositing the source solitaire onto a studio scene that ALREADY contained a halo ring, with the source's soft drop-shadow left un-keyed — result read as failed AI inpainting: white mask/segmentation residue around the ring, the original halo ring peeking out behind the inserted solitaire (two rings), mismatched contact lighting/shadows.

**A composite must also pass these checks (reject immediately if any fails):**
- original_object_removed · single_ring_present · no_segmentation_artifacts · no_white_mask_residue · consistent_lighting_shadows · natural_background_integration.

**Root cause + fix (enforced, not detected after):** the failure comes from a DIRTY scene (already had a ring) + loose keying — so the guarantee is at the INPUT: composite ONLY into a **clean, ring-free scene** (empty cloth / bare finger), and key the source with a clean alpha (drop its background shadow). `qc.composite_integrity` HARD-FAILS `original_object_removed` + `single_ring_present` unless the caller asserts `scene_is_clean=True`; segmentation/residue/lighting/integration are vision/manual ("unverified" — classical CV can't reliably spot a soft white-mask patch; it reads like cloth highlights, so no pixel-detector is claimed). `qc_final` therefore no longer auto-passes a composite on geometry provenance alone — it stays geometry_guaranteed but `passed=False` until integrity is satisfied. The geometry regression suite (docs/14) still asserts the geometry invariant only; composite integrity is checked per-shot / shadow-test.

## RELATED
`docs/13_JEWELRY_PRESERVATION_SPEC.md` (Geometry Lock + QA checklist) · `docs/03 §A` (Design Preservation) · `prompts/07` (GEOMETRY LOCK header) · `config/QUALITY_MEMORY.json` (`zero-jewelry-invention`, `geometry-immutable-auto-fallback`) · `lib/pipeline/qc.py`.
