# 12 — STUDIO ANGLES + PHYSICAL REALISM (MANDATORY)

Locked standards (user-locked 2026-07-10/11). Apply to EVERY catalog's studio set. These add to — never override — P0–P8 in `docs/02_SYSTEM_RULES.md`.

## 0. STUDIO STARTING-POINT SEQUENCE (ABSOLUTE PRIORITY — locked 2026-07-11)
Every office/studio photoshoot MUST begin from the same approved studio setup, built in this exact order. This layered build order is the default starting scene for every studio image — the scene is prepared cloth→logo→jewelry, THEN photographed.
1. **BACKGROUND first — approved premium white cotton cloth** (permanent studio asset; never replaced, never AI-generated as a different fabric). Plain / naturally folded / softly draped — whichever looks most natural. Identical material, texture, weave, softness, finish, neutral premium-white color. Never yellow/cream/beige/pink/red/gray/blue tint or any warm cast. (docs/11)
2. **LOGO second — apply the preserved official logo AFTER the cloth is placed.** Never AI-generate/redraw/recreate/approximate; always the preserved asset, composited to look permanently printed INTO the cloth before the jewelry was photographed — following texture/weave/folds/perspective/lighting/shadows. May be fully visible / partially cropped / partly hidden by folds; never a watermark/floating overlay/sticker/AI text/digital graphic. (docs/04)
3. **JEWELRY third — place the ring only AFTER cloth + printed logo are correctly prepared.** The jewelry is the primary subject; cloth + logo are supporting branding. Ring 100% identical to source.
4. **PHOTOGRAPH last — shoot the completed scene with the approved studio setup.** Same camera height, distance, lens perspective, bright neutral lighting, luxury studio quality. Vary ONLY ring orientation, camera viewing angle, composition, and natural cloth folds.

**FINAL VALIDATION (every studio image):** ✓ approved premium white cloth used ✓ preserved official logo used ✓ logo naturally printed into cloth ✓ jewelry placed after background prep ✓ physics correct ✓ neutral white balance ✓ NO AI-generated logo ✓ NO AI-generated cloth. This sequence is mandatory for every office/studio photoshoot. (Practical pipeline: the Higgsfield render delivers the clean-cloth+ring intermediate; the preserved logo is composited locally per `docs/04` — the build ORDER and validation still govern the final deliverable.)

## A. STUDIO PHOTOSHOOT — THE 5 REQUIRED ANGLES
Every SKU's 5 studio images must be exactly these angles, so a customer can inspect the piece from every important side. Same locked white cloth + printed logo + identical lighting/exposure/white-balance across all five.

1. **Hero Front View** — straight-on hero shot; entire piece clearly visible; best e-commerce composition; maximum brilliance; premium luxury lighting.
2. **45° Left Front View** — rotate ~45° left; show center-stone depth; clearly display side stones, gallery and band; reveal setting height naturally.
3. **45° Right Front View** — opposite 45°; show the other side of the setting; display band profile and craftsmanship.
4. **Side Profile** — true side view; clearly show basket, gallery, prongs, hidden halo (if present), cathedral (if present), under-gallery, and side-stone setting; the customer should understand the ring's construction.
5. **Three-Quarter Perspective** — premium luxury angle showing top and side simultaneously; reveal the complete architecture; ideal for appreciating overall craftsmanship.

**General:** every important design detail must be visible across the five; never hide structural features; preserve exact geometry; no design modifications; identical lighting quality, exposure, reflections and white balance across all five; luxury e-commerce style.

## A1. CATALOG ANGLE DIVERSITY — ZERO TOLERANCE (user-locked 2026-07-17)
**Every catalog image MUST provide a unique viewpoint.** Never generate two images with the same or nearly identical: camera angle · camera rotation · camera height · camera distance · perspective · lens composition · ring orientation · subject framing.

**Before generating EACH image:** (1) compare against **every** image already generated in this catalog · (2) measure viewpoint uniqueness · (3) **if similarity exceeds 90% → reject internally** · (4) automatically choose a new camera position · (5) regenerate until the composition is clearly different.

**Duplicate examples (all rejected):** ✗ front 3/4 left + front 3/4 left slightly zoomed · ✗ front view + front view minor rotation · ✗ side view + side view with a different crop.

**A valid 12-image catalog maximises coverage, e.g.:** front · back · left profile · right profile · front-left 45° · front-right 45° · rear-left 45° · rear-right 45° · top detail · diamond close-up · hand lifestyle · additional lifestyle or detail.

**Changing only crop, zoom, focal length or cloth folds does NOT create a new angle. ANGLE UNIQUENESS is a mandatory validation step before approving any image.** (Where a required angle isn't supported by the SKU's CAD views, `13 §3.4` wins: shoot the closest supported angle or drop the slot — never invent geometry to fill it.)

### CAMERA VARIATION — ZERO TOLERANCE (user-locked 2026-07-17; applies to studio AND lifestyle)
Every catalog image must be **compositionally unique**. Changing only the hand pose, finger position, wrist rotation, crop or zoom **does not create a new image**. Before generating, compare against every previously approved image in the catalog and **reject immediately if substantially similar**.

**Must differ between every image:** camera height · camera distance · camera yaw · camera pitch · camera roll · lens focal length · subject framing · jewelry orientation · hand orientation · wrist orientation · finger arrangement · cloth folds (studio) · background composition · lighting direction · shadow pattern · depth of field · storytelling context.

**INVALID variations:** ✗ same front-left angle with a different finger pose · ✗ same side angle with a different crop · ✗ same composition with a different hand position · ✗ same hero angle slightly zoomed · ✗ same wrist angle with different finger spacing.

**VALID variations:** hero front (0°) · left three-quarter (35–45°) · right three-quarter (35–45°) · true profile (90°) · rear gallery · low-angle hero · high three-quarter hero · hand resting on sofa arm · hand holding a coffee mug · hand near face · hand on neck · hand holding a flower · hand holding a book · hand on a laptop · hand opening a door · hand by a window in natural light.

**If composition similarity exceeds ~20%, reject and regenerate with a completely different camera setup.** (20% bar, user-locked 2026-07-18; supersedes the earlier 25%/90% thresholds — strictest wins, `17` POLICY MERGE RULE.)

**MASTER CAMERA UNIQUENESS (user-locked 2026-07-18, global).** A new image is valid ONLY if the CAMERA ORIENTATION itself differs — changing only zoom/distance/crop/focal length, cloth folds, background or ring position does NOT create a new angle. Before approving, compare against every prior image on: camera yaw · camera pitch · camera roll · viewing direction · jewelry orientation · visible geometry · overall composition; reject if it matches (the `≤20%` composition bar below is the operative threshold; the standalone 80% figure is a floor). Keep a catalog-level CAMERA MEMORY: each approved image reserves its orientation; never reuse it later in the catalog. Assign each frame a distinct reserved viewpoint — straight front · front-left 3/4 · front-right 3/4 · left profile · right profile · rear · rear-left 3/4 · rear-right 3/4 · high angle · low angle · macro detail · lifestyle close-up — each used once. Lifestyle frames must also each be a genuinely new camera position (new finger angle/hand pose/ring orientation), not the same shot re-cropped. Recurrence 2026-07-18 (LR-0159): front-45, side and rear all rendered as the same upright three-quarter — reject and re-shoot at truly different yaw/pitch. Record duplicate-orientation failures in Failure Memory and block that orientation for the rest of the catalog.

**ONE IMAGE PER ANGLE + 20% SIMILARITY BAR (user-locked 2026-07-18).** Each distinct angle is delivered exactly ONCE per catalog; each required angle may appear ONLY once. Never output two images with substantially the same composition. Before generating each image, compare it against every previously approved image in the catalog on ALL of: camera height · camera yaw · camera pitch · camera roll · focal length · distance · framing · jewelry orientation · diamond presentation · overall composition. **If similarity exceeds ~20%, reject and regenerate** (this 20% bar supersedes the earlier 25%/90% thresholds — strictest wins, `17` POLICY MERGE RULE). A valid catalog assigns each frame a distinct named slot, e.g.: Hero Front · Front 45° · Left Profile · Right Profile · Rear 45° · Top Macro (high 3/4, never 90° overhead per CAMERA VALIDATION) · Finger Lifestyle · Coffee Lifestyle · Reading Lifestyle · Marble Lifestyle · Office Desk · Hand Close-up — never two frames of the same slot. Recurrence 2026-07-18 (LR-0163 grid): multiple frames repeated the same face-down and three-quarter angles.

### CAMERA VALIDATION — ZERO TOLERANCE (user-locked 2026-07-17)
**Never** position the camera directly above the ring (90° top-down) · never create an orthographic or CAD-style top view. Every camera angle must resemble a real professional jewelry photograph: the **diamond crown, prongs and band depth stay visible**, with realistic perspective and natural lens compression. **Prefer a slight front elevation (~15–35°) for hero images** unless the requested source angle specifically requires another viewpoint. Camera changes must never reduce visibility of the setting, gallery or diamond proportions.

**Automatic rejection — reject any render where:** the image looks like a CAD screenshot · the ring loses visible depth · the diamond appears flattened · the viewing angle is unnaturally top-down · the ring reads as a perfect circle because of an overhead viewpoint · the band hides behind itself · the perspective does not resemble a real luxury jewelry studio photograph.

*Observed (LR-0157, 2026-07-17): a 90° top-down flat-lay produced exactly this — unnaturally circular ring, flattened stone, setting depth gone, CAD-screenshot look. Angle uniqueness must be achieved with **yaw**, not by removing depth. Note: "top detail" in the coverage map means a HIGH ~60° three-quarter, never a 90° overhead.*

Every catalog must resemble a real professional jewelry photoshoot: each image a unique perspective, same studio setup.

**Unique camera angles — every image in a catalog has its own.** Never generate duplicate camera angles · nearly identical viewpoints · slightly rotated copies of the same shot · repeated compositions · repeated framing. Each image must contribute NEW visual information.

**Required catalog coverage** — collectively showcase the complete ring: front beauty · front three-quarter · left three-quarter · right three-quarter · left profile · right profile · head/top · gallery view · rear view · any additional unique artistic angle.

**Complete jewelry visibility** — the whole ring stays visible. Avoid: cropped ring · cut-off prongs · missing shank · missing basket · missing gallery · head hidden by framing · camera too close · ring extending outside the frame. The jewelry fits comfortably in frame while remaining the primary subject.

**Natural camera variation** — between images vary naturally: camera height · distance · yaw · pitch · roll (only if realistic) · ring orientation. No abrupt or unrealistic perspective jumps; transitions should feel like a photographer walking around the ring during the same session.

**Catalog validation (before approving a catalog):**
- [ ] No duplicated angle · [ ] no duplicated composition · [ ] every image contributes a new viewpoint · [ ] entire ring visible · [ ] jewelry is the primary subject · [ ] same studio setup · [ ] same background (docs/11 MASTER BACKGROUND LOCK) · [ ] same lighting · [ ] same logo placement rules (docs/04)

Reject any image that is visually redundant or fails to show the complete jewelry.

**MASTER RULE:** a customer should feel they are viewing ONE continuous professional photoshoot where every image reveals a different natural perspective of the same ring, without repetition.

**ANGLE DISTINCTNESS (MANDATORY — user-locked 2026-07-11):** the five studio shots must be FIVE VISIBLY DIFFERENT camera positions — no two may look like the same view. A recurring failure: hero, 45° left and 45° right all come out as near-identical near-front views. To prevent it, separate them by real camera geometry:
- **Hero front:** camera at ring height, straight-on, 0° yaw, ~0–5° top tilt.
- **45° left:** camera yawed ~45° to the LEFT of front AND raised to ~30–35° top-down — the setting clearly seen from the left-front above.
- **45° right:** camera yawed ~45° to the RIGHT AND raised ~30–35° — mirror of the left, clearly the other side.
- **Side profile:** true 90° side, camera at ring height — band/gallery/basket in pure silhouette, top of the stone NOT visible as a face.
- **Three-quarter:** high ~60° top-down at ~30° yaw — top and one side seen together.
Target ≥30–40° of yaw and/or pitch separation between any two studio shots. If two of the five read as the same angle, they are FAILED → regenerate the duplicate(s) at the correct distinct camera position. Distinctness applies to the CAMERA only; the ring itself stays byte-identical (see docs/03 §A).

## A1. PER-CATALOG ANGLE ROTATION + NATURAL-PHOTOGRAPHY REALISM (user-locked 2026-07-13)
Every catalog must look **freshly, naturally photographed** — never the same templated set, never "AI-generated / artificial." Two rules:

**(1) Vary the angles per catalog — don't reuse the previous SKU's exact camera setups.** §A's five roles (hero / two three-quarters / side / high three-quarter) still define WHAT must be covered, but the SPECIFIC camera geometry must ROTATE from one catalog to the next, and should include at least one or two *harder, more dynamic* angles so no two catalogs feel identical. Draw a different combination each SKU from a pool such as:
- steep bird's-eye ~75–85° straight down onto the table
- low near-table hero ~10–15° (worm's-eye), stone towering over the band
- over-the-shoulder three-quarter from behind the head looking forward
- raked/oblique macro with light skimming across the facets
- tight off-center crop with the ring in one third of the frame
- gentle natural camera tilt (a believable handheld feel, not a rigid dutch angle)
- profile with a slight 10–15° yaw (not a dead-flat 90°)
- high three-quarter from the opposite corner to the last catalog's
Keep the five mutually distinct (§A ANGLE DISTINCTNESS still applies: ≥30–40° separation). Rotating the set is what stops catalogs looking mass-produced. Track which setups the previous SKU used and deliberately pick different ones.

**(2) Make each frame read as REAL photography, not a render.** Emulate a human macro photographer, not a symmetrical CGI turntable:
- Natural, believable perspective and a real focal plane — genuine shallow depth of field with a soft, gradual falloff (a real point of focus, not everything uniformly razor-sharp).
- Centered, visually balanced composition — the ring sits centered horizontally and vertically (see §A2; supersedes the earlier off-center/rule-of-thirds guidance, user-locked 2026-07-15).
- Organic cloth arrangement — folds fall where gravity would really put them, never a tidy repeating pattern.
- Real-lens character: gentle light falloff toward the edges, believable specular highlights and soft shadow gradients, faint natural imperfection — not clinical, flat, plastic, over-even studio sterility.
- Bright neutral-white daylight still governs (docs/03 §E); this rule changes only the *camera craft*, never white balance, and never the ring geometry (byte-identical per docs/03 §A).
Avoid the AI tells: unnaturally even lighting, everything in focus, waxy over-smooth surfaces. If a shot looks artificial/rendered → regenerate with a more natural camera, focal plane, and composition. (Perfect centering is now REQUIRED, not an AI tell to avoid — see §A2.)

## A2. JEWELRY IS ALWAYS THE HERO (user-locked 2026-07-15, supersedes 2026-07-13 version)
The jewelry is the subject of every shot — studio, lifestyle and close-up. The viewer's eye must land on the ring within the first second.
- **Attention share:** the jewelry occupies **55–70%** of the viewer's visual attention; focus locks on the **center stone and ring**. Everything else is secondary support.
- **Position — CENTERED:** the ring is placed centered horizontally, centered vertically, and visually balanced in the frame. Never place it near the edges. (This replaces the earlier off-center/rule-of-thirds requirement.)
- **Frame it large:** the ring fills the composition prominently WITHOUT cropping important design details (prongs, gallery, side stones, band). No shrinking the ring into the frame; keep balanced margins and comfortable breathing room (professional luxury composition, not cropped tight).
- **Background is support only, softly blurred:** minimal and premium; background blur increases naturally with distance from the jewelry (real macro shallow DoF). The background must NEVER be sharper than the ring.
- **Camera priority order:** 1) jewelry, 2) diamond brilliance, 3) metal finish, 4) ring geometry, 5) background (lowest).
- **Never let the eye be pulled** to cloth, props, flowers, books, furniture, hands, or scenery. In lifestyle shots the hand/skin is a *stand*, not the subject — the ring stays the hero, framed large; NOT portrait-style hand photography.
- **Logo stays supporting:** the logo occupies only supporting space (see docs/04, position roughly consistent shot-to-shot; small camera-perspective drift OK, large position changes not) and must never approach the ring's visual dominance.
- **Forbidden:** busy backgrounds; distracting props; strong textures competing with the ring; large empty negative space; wide environmental shots; portrait-style framing where the hand is the subject; background sharper than the ring; off-center/edge-placed jewelry; any composition where the jewelry is not instantly the focal point.
- Every shot must immediately read as **"luxury jewelry product photography."** If the eye goes anywhere but the ring first, the ring isn't centered, or the background competes/out-sharpens the ring → regenerate.

## A3. GEOMETRY IS IMMUTABLE — AUTOMATIC FALLBACK WORKFLOW (user-locked 2026-07-13)
The final objective is **EXACT jewelry geometry with realistic luxury photography**. Jewelry geometry is immutable; AI may only change camera angle, composition, cloth, background, lighting, reflections, shadows, and depth of field. Never redesign, reinterpret, optimize, smooth, or reconstruct the ring. **Never ask the user which method to use — the fallback is automatic.**

Per SKU, per shot, run this ladder and stop at the first method that passes QC:
1. **AI generation, strict locked-geometry.** Feed the source images FIRST at max weight; prompt the hard CAD lock (only camera/scene changes). This is the default because it gives natural relighting and any camera angle.
2. **AUTO-QC vs source** (do not deliver until it passes): head; halo outer diameter + rim thickness; center-stone diameter + center-to-halo ratio; 4-prong positions/angles/size; halo stone count/spacing/diameter; shank width/thickness; shoulder→head transition; cathedral/gallery architecture; metal thickness; diamond proportions; every contour/silhouette.
3. **If ANY geometry differs → do NOT deliver; fall through automatically:**
   - **Fallback 1 — composite the real ring.** Preserve the ORIGINAL jewelry exactly: cut the source-ring pixels and composite them into the AI-generated scene (`scripts/composite_ring_into_scene.py`), matching lighting, shadows, reflections, perspective, DoF and color. Geometry is then 100% identical (they are the source pixels). Limited to the angles the source provides; best for studio (flat) shots.
   - **Fallback 2 — render from CAD.** If compositing cannot achieve the requested camera angle, render the exact geometry at that angle from the original CAD model (only when the CAD file is available), then composite onto cloth.
   - Never deliver a regenerated ring whose geometry changed.

**QC pass bar (all must hold):** ✔ 100% geometry match ✔ natural macro photography ✔ bright neutral-white daylight ✔ physically realistic reflections ✔ logo physically printed into the fabric ✔ camera angles varied across catalogs ✔ focus always on the jewelry.

> Honest note kept in-repo: nano_banana biases toward the CAD but cannot guarantee <1% geometry; that is *why* the fallback ladder exists. Compositing (Fallback 1) is the in-pipeline route to true 0% drift.

## B. PHYSICALLY ACCURATE RING + CLOTH POSITIONING
Every pose, fold, wrinkle, shadow and contact point must be physically realistic and achievable in a real studio — not CGI, not an impossible AI composition.

### Ring physics
- Gravity acts naturally; the ring's center of mass is properly supported on real contact points with the cloth.
- Never float, hover, sink, clip through fabric, or balance impossibly.
- Upright/tilted poses ONLY when a believable cloth fold physically supports the ring.
- Shank, center stone, setting, gallery, side stones stay rigid and undeformed — no stretch/bend/twist/proportion change.
- Contact shadows appear exactly beneath the true contact areas; orientation is stable under real gravity.

### Cloth physics
- Behaves like real premium soft white fabric; folds form naturally from gravity, compression, tension, support; every raised fold has a believable cause.
- Wrinkles flow continuously (don't stop/merge/bend unnaturally).
- Cloth compresses only slightly under the ring's light weight — no deep deformation; folds never pass through the ring or gemstones.
- Never frozen/liquid/plastic/inflated/geometrically impossible; shadows and highlights follow each fold's true direction and depth; thickness/softness/texture/drape consistent throughout.

### Ring–cloth interaction
- Ring and cloth share one physical scene: contact points, pressure, shadows, occlusion, perspective all match.
- Leaning against a fold → that fold visibly and logically supports it. Standing upright → base + surrounding fabric make it stable. Lying flat → shank rests naturally on the surface.
- No penetration/merging; cloth reacts subtly, not exaggeratedly.

### Logo on cloth (physics)
- The printed logo follows the same physically correct cloth surface: bends/warps naturally with folds and perspective; may be fully visible, partially hidden, or naturally cropped; never floats above the cloth or stays unnaturally flat across deep folds. Preserve the exact official artwork and color. (Composited locally per `docs/04_LOGO_WORKFLOW.md`; the print script's fold-displacement + brightness-modulation delivers this.)

### Final physics check (verify before accepting each image)
✓ center of mass supported ✓ pose stable/achievable ✓ gravity consistent ✓ folds have believable causes ✓ deformation matches light weight ✓ contact points/shadows match ✓ no floating/clipping/penetration/impossible balance ✓ logo follows cloth surface ✓ lighting/perspective/shadows/reflections agree. If any fails → correct before final output.
