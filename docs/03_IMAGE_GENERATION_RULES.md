# 03 — IMAGE GENERATION RULES

Complete rules for every generated image.

## HIGH PRIORITY — JEWELRY-FIRST PHOTOGRAPHY STANDARD (CRITICAL, user-locked 2026-07-17)
**Priority: CRITICAL — higher than scene styling and artistic composition.** The jewelry is always the hero; the environment exists only to support it, never to compete with it. (Ranks below the ABSOLUTE jewelry-preservation rule, `docs/02`.)

**UNIQUE BRAND IDENTITY** — do not imitate common Etsy, Pinterest, Amazon or competitor photography styles; avoid clichéd compositions widely used across online marketplaces. Establish a unique **Lucent Carat Lab** visual identity — recognisable premium photography rather than following trends.

**JEWELRY IS THE HERO** — every composition must immediately draw the eye to the jewelry within the first glance. The environment complements, never becomes the focal point. Avoid: busy scenes · heavy decorations · large props · distracting backgrounds · visual clutter · oversized furniture · strong textures competing with the ring · lifestyle elements dominating the frame.

**NATURAL PHOTOGRAPHY** — every image must resemble a genuine high-end luxury jewelry photograph. Maintain: real camera perspective · real optical behaviour · realistic depth of field · natural lens compression · natural shadows · natural reflections · natural fabric interaction · natural skin texture (when applicable) · natural diamond optics · real gold reflections. Avoid: AI artifacts · CGI appearance · plastic materials · unrealistic blur · artificial HDR · over-sharpening · excessive bloom · unrealistic symmetry · impossible lighting. **The final image must be indistinguishable from a professionally captured photograph.**

**CATALOG THEME LOCK** — the first approved image defines the MASTER THEME; every remaining image preserves the same photography style · environment · mood · lighting · background family · prop family · colour neutrality · overall visual identity. Only viewpoint and composition may change naturally.

**SUBTLE SCENE DESIGN** — scenes feel authentic and understated; props support the story while remaining visually secondary; the environment communicates luxury without distracting from the jewelry.

**MASTER VALIDATION — before approving every image ask:** (1) Is the jewelry unquestionably the first thing the viewer notices? (2) Does the environment support rather than dominate it? (3) Does this avoid common marketplace clichés? (4) Does it look like a real luxury product photograph? (5) Would a professional photographer believe it was captured with a real camera rather than generated? (6) Does it maintain the approved catalog theme? **Any NO → reject internally · record in `07_QUALITY_MEMORY` · regenerate.**

**MASTER PRIORITY RULE** — the primary objective of every generated image is to showcase the jewelry in the most natural, luxurious and believable way possible. Every catalog must establish a consistent premium visual identity unique to Lucent Carat Lab, so natural that the photographs are visually indistinguishable from genuine professional jewelry photography.

### ULTIMATE PHOTOGRAPHIC REALISM STANDARD (HIGHEST PRIORITY — NON-NEGOTIABLE, user-locked 2026-07-17)
**This rule overrides all artistic rendering preferences.** Target the visual quality of genuine high-end luxury product photography. **The objective is never to look "AI-generated" — it is to be visually indistinguishable from a genuine luxury jewelry photograph captured with professional photographic equipment.** Every decision during generation must favour PHYSICAL REALISM over AI-style rendering.

**REAL PHOTOGRAPH STANDARD — every image must exhibit:** physically correct lighting · physically correct shadows · physically correct reflections · real camera optics · natural depth of field · natural lens perspective · realistic material behaviour · natural skin texture (if present) · natural fabric texture · natural gold reflections · natural diamond optics · natural micro-details · professional photographic exposure · neutral white balance.

**STRICTLY PROHIBITED — reject immediately if the image exhibits:** CGI appearance · AI-style rendering artifacts · plastic-looking materials · artificial bloom · unrealistic HDR · over-sharpening · over-smoothed textures · repeating patterns · hallucinated geometry · impossible reflections · impossible shadows · synthetic-looking diamonds · synthetic-looking fabric · any visually implausible artifact.

**REALISM VALIDATION (before approval):**
- [ ] Image matches professional luxury jewelry photography · [ ] materials behave realistically · [ ] lighting physically plausible · [ ] shadows physically plausible · [ ] jewelry appears physically manufactured · [ ] cloth appears physically photographed · [ ] logo appears physically printed · [ ] no obvious synthetic visual artifacts

**Any validation failure → reject internally · record the failure in `07_QUALITY_MEMORY` · regenerate.**

**MASTER RULE** — every delivered image must achieve the visual standard of genuine high-end commercial jewelry photography. The system must continuously optimise for photographic realism **while preserving the jewelry exactly as defined by the source CAD and all locked preservation policies** (`02`, `13`, `16`).

**PHOTOREALISM POLICY (HIGHEST PRIORITY — user-locked 2026-07-17).** Every generated image must be **visually indistinguishable from a professional luxury jewelry photograph captured with a high-end full-frame camera and premium macro lens**. The objective is MAXIMUM PHOTOREALISM.

*Every image must exhibit:* physically accurate lighting · natural global illumination · correct optical reflections · real lens behaviour · authentic depth of field · realistic micro-contrast · natural colour response · real fabric physics · real metal reflections · physically accurate diamond optics · **real-world imperfections** · subtle manufacturing tolerances · natural camera noise where appropriate.

*Lifestyle images additionally:* natural skin texture · individual pores · fine peach fuzz · natural lip texture · realistic eyelashes · natural eyebrows · correct eye reflections · realistic hair strands · natural finger anatomy · authentic nail texture.

*Never:* CGI appearance · over-sharpening · plastic surfaces · waxy skin · synthetic-looking diamonds · repetitive patterns · AI artifacts · unrealistic symmetry · hallucinated geometry.

**Every model must look like a real luxury-campaign model photographed by a professional fashion photographer; every jewelry image must look like genuine commercial product photography from a luxury jewelry brand. Prioritise REALISM OVER STYLIZATION — if any rendering choice makes the image look synthetic, artificial or computer-generated, reject and regenerate.**

**Detail (subordinate to the above):**

**REAL CAMERA STANDARD** — every image must be consistent with a real camera capture: natural perspective · realistic lens behaviour · natural depth of field · correct optical focus falloff · real exposure · real white balance · natural dynamic range · realistic reflections · natural shadow transitions · real fabric interaction · real metal behaviour · real diamond light performance. **Never simulate unrealistic camera effects.**

**REAL MATERIAL STANDARD** —
· **Gold:** natural reflections · correct polish · no plastic appearance · no artificial glow.
· **Diamond:** realistic brilliance · natural fire and scintillation · correct transparency · no overexposed white areas · no unrealistic sparkle effects.
· **Cloth:** premium cotton · natural weave · real fibre texture · soft natural sheen · physically correct folds.
· **Skin (if present):** natural pores · natural texture · realistic lighting response · never waxy or over-smoothed.

**NO ARTIFICIAL RENDERING — reject immediately on:** CGI appearance · plastic-looking materials · unrealistic reflections · impossible shadows · artificial bloom · excessive HDR · over-sharpening · over-smoothed surfaces · repeating texture artifacts · symmetry artifacts · distorted geometry · hallucinated details · any other visually implausible rendering artifact.

**REAL PHOTOGRAPH VALIDATION (before approval):**
- [ ] Lighting physically plausible · [ ] shadows physically plausible · [ ] material responses physically plausible · [ ] camera perspective physically plausible · [ ] jewelry interactions physically plausible · [ ] background interactions physically plausible · [ ] no obvious rendering artifacts · [ ] overall appearance matches professional luxury jewelry photography

**MASTER RULE** — every delivered image must be indistinguishable, to a reasonable viewer, from a professionally captured luxury jewelry photograph taken with a real camera under controlled photographic conditions. If an image contains obvious synthetic or implausible artifacts → reject · record the specific failure in `07_QUALITY_MEMORY` · regenerate.

## GENERATION ORDER (LOCKED — run for every image)
1. Load `13_JEWELRY_PRESERVATION_SPEC`.
2. Load `07_QUALITY_MEMORY` (Approved Benchmarks + Failure Memory; store = `config/QUALITY_MEMORY.json`).
3. Load `04_LOGO_WORKFLOW`.
4. Load `03_IMAGE_GENERATION_RULES`.
5. Validate all loaded policies.
6. Load 4-view CAD (single source of truth).
7. Load cached Design Profile (`06_CACHE`).
8. Generate image.
9. Validate against: Source CAD · Jewelry Preservation Spec · Physics & Logical Validation · Failure Memory · Approved Benchmarks · Logo Workflow · Cloth Standard.
10. Reject internally if any validation fails.
11. Record every new failure in `07_QUALITY_MEMORY` (Failure + Cause + Prevention Rule).
12. Deliver only after all validations pass.

The workflow, policies and validation sequence are **LOCKED**. Improve only by adding new Failure Memory rules and enforcing these validations more strictly. All steps run silently (`docs/17`).

### ONE-TIME PERMISSION (user-locked 2026-07-17)
Once the user supplies the source files (CAD/references/logo/approved assets) and requests generation, that is ONE-TIME authorization to complete the requested image set — never ask permission before each image or after each regeneration. During an active session: generate all requested images, validate every image, reject failures internally, regenerate automatically, update Failure Memory on each rejection, never interrupt unless input is genuinely required. Authorization ends when: the user changes the design · uploads a new CAD · uploads new references · changes workflow/policies · explicitly pauses/stops · the task completes. Ask ONLY when: a required source asset is missing · the CAD/reference is ambiguous · a requested change conflicts with locked policies · the user starts a different project. Scope: current task only.

**PERMISSION POLICY — CONNECTORS & MEDIA (user-locked 2026-07-17).** Obtain all required connector permissions at the START of the session. **Never interrupt the workflow to request repeated permissions.** Reuse existing authenticated sessions (Higgsfield, Drive, GitHub). **Reuse uploaded media whenever possible — never re-upload identical source files**; reuse each `media_id` (cloth, logo, CAD, approved masters) until it expires (`06_CACHE`, `17` OPERATIONAL NOTES). Request additional permission ONLY when a completely new connector or a new permission scope is genuinely required. **The generation workflow must continue without repeated approval dialogs whenever technically possible.**

### MANDATORY PRE-DELIVERY VALIDATION
**A. SOURCE CAD (only camera angle may change):** overall geometry · ring proportions · band width · band thickness · ring profile · head · gallery · basket · cathedral · bridge · setting · prongs · prong count · prong thickness · prong position · centre diamond · pavilion · crown · table · side diamonds · pavé · metal — ALL unchanged.

**B. JEWELRY PRESERVATION (reject immediately on any):** geometry drift · invented geometry · missing metal · added metal · missing diamonds · added diamonds · wrong proportions · wrong setting · wrong head · wrong basket · wrong gallery · wrong bridge · wrong cathedral · wrong prongs · wrong diamond shape · wrong diamond orientation. (Owner: `docs/13`, `docs/16`.)

**C. PHYSICS & LOGICAL.** *Head & stone support:* centre diamond physically supported; never floating; girdle visibly seated inside the setting; pavilion naturally supported by the head; crown/girdle/pavilion align with the setting. *Prongs:* every prong visibly contacts AND wraps over the girdle; no gaps; prongs originate naturally from the head; mechanically capable of retaining the stone. *Load path — visually continuous, no interruption or unsupported transition:* `Centre Diamond → Prongs → Setting Head → Basket → Gallery → Bridge → Shank`. *Manufacturing:* realistically manufacturable; stone retained after setting; metal thickness structurally believable; setting capable of supporting the shown diamond; no impossible/unstable geometry. *Visual physics:* gravity respected; no unsupported mass; no floating components; no impossible contact surfaces; metal↔diamond connections believable.
**PHYSICAL CONTACT VALIDATION (user-locked 2026-07-17).** Every object must obey gravity and **physically interact with the cloth**. Always verify: the cloth **compresses under the ring** · fabric folds respond naturally to the ring's weight · contact shadows originate from the TRUE contact points and match the lighting direction · **ambient occlusion** appears beneath the ring · the ring never appears to float. **Reject and regenerate if the ring appears unsupported or the cloth lacks realistic deformation.** (Observed on LR-0156: the ring rested on the cloth with too little compression, too light a contact shadow and no local fabric deformation.)

**MASTER PHYSICS QUESTION (before approving every image):** *"If this exact ring were manufactured in real gold using the shown geometry, would the centre diamond remain securely held under normal wear without relying on hidden or impossible support?"* Anything other than YES → reject internally · record the failure · regenerate.

**D. LOGO (owner: `docs/04`):** official logo only · no AI recreation · correct typography · correct diamond icon · correct colours · correct gradients · correct spacing · correct alignment · correct perspective · correct opacity · naturally printed on premium white cotton · follows cloth folds · no sticker effect · no floating logo · no embossing · no white box.

**E. CLOTH / BACKGROUND (owner: `docs/11`):** premium plain white cotton · natural weave · natural folds · natural shadows · correct perspective · no artificial texture · no colour shift · **MASTER BACKGROUND LOCK + master validation question** per `docs/11`.

**F. INDIVIDUAL IMAGES ONLY (user-locked 2026-07-17).** Each catalog image is an INDEPENDENT full-frame high-resolution render, exported independently, identical studio quality, locked background + locked logo. **Never generate** a contact sheet · thumbnail grid · gallery preview · multi-image board · collage · comparison board · batch overview · catalog sheet · mosaic · storyboard · composite image. **Reject immediately** if an output contains multiple rings in one image · multiple camera views in one image · thumbnail/gallery/grid layout · contact sheet · preview page · image board · composite render. Deliver only the requested individual images; never generate or display group previews unless the user explicitly requests a contact sheet or comparison board.

**G. FINAL REALISM VALIDATION (user-locked 2026-07-17 — run last, before approving ANY render):**
- [ ] Cloth is pure neutral white premium cotton
- [ ] No warm, cream, beige, yellow, blue, grey or magenta colour cast
- [ ] Logo is physically printed INTO the cotton fibres
- [ ] Logo follows the fabric weave, folds, perspective and lighting
- [ ] Logo edges inherit the same softness as the cloth
- [ ] Logo never appears pasted, overlaid, floating or digitally composited
- [ ] Gold reflects the real environment naturally, without artificial glow
- [ ] Diamonds show physically accurate refraction and dispersion with realistic internal reflections
- [ ] Every visible surface resembles a professionally photographed real ring rather than a CGI render

Any unchecked item → reject internally · record in `07_QUALITY_MEMORY` · regenerate. (Detail owners: cloth `11` · logo `04` · realism `03` ULTIMATE PHOTOGRAPHIC REALISM · diamonds `13 §3.1`.)

### MANDATORY POLICY EXECUTION (ZERO TOLERANCE — user-locked 2026-07-17)
**Before generating ANY image, ALL loaded policies are MANDATORY and OVERRIDE every default behaviour of the image model.** The renderer MUST execute every policy exactly as written.

**The renderer is NOT allowed to:** ignore any policy · partially follow any policy · balance one policy against another · override a policy using learned priors · replace policy instructions with its own assumptions · simplify policy instructions · interpret policy instructions creatively.

**Every policy is a HARD CONSTRAINT. If ANY policy conflicts with the model's learned behaviour, the POLICY ALWAYS WINS.** The renderer has NO authority to modify, reinterpret, optimise, redesign, beautify, reconstruct, hallucinate or substitute any part of the **jewelry, logo, cloth, environment or approved workflow**.

**The renderer's authority is LIMITED ONLY to:** camera angle · camera distance · camera lens · camera height · camera rotation · studio lighting · exposure · focus · depth of field · environment lighting. **Everything else stays exactly as the loaded policies define it.**

**Generation is NOT permitted until ALL required policies are successfully loaded and validated.**

**GENERATION ORDER:** (1) load every required policy · (2) validate every policy · (3) validate against **Failure Memory** · (4) validate against **Approved Benchmarks** · (5) build prompt · (6) generate image · (7) post-generation validation · (8) reject immediately if ANY policy is violated · (9) record every failure into Failure Memory · (10) regenerate until every policy passes.

#### POLICY EXECUTION ENGINE (context-aware loading — user-locked 2026-07-17)
The policy system is **context-aware**: do NOT load every policy for every generation. Load ONLY the policies the current task requires — the workflow determines them from the requested image type. This cuts processing without reducing quality (`17` lazy-load).

**ALWAYS LOAD (mandatory for every jewelry generation):** MASTER JEWELRY PRESERVATION (`13` — incl. §3.3 CAD LOCK MODE, §4.0/§4.1 D2D) + `16` · **QUALITY_MEMORY** (`07` + `config/QUALITY_MEMORY.json` — Approved Benchmarks + Failure Memory).

**LOAD CONDITIONALLY, only when applicable:** studio images → `12` STUDIO · house lifestyle → `03` HOUSE LIFESTYLE POLICY · office lifestyle → `11` OFFICE PHOTOSHOOT · white-cloth scene → `11` CLOTH · logo visible → `04` LOGO · human model appears → `03` MODEL REALISM · different camera angle → `12` CAMERA/ANGLE DIVERSITY · multiple jewelry pieces → MULTI-PRODUCT · packaging → PACKAGING · video generation → VIDEO. **Do NOT load policies unrelated to the requested output.**

**POLICY PRIORITY when several are active:** 1. MASTER JEWELRY PRESERVATION (highest authority) · 2. QUALITY_MEMORY · 3. scene policy · 4. camera policy · 5. logo policy · 6. cloth policy · 7. model policy · 8. rendering guidelines. **A lower-priority policy may NEVER override a higher-priority one.**

**CONFLICTS:** MASTER JEWELRY PRESERVATION always wins · QUALITY_MEMORY overrides previously failed behaviour · scene-specific policies apply **only after geometry is preserved**.

**Generate only after all required policies are active. Never use unnecessary policies; never skip a required one. Use the MINIMUM required policy set while holding 100% compliance with jewelry preservation and Failure Memory. The generator must FOLLOW every active policy during generation — not merely reference them beforehand.**

**The image MUST NOT be delivered unless ALL policies pass 100%. Failure of even ONE policy = automatic rejection.**

Every generation MUST strictly enforce every loaded policy before, during and after generation. **Policy loading alone is not sufficient** — the system must actively VALIDATE every generated image against every applicable policy before delivery.

**Sequence:** (1) load all required policies · (2) validate that all required policies loaded successfully · (3) generate · (4) execute EVERY validation defined in EACH loaded policy · (5) on any failure → reject internally, record in `07_QUALITY_MEMORY`, regenerate automatically · (6) repeat until every validation passes · (7) deliver only images that pass all policy validations.

**Strict compliance:** no policy may be ignored · no validation may be skipped · no rule is optional. When multiple policies apply, ALL must pass simultaneously. Where two policies overlap, enforce the **stricter** requirement.

**VALIDATION ORDER:**
1. Jewelry Preservation Spec (`13`)
2. Zero Jewelry Invention (`16`)
3. Physics & Logical Validation (§C above)
4. Background Standard (`11`)
5. Studio Angles Standard (`12`)
6. Logo Workflow (`04`)
7. No Regression Policy (`14`)
8. QUALITY_MEMORY — Failure Memory + Approved Benchmarks (`07`)
9. Image Generation Rules (this file)

Only if EVERY validation passes may the image proceed to delivery.

**FINAL DELIVERY GATE:** deliver ONLY if ALL pass — Source CAD · Jewelry Preservation · Zero Invention · Physics & Logical · Background · Studio Angles · Logo · No-Regression · Failure Memory · Approved Benchmarks · Individual-image. Any single failure → reject internally · record in `07_QUALITY_MEMORY` (Failure + Cause + Prevention Rule) · regenerate. An image cannot be delivered if any policy reports a failure. **Never rely on manual review for failures already covered by an existing policy — all such failures must be detected automatically through policy validation.**

**MASTER RULE: policy compliance is mandatory, not advisory. Every delivered image must satisfy 100% of all loaded policies.**

### STRICT POLICY ENFORCEMENT ENGINE (user-locked 2026-07-17)
**Policies are executable validation rules, not reference documents.** Every image must satisfy every applicable policy before it can be delivered.

**Mandatory pre-generation check:** (1) load every required policy · (2) verify every required policy loaded successfully · (3) verify no policy is skipped · (4) load QUALITY_MEMORY · (5) load Approved Benchmarks · (6) load Failure Memory · (7) load Source CAD · (8) compare the generation request against every policy · (9) apply every recorded prevention rule. **If any required policy is unavailable or not validated → STOP generation immediately.**

**Mandatory during generation:** continuously enforce every applicable policy · no policy ignored · no validation bypassed · **no conflicting instruction may override a locked policy.** When multiple policies apply: evaluate ALL of them · enforce the STRICTEST requirement · preserve all locked assets.

**Mandatory post-generation validation:** run every validation defined by every active policy. Validation is complete only when EVERY policy returns PASS. If any policy returns FAIL: reject internally · do not deliver · identify the exact failed rule · record in `07_QUALITY_MEMORY` · strengthen the existing prevention rule if necessary · regenerate · repeat the COMPLETE validation cycle.

**ZERO-TOLERANCE RULE:** a single failed validation is sufficient to reject the image. Never deliver an image that only partially complies. **PASS = every policy passes. FAIL = entire image rejected.**

**Continuous learning:** every rejection updates QUALITY_MEMORY · strengthens future validation · prevents recurrence. Every approval reinforces Approved Benchmarks · preserves successful patterns · improves future generations.

**MASTER RULE — enforcement stays active:** ✓ before generation ✓ during generation ✓ during validation ✓ during regeneration ✓ before delivery ✓ after user feedback ✓ throughout the entire catalog. **No image may bypass policy validation at any stage.**

### BEFORE / DURING / AFTER ENFORCEMENT (user-locked 2026-07-17)
Enforcement is CONTINUOUS and cannot be skipped at any stage: **before generation → during generation → after generation → during regeneration → before final delivery → after user feedback.**

**BEFORE generation:** (1) load all required policies — `13`, `07`, `04`, `03` + every other applicable locked standard · (2) confirm every required policy is available and active · (3) load the 4-view source CAD, cached Design Profile, Failure Memory and Approved Benchmarks · (4) check the complete request against every policy · (5) apply every previously recorded prevention rule BEFORE generating · (6) **do NOT begin** if any required policy is missing · any source asset is missing · any instruction conflicts with locked policies · historical failure-prevention rules have not been applied.

**DURING generation:** preserve the source jewelry exactly · enforce all active policies continuously · prevent every recorded historical failure · never invent or modify jewelry geometry · maintain locked logo, cloth, background, lighting and catalog standards · keep every catalog angle unique and physically realistic · do not ask repeated permission during the same approved task (one-time permission above).

**AFTER generation:** immediately validate every output against — (1) Source CAD · (2) Master Jewelry Preservation · (3) Zero Jewelry Invention · (4) Physics & Logical · (5) Logo Workflow · (6) Background Standard · (7) Studio Angles Standard · (8) No Regression Policy · (9) Failure Memory · (10) Approved Benchmarks · (11) Image Generation Rules. If ANY single rule fails: reject internally · do not deliver · identify the exact failure · identify the root cause · add the learning to `07_QUALITY_MEMORY` · add or strengthen the appropriate prevention rule · regenerate automatically · **validate again from the beginning.**

**USER FEEDBACK LEARNING:** every user correction/rejection after delivery is new learning. Record: what was wrong · which component failed · why it occurred · which EXISTING policy should contain the correction · the prevention rule · the expected correct output. **Do not create a duplicate policy** — merge the learning into the existing relevant policy and update `07_QUALITY_MEMORY` (see `17` POLICY MERGE RULE).

**NO-REPEAT RULE:** before every future generation — load all recorded failures · compare the new generation against every past failure · prevent identical AND substantially similar mistakes · preserve all previously approved corrections. The same identified mistake must not be repeated.

**FINAL DELIVERY GATE — deliver only when:** ✓ all policies checked before generation · ✓ all policies enforced during generation · ✓ all policies passed after generation · ✓ no recorded failure repeated · ✓ all new learnings recorded correctly. Otherwise: **Reject → Learn → Update QUALITY_MEMORY → Regenerate → Revalidate.**

### CATALOG IMAGE STANDARD (user-locked 2026-07-17)
Generate ONE catalog at a time: **Office Photoshoot (5) → House Lifestyle (7)**.

**CATALOG 01 — OFFICE PHOTOSHOOT · 5 images.** Purpose: professional product photography for Etsy, website, marketing, brand identity.
Required views (each unique): 1. Front Beauty (Hero) · 2. Front Three-Quarter · 3. Side Profile · 4. Rear / Gallery View · 5. Artistic Hero Angle.
Rules: same premium pure white cotton cloth · same naturally printed preserved logo · same neutral lighting · same white balance · same exposure · same studio environment · same photographic theme · every angle unique · complete jewelry visible · no duplicated composition · natural professional photography only. (`11` background lock, `12` angle diversity, `04` logo.)

**CATALOG 02 — HOUSE LIFESTYLE · 7 images.** Purpose: natural luxury lifestyle marketing.
Lifestyle (4): 1. Elegant living room / coffee table · 2. Luxury bedroom / vanity setup · 3. Window daylight lifestyle · 4. Luxury home décor composition.
Natural close-up (3): 5. Natural close-up beauty shot · 6. Natural close-up side angle · 7. Natural close-up artistic detail.
Rules: preserve jewelry exactly · natural home environment · natural daylight · natural shadows · neutral colour balance · no artificial props · no AI-looking environment · no artificial colour grading · each image a unique composition.

**HOUSE LIFESTYLE POLICY (LOCKED — user-locked 2026-07-17):**
- **Every House Lifestyle catalog features a realistic HUMAN MODEL WEARING the jewelry.**
- The **jewelry remains the primary subject**; the model supports the presentation rather than becoming the focus (`03` JEWELRY-FIRST).
- **One consistent home environment across the entire lifestyle catalog** — never mix indoor/outdoor or different home styles (`03` CATALOG THEME CONSISTENCY).
- Natural, high-end residential lighting and authentic poses.
- **Preserve the jewelry D2D exactly** — no geometry, diamond, prong or setting changes (`13 §4.1`).
- The overall result must look like a professional luxury jewelry photoshoot (`03` ULTIMATE PHOTOGRAPHIC REALISM). Hands/skin: natural pores and texture, realistic lighting response, correct anatomy — never waxy or over-smoothed.

**LOCKED MODEL REALISM POLICY (user-locked 2026-07-17).** Use **100% photorealistic human models** in all lifestyle images — they must look captured in a professional luxury jewelry photoshoot.
**Preserve:** natural skin texture and pores · realistic anatomy and proportions · natural facial expressions · realistic hands and fingers · natural hair · authentic clothing folds and fabric · soft, physically accurate lighting and shadows · natural depth of field.
**Avoid any CGI or AI-looking characteristics:** overly smooth or plastic skin · unnatural eyes · incorrect finger anatomy · artificial poses · over-processed lighting or skin · any visual cue that makes the model read as computer-generated.
**The jewelry remains the primary focus** — the model serves to showcase it naturally. Applies together with the locked standards for CAD fidelity (`13`), cloth (`11`), logo printing (`04`), consistent 18K gold (`03 §C`), catalog theme consistency and overall photographic realism. Any failure → reject internally · record in `07` · regenerate.

**After each catalog:** validate every image · record user corrections · learn from approvals and failures · update `07_QUALITY_MEMORY` · preserve successful patterns · prevent repeated mistakes · commit the final approved catalog · push to Git · proceed to the next catalog.

#### CATALOG THEME CONSISTENCY (user-locked 2026-07-17)
Every catalog represents ONE continuous professional photoshoot with a single visual theme. **A catalog must never mix environments or photography styles.**

**THEME LOCK** — the first approved image defines the MASTER THEME for the entire catalog; it becomes a locked reference. Every remaining image preserves the same: environment · photography style · lighting style · background style · props · mood · white balance · colour tone · camera style. **Only camera angle, camera distance, ring orientation and composition may change naturally.**

**Office photoshoot** — if the first image is an office photoshoot, every remaining image stays an office photoshoot. Never introduce: home environment · outdoor · garden · bedroom · kitchen · café · marble lifestyle · nature · any other lifestyle scene.

**House lifestyle** — if the first image is a house lifestyle scene, every remaining image stays inside a residential home. Allowed: living room · coffee table · bedroom · vanity · dining area · window daylight · home décor. Never introduce: office · outdoor · commercial studio · café · restaurant · garden · hotel · street · any unrelated environment.

**NO THEME MIXING** — within one catalog never mix home+office · home+outdoor · office+outdoor · luxury studio+home · indoor+outdoor. **One catalog = one continuous theme.**

**Validation (before approving each image):**
- [ ] Same environment · [ ] same photography style · [ ] same lighting style · [ ] same mood · [ ] same props · [ ] same background family · [ ] same studio/home setting

If an image appears to belong to a different environment than the first approved image → reject internally · record the failure in `07_QUALITY_MEMORY` · regenerate.

**MASTER RULE:** a customer viewing the complete catalog should believe every image was photographed during ONE uninterrupted professional photoshoot in the same location, with only the camera position changing naturally.

### CATALOG APPROVAL & LEARNING WORKFLOW (user-locked 2026-07-17)
1. Load and validate all locked policies. 2. Load the 4-view CAD, cached Design Profile, Failure Memory, Approved Benchmarks. 3. Generate only ONE image for a new catalog. 4. Validate it against every active policy. 5. Deliver it for user approval. 6. **Do not generate the remaining catalog images until the first is approved.** 7. Apply every requested correction to that first image.
8. For every approval, correction or rejection, record in `07_QUALITY_MEMORY`: result (approved/rejected) · successful element · failure or requested change · root cause · prevention rule · correct expected result · applicable policy section.
9. **Never create duplicate rules.** 10. Merge each learning into the existing relevant policy ONLY when it creates a permanent generation requirement (`17` POLICY MERGE RULE).
11. **After the first image is approved:** lock its approved cloth · locked logo appearance · lighting + studio theme · photographic realism · preserve all approved jewelry corrections · generate the remaining catalog images automatically · **do not request repeated permission per image** (one-time permission above).
12. Validate every remaining image separately. 13. Reject and regenerate automatically when any policy or recorded learning fails.
14. Each subsequent image must learn from: successes of previously approved images · failures of rejected images · user corrections · existing Failure Memory · Approved Benchmarks.
15. **Never repeat the same or substantially similar mistake.**

**FINAL CATALOG LEARNING (after the complete catalog is approved):** review all successful images · review all rejected images · consolidate duplicate learnings · store final successes as Approved Benchmarks · store final failures + prevention rules in `07_QUALITY_MEMORY` · preserve only permanent, reusable learnings · never rewrite or duplicate locked policies.

**GIT RULE:** do NOT commit or push during image generation. After the complete catalog is approved: (1) save all final policy + QUALITY_MEMORY updates · (2) commit the completed catalog changes · (3) push to the authorized repository and branch · (4) never create a new branch without permission · (5) never push failed, temporary or unapproved images. (Detail: `15`.)

**WORKFLOW:** generate first image → validate → take approval + corrections → record learning → approve first image → generate remaining automatically → validate and learn continuously → complete catalog → store final learning → commit → push.

## A. JEWELRY PRESERVATION (P1)
- 100 % identical to the correct SOURCE file. Verify design by viewing the source before generating.
- Preserve: overall design/silhouette, stone SHAPE, stone COUNT, stone SIZE + spacing, SETTING type, PRONG count/shape/position, side/accent settings, gallery/trellis, band width + structure, metal type/color.
- NEVER: add stones, remove stones, add a center stone, resize, thicken the band, swap halo shape (round vs cushion), recolor gems, restyle prongs, or "improve" anything.
- **PRODUCT GEOMETRY LOCK (ABSOLUTE PRIORITY — user-locked 2026-07-11):** the reference image is the MASTER PRODUCT — the exact product to reproduce, NOT inspiration/style. Never redesign, reinterpret, beautify or improve any component. Preserve EXACTLY: overall silhouette; ring proportions; head/gallery/basket geometry; prong count/position/shape/thickness; center stone size + proportions; side stone size/count/spacing; halo diameter + geometry; crossover geometry; split-shank geometry; band width/thickness/curvature; shoulder profile; setting style; metal coverage; stone placement; and the relative distances between every component. Treat every visible pixel of the reference jewelry as ground truth. ONLY change camera angle, environment, lighting, background, photography composition — never the jewelry itself. If ANY jewelry component differs from the reference → regenerate before returning. **MENTAL MODEL:** imagine moving the SAME PHYSICAL RING to another photoshoot — never manufacturing a new ring; only the photography changes, the ring is the same object in every image (studio AND lifestyle). If two catalog images could plausibly be two different rings (e.g. a full symmetric halo in one and an open/asymmetric bypass halo in another), the jewelry drifted → regenerate all shots to the single source geometry.
- **GEM GEOMETRY LOCK (ABSOLUTE PRIORITY — user-locked 2026-07-11):** the uploaded gemstone is the exact physical stone — never estimate, reconstruct, reinterpret or create a new gem. Its geometry stays IDENTICAL in every image. Preserve exactly: shape, outline, length-to-width ratio, table size, crown height, pavilion depth, girdle thickness, culet position, symmetry, profile, silhouette, apparent size, orientation, optical proportions. The gemstone must look like the SAME physical stone from every camera angle — rotating the camera only reveals that same stone from a new view, never a differently-proportioned one. Do not modify its proportions. (Facet light/brilliance changes with angle as real optics dictate, but the stone's geometry does not.)
- **SIDE-PROFILE CONSISTENCY (user-locked 2026-07-11):** from ANY side angle preserve the reference's exact side profile — never deepen the pavilion, never increase crown height, never shorten/widen the outline, and (for fancy shapes) never let an oval/elongated stone appear rounder. The apparent gemstone proportions across front, 30°, 45°, 60°, side and rear views must be exactly those that would occur when photographing the ONE physical ring — the length-to-width ratio and crown/pavilion profile stay constant; only foreshortening from real perspective changes.
- **SIDE STONE & BAND LOCK (ABSOLUTE PRIORITY — user-locked 2026-07-11):** the side diamonds and band/shank diamonds are part of the original design — never redesign, resize, replace or reinterpret them. Preserve EXACTLY per stone: shape, size, count, proportions, position, spacing, orientation, alignment, setting type, prongs/beads, and metal coverage. Preserve the BAND itself EXACTLY: width, thickness, shoulder width, taper, curvature, cross-section, metal volume, polish, proportions. Side + band diamonds must show the SAME premium optics as the center stone (see §L): natural facet reflections, crisp facet junctions, realistic scintillation, balanced brilliance, natural fire, realistic contrast, proper transparency, correct optical depth — never artificial glow, over-whitening, blurred facets, plastic look, or painted highlights. Every diamond (center, side, band) reads as a real high-quality diamond captured by a pro camera under physically accurate lighting. Only camera angle, environment and lighting change; the jewelry never does.
- **DESIGN PRESERVATION (HIGHEST PRIORITY — user-locked 2026-07-16; target fidelity 99.9% identical to source).** The generated image must preserve the source jewelry EXACTLY. Never redesign, reinterpret, beautify, or improve the ring — the AI's only job is to place the *existing* ring into a realistic scene and lighting. Preserve exactly: twist/crossover geometry (incl. open negative spaces between strands); halo diameter AND thickness AND its height above the gallery; gallery architecture + support bars; basket design; cathedral structure; shank width + thickness; pavé layout + routing + stone spacing; stone count; stone size; stone orientation; prong count; prong position; ring proportions; ring height; side silhouette/profile; every visible metal contour. Observed failure (2026-07-16, twist-halo split-shank SKU): output was attractive but an "inspired recreation" — twist flattened + negative spaces closed, halo thickened + merged into head, gallery/basket redesigned, band thickened, pavé routing off, side profile + crown height changed. That is a COMPLETE REJECTION for a production catalog. **If ANY structural feature differs from the source CAD, the generation is a FAILURE → do not deliver; auto-fallback per `config/QUALITY_MEMORY.json geometry-immutable-auto-fallback` (composite the real source-ring pixels via `scripts/composite_ring_into_scene.py`, or render the angle from CAD), never ship the redesign.** Pure generation cannot hit 99.9% — the composite fallback is mandatory, not optional.
  - **GEOMETRY LOCK — the allow-list (user-locked 2026-07-16).** Treat the source render as the master CAD model. The ONLY things that may change between the source and the output are: environment/background (white cloth), lighting, camera angle, focus/depth-of-field, shadows, reflections. EVERYTHING structural stays identical: overall proportions, halo diameter + thickness, center-stone size + crown/table proportions, prong count/shape/placement, band width, twist/crossover geometry + openings, pavé layout/spacing, stone count, stone size, stone orientation, gallery, metal thickness, stone proportions. **Mental model:** the exact same physical ring is moved into a new photoshoot — never a newly interpreted version. This is the line between a *product visualization* and a *lifestyle photograph*: a lifestyle image depicts the SAME ring in a different setting, NOT a redesign. Applies equally to studio AND lifestyle/closeup shots.
  - Second observed failure (2026-07-16, round-halo twist-shank SKU): output was aesthetically pleasing but a redesign — halo thicker + halo diamonds larger (halo dominates), center stone larger relative to halo with different crown/table balance, twist shoulders widened + reshaped, pavé larger + differently spaced, prongs thicker + repositioned. All structural = FAIL → auto-fallback, never ship.
- Band: keep THIN; uniform thickness all the way around; structure exactly as source (plain / pavé single-row / twisted / half-eternity etc.).
- No extra metal under stones (open clean basket). Center stone level, centered, square.
- Non-front and worn/bare-hand angles are the biggest drift points — scrutinise hardest.

## B. DIAMOND RENDERING (P2)
- Every diamond (center AND small pavé/accent) = real photographed brilliant-cut: sharp individually visible facets (star/pinwheel), as clear/faceted as the center just smaller; each small stone bead-set with crisp faceting.
- CONTRAST: natural mix of bright-white flashes AND dark grey/black facet reflections. Colorless icy-white (top D), crystal clear, spotless.
- Center stone facet pattern = ONE real pattern from a single table. NO doubled/mirrored/ghost facets, NO CGI kaleidoscope symmetry.
- NO glassy beads, flat white dots, plastic/opaque or blown-out stones.
- Colored gems (e.g. LR-0136 green emeralds): keep exact color + cut (emerald/step cut), never recolor to white/diamond.
- Governs rendering only — never shape/cut/count/size/scale.
- **Benchmark image:** LR-0156 studio shot (user-approved 2026-07-10). Match every future center + pavé to that look.

## C. METAL RENDERING
- Default 18K NATURAL YELLOW GOLD — warm yellow, premium polished finish. Never rose/white/silver/pale unless the source is that metal.
- Match the source's exact metal color and finish. High polish; realistic gold reflections; no CGI shine.

### LOCKED 18K GOLD CONSISTENCY POLICY (user-locked 2026-07-17)
**Every image in a catalog must use the EXACT SAME 18K yellow gold colour** — the gold tone stays identical across all images, with **no variation in hue · warmth · saturation · brightness · reflectivity · finish**. Keep a consistent high-polish 18K yellow gold appearance throughout the entire catalog (office and lifestyle alike). **Only change the gold colour when the user explicitly requests another metal** (e.g. white gold or rose gold). Any image whose gold reads warmer, paler, duller, brassier or more/less polished than the approved master → reject before delivery and regenerate.

## D. CAMERA
- Studio: straight product angles (front top-down, macro, side profile, three-quarter, held-on-fold). Real DSLR macro look.
- Lifestyle: natural hand/product framing; shallow depth of field so the ring is the sharp hero.
- One consistent virtual camera / focal feel across all catalog images.

## E. LIGHTING
- Soft, even studio light; natural and realistic. Neutral white balance.
- No over-lighting, no artificial hotspots, no CGI glow, no starburst/lens flare, no rainbow fire.
- Studio cloth must never pick up warm/yellow lighting — keep neutral white.
- **Lighting character (user-locked 2026-07-11):** neutral daylight / luxury jewelry studio light with soft shadows, clean highlights, neutral white balance. NEVER yellow/orange/blue/blackish/dark, warm indoor, cinematic, dramatic, or moody lighting. White fabric stays pure neutral white; gold stays natural yellow gold; diamonds stay colorless. Lighting may change naturally by scene, but the reference's lighting calibration/white balance is preserved.

## F. BACKGROUND (P3 — see docs/11_BACKGROUND_STANDARD.md)
- Studio: the LOCKED white cloth material only, neutral pure white, same texture/fold/grain as references, with the printed logo (composited locally).
- Lifestyle/closeup: cozy warm US-home scene (soft knit, marble, warm window light); soft blurred background; NO desks/laptops/offices; NO logo.

## G. COMPOSITION
- Studio: ring as hero, CENTERED horizontally+vertically, occupying ~55-70% of visual attention with balanced margins (user-locked 2026-07-15; see docs/12 §A2); elegant natural cloth drape; logo stays a secondary, naturally off-center branding mark (never dead-center itself, never competing with the ring — this off-center guidance applies to the LOGO only, the ring is always centered).
- Lifestyle: natural hand pose, five fingers, natural skin, neutral manicure; ring prominent and sharp.
- Vary pose every image and every catalog (looks like a real photoshoot, not a template) — vary angle/pose, never the ring's centered position.

## H. CROPPING
- Ring fully visible and sharp.
- The printed logo MAY be partially cropped by the frame, partly hidden behind the jewelry, or interrupted by a fold (60–90 % visible) — this is realistic and preferred. Never crop the ring itself awkwardly.

## I. RESOLUTION / FORMAT
- ALWAYS `aspect_ratio:"1:1"` and `resolution:"2k"`. No 4:5, no 1k. No quality compromise for token savings.

## J. SHADOW RULES
- Natural soft contact shadows under the ring on the cloth; consistent single soft light direction.
- Printed logo must sit UNDER the fabric's own shadows/highlights (it is printed on the cloth, so folds and shadows pass over it). It must not float above shadows like a sticker.
- Lifestyle: natural shadows consistent with the home lighting; ring casts believable soft shadow.

## K. HANDS (lifestyle)
- Exactly five natural fingers, natural skin tone/texture, neutral manicure. No extra/missing/warped fingers.

## L. DIAMOND REALISM (locked 2026-07-10)
Diamonds must look like a real professionally photographed natural gemstone under luxury studio light — bright, crisp, clean, transparent, highly reflective, naturally brilliant, but NEVER artificially white.
- FORBIDDEN: overexposed/pure-white "glowing" stones, artificial whitening, burnt/clipped highlights, flat white reflections, plastic/milky/cloudy look, AI glow, unrealistically perfect reflection symmetry, fake sparkle, CGI lighting, exaggerated fire/rainbow, excessive contrast, artificial sharpening. **Never a fake-gem look:** no CZ, moissanite (over-dispersive rainbow), glass, plastic, acrylic, artificial crystal, or CGI-gemstone appearance — every stone reads as a premium natural-looking lab-grown diamond.
- REQUIRED: natural brilliance, realistic scintillation, natural fire, realistic contrast, visible facet structure, correct internal reflections, accurate light return, natural transparency, proper depth, realistic crown/pavilion reflections. Highlights controlled — no part of the stone becomes a solid white area; the facet pattern stays clearly visible.
- Use the reference's existing bright studio light; do NOT increase brightness/sparkle/whiteness. Beauty comes from correct optics, not enhancement.
- **SCOPE — EVERY ENVIRONMENT, EVERY STONE (user-locked 2026-07-11):** this diamond standard applies to EVERY image regardless of scene — office studio, home lifestyle, indoor, outdoor, editorial, luxury product, macro, and any future scene — and to EVERY stone (center AND every side/accent stone) across all shapes, cuts, and carat sizes. Automatically preserve the correct optical properties for each shape/cut/carat: physically accurate proportions, correct facet pattern, crystal-clear water-like clarity, razor-sharp facet definition, natural brilliance/fire/scintillation, realistic internal+external reflections, accurate light return, visible depth, high optical symmetry. Lighting behaves according to the ACTUAL environment while diamond optics stay physically accurate. Every center and side stone must be indistinguishable from a real professionally photographed premium VVS/IF lab-grown diamond — never AI-generated-looking, never artificial sparkle/glow/rainbow, never overexposed/milky/cloudy/plastic/glass/CGI/unrealistic reflections. Natural realism always outranks visual enhancement.
- **OPTICAL SPEC (user-locked 2026-07-11) — match the reference's optical quality; a professionally photographed premium lab-grown diamond, NOT an AI-enhanced gem:** crystal-clear water-like transparency; razor-sharp facet definition; excellent light return; high optical contrast between bright and dark facets; natural white brilliance; small realistic spectral fire ONLY where physically correct; accurate crown/table/pavilion/girdle geometry; crisp reflections inside every facet. NONE of: milky, cloudy, washed-out white areas, artificial glow, bloom, fake sparkle, overexposed highlights, excessive sharpening, plastic/glass look, CGI look. Looks captured with a professional macro camera under luxury studio lighting; every visible facet clean/crisp/physically correct; optical behavior true to the cut + camera angle; brilliance never boosted artificially. End result reads as a real VVS/IF-quality diamond in a high-end studio: exceptional clarity, realistic brilliance, perfectly defined facets.
- **DIAMOND GEOMETRY + PHYSICAL OPTICS LOCK (HIGHEST PRIORITY — user-locked 2026-07-11):** the diamond is NOT recreated — its geometry already exists in the reference; every view = the SAME physical stone from another camera position. Preserve EXACTLY the full cut anatomy: overall dimensions, length-to-width ratio, table size, crown angle, crown height, pavilion depth, girdle thickness, culet position, facet layout, facet count, facet proportions, star facets, bezel facets, upper-girdle facets, lower-girdle facets, pavilion mains, symmetry, polish, optical symmetry. Changing the camera MUST NOT change oval proportions, pavilion depth, crown height, table size, stone thickness/volume, silhouette, or the optical pattern. Physical optics: every angle keeps identical facet pattern, optical symmetry, brilliance, scintillation, fire, contrast, transparency, light return, optical depth — no invented reflections/facets/pavilion/crown, no fake sparkle/glow, no overexposed white, no melted facets, no blurry junctions, no plastic. Reads as a pro-photographed IGI-certified premium lab-grown diamond from EVERY angle.
- **SIDE-VIEW LOCK:** side views reveal the SAME stone — never make it appear thinner/thicker/longer/shorter/flatter/deeper/wider/narrower; visible pavilion, crown and girdle stay geometrically consistent with the front view; the profile looks exactly as if a real photographer rotated the same ring by 20°/45°/60°/90°. Never generate a new diamond; only reveal the existing one from another angle.
- **ACCENT QUALITY LOCK:** side diamonds, baguettes and accent stones get the SAME macro-lens rendering quality as the center — exact dimensions, cut, proportions, facet structure, symmetry, brilliance, fire, transparency, scintillation. Never simplify/blur accents; never replace baguettes with generic glass. Every accent reads as a real premium lab-grown diamond shot with the same professional macro lens as the center.

## M. PHOTOGRAPHY / REFERENCE CONSISTENCY (locked 2026-07-10)
Every image matches the approved master reference: identical camera height, camera distance (framing/crop), lens perspective, field of view, image scale, lighting intensity, bright exposure, white balance, lighting direction, soft-shadow quality, and locked cloth. The existing lighting is correct — do NOT brighten/darken/warm/cool. Jewelry appears at a consistent size across the whole catalog. No zoom in/out; no significant camera height/distance change.

## N. NATURAL VARIATION (locked 2026-07-10)
Do not repeat the same composition. Keeping camera height + distance fixed, naturally vary only what a real photographer changes between shots: ring rotation/orientation/placement, camera left/right position, yaw around the piece (slight pitch when needed), cloth draping/folds (plain OR folded — whichever looks natural, don't force folds), logo visibility, and composition. Each image = another photograph from the same shoot; unique yet fully consistent.

## O. COLOR FIDELITY (ABSOLUTE PRIORITY — locked 2026-07-11; color fidelity > artistic styling)
The SOURCE image is the master reference for ALL colors. Preserve its original color palette and neutral white balance EXACTLY. Color fidelity to the source outranks any artistic/stylistic consideration.
- **No color grading of any kind:** never apply automatic color grading, artistic/cinematic color styling, warm-tone "enhancement," creative white-balance, teal-orange, film looks, or any stylized LUT.
- **White balance = source, neutral:** never introduce a pink, yellow, red, orange, beige, cream, ivory, gray, blue, purple, or green tint, and no warm OR cool color cast. The generated image must match the source's neutral color balance.
- **Lighting:** preserve the existing bright neutral studio lighting. Do NOT increase warmth, saturation, or contrast unnaturally; no HDR-like effects; no unnecessary exposure change. Bright, neutral, consistent with the source.
- **Metal & diamonds:** preserve natural metal color and diamond appearance; never inject artificial colored reflections or color contamination into the jewelry.
- **Cloth:** the approved premium white cotton stays the same neutral white as the source — never yellowish/pinkish/reddish/creamish/beige/off-white.
- **FINAL VALIDATION (run before returning EVERY image):** ✓ colors match source ✓ white balance matches source ✓ no pink/yellow/red/cream/beige/warm tint ✓ lighting neutral ✓ cloth premium neutral white ✓ jewelry colors natural. If ANY color shift is detected → correct locally (`whiten_cloth.py`, 0 credits) or regenerate BEFORE returning. A warm/tinted cast is a hard FAIL (see docs/11 FAILURE POLICY).
