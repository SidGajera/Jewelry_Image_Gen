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

## RELATED
`docs/13_JEWELRY_PRESERVATION_SPEC.md` (Geometry Lock + QA checklist) · `docs/03 §A` (Design Preservation) · `prompts/07` (GEOMETRY LOCK header) · `config/QUALITY_MEMORY.json` (`zero-jewelry-invention`, `geometry-immutable-auto-fallback`) · `lib/pipeline/qc.py`.
