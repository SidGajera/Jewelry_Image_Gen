# 08 — PHOTO CLEANUP THROUGH ENGINE 2 (`gflow-nb2`) — LOCAL RUNBOOK

**What this is for.** Cleaning an EXISTING photograph — dust, lint, fingerprints, surface
grime — through Nano Banana 2 on the Google Flow route, on user instruction (2026-08-26:
*"Clean image with 2nd pipeline"*).

**Where it runs.** A local machine only. Claude Code on the web cannot reach engine 2: the
sandbox egress policy denies `openflowmcp.com:443` (gateway 403 to CONNECT). Nothing in this
runbook works from a web session until that host is allowed in the environment's network
policy.

---

## 0. Read this before you run it

Engine 2 does not retouch. It **re-rolls the frame** on every call — the upstream's own
measured note (2026-08-23):

> "One call re-rolls everything at once: fix the focus and the freckles change, fix the
> freckles and the bottle changes size."

A reference in `image_inputs` steers the render; it does not carry the source pixels through.
So the piece that comes back is a rebuilt piece. On a solitaire the things that drift — facet
pattern, prong tips, girdle line, stone diameter — **are** the design. That is why §3 is not
optional: the render is not finished when it looks clean, it is finished when it measures
clean.

If the requirement is *the diamond must not change*, the deterministic path
(`scripts/clean_photo.py`) holds the design by construction and this route does not. Use this
runbook when engine 2 is what was asked for, and gate the output either way.

---

## 1. Preconditions

```bash
claude mcp add --transport http openflow https://openflowmcp.com/mcp
```

Then, in the local session: `check openflow status` (registers a key), and
`connect my Google account to openflow` (runs the local grabber; the password is typed into
Google's own page). Already done 2026-08-21 for the account recorded in
`config/engines.json` → `engines.openflow.auth`. Confirm with `check openflow status` rather
than assuming the session survived.

Images are free on this route; only video spends Google credits.

## 2. The call

Give the local agent the source photo and this instruction. Keep the prompt short — a long
scene description invites the engine to re-roll more of the frame, which is the failure mode.

> Use openflow's `generate_image` with Nano Banana 2. Pass the attached photograph as
> `image_inputs`. Aspect ratio 1:1.
>
> Prompt:
> *Retouch this exact photograph. Remove only the dust specks, lint and fingerprint smudges
> from the ring and from the black reflective surface. Keep the ring itself exactly as
> photographed — identical diamond, identical facet pattern, identical prongs, identical band
> shape and thickness, identical yellow gold colour, identical size and position. Keep the
> mirror reflection, the dark glossy surface, the soft light band and the out-of-focus
> highlights. Natural clean studio photograph, real camera, natural sparkle from the existing
> highlights. Do not restyle, do not redesign, do not beautify, do not add sparkle or glare
> that is not already there, do not smooth the surface into plastic, do not add text or
> watermark.*

Then save the result into the repo:

```
save that image to workspace/output/<SKU>_gflow_clean.png
```

## 3. Gate it — three checks, in order

**a. Watermark.** `docs/26` §5 records that every image generated through this bridge on
2026-08-21 carried Google's sparkle mark in the bottom-right *despite* the service's
`visible_watermark: false` flag. Look at the corner. A watermarked render is dead on arrival
for a deliverable that must not read as AI.

**b. Design drift — the blocking check.**

```bash
python3 scripts/verify_drift.py \
  --source   workspace/input/<SKU>.jpg \
  --candidate workspace/output/<SKU>_gflow_clean.png \
  --report   workspace/output/<SKU>_drift.json
```

Exit 0 = every measurable design check held. Exit 1 = the piece changed; **reject the render,
do not deliver it, and do not talk yourself into it because the photograph looks good**
(LAW-02). The measure that catches a resized stone is `stone vs metal area` — share-of-piece
saturates on a solitaire and waved a forged 1.12x stone through at 3.91%.

Re-roll on a rejection, at most 5 rounds, then STOP and report (LAW-02).

**c. Did it actually clean anything.** Drift 0 is trivially satisfiable by a render that
changed nothing at all. Compare the dust visually, or run the source through
`scripts/clean_photo.py --report` and compare speck counts.

## 4. Delivery

Engine 2's native frame is 768x1376, upscaled to 1536x2752, delivered as a 1536x1536 centre
crop — 43.75% less pixel area than engine 1's native 2048². That trade is already accepted in
`config/delivery_profiles.json`. `G1_FORMAT` still governs what may ship.
