# IMAGE GENERATION LAW — PERMANENT, BINDING, NON-NEGOTIABLE

**User-locked 2026-08-22.** This file is the **boundary** of image generation. No catalog, no
SKU, no engine, no model, no pipeline, no mode, no session and no future instruction short of
the user's own explicit change may generate outside it.

> **Format contract.** This file states LAW. It never restates a rule's text — each clause
> **points at the one rule that owns it** in `policy/registry.json`. One law clause → one owner
> rule → one enforcing gate. If you want to know the exact wording of a requirement, read the
> owner rule. Editing a requirement means editing its owner rule, never this file and never a
> second copy elsewhere. This is what keeps "one policy, one rule, one instruction" true.

**Integrity.** `policy/generation_law.json` carries this file's SHA-256. `policy/law_gate.py`
verifies it, verifies every clause resolves to exactly one ACTIVE owner rule, and verifies each
owner's gate exists. `run_catalog.py` runs that gate **first, before anything else**, and STOPs
the catalog on any failure. The law cannot be silently weakened, bypassed or deleted.

---

## LAW-01 · JEWELLERY DESIGN IS ABOVE EVERYTHING

- **STATUS:** PERMANENT · BINDING · HIGHEST PRECEDENCE
- **INSTRUCTION:** The jewellery design outranks every other consideration — scene, styling,
  theme, pose, lighting, composition, aesthetics, token cost and delivery schedule. When any of
  those conflict with the design, the design wins and the other thing changes.
- **OWNER RULE:** `JEWELRY_PRESERVATION_ABSOLUTE` (key `geometry.preservation`)
- **ENFORCED BY:** `G_INVENT`, `G20_MIN_SUBJECT_SCALE`, `G22_STONE_WITHIN_FINGER`, `law_gate`
- **ON VIOLATION:** reject the render, regenerate. Never deliver, never negotiate the design down.

## LAW-02 · NO AI REDRAW OF THE JEWELLERY — EVER

- **STATUS:** PERMANENT · BINDING · STRICTLY RESTRICTED
- **INSTRUCTION:** The generation model's job is to build the **photograph** — scene, hand, skin,
  cloth, environment, light, shadow — to instruction. It may **not** regenerate, redesign,
  redraw, restyle, "improve", "clean up", complete or reinterpret the jewellery. The piece comes
  from the source and stays as the source has it. Target: **D2D pixel-perfect**.
- **OWNER RULE:** `JEWELRY_PRESERVATION_ABSOLUTE` (key `geometry.preservation`)
- **ENFORCED BY:** `G_INVENT`, `G2_ACCENT_COUNT`, `G7_SETTING_COUNT`, `G8_UNAUTHORIZED`,
  `G9_PIECE_COUNT`, `G21_STONE_RATIO`
- **ON VIOLATION:** reject and regenerate; max 5 rounds; then STOP and report. Never deliver a
  redrawn piece, and never label drift acceptable because the photograph looks good.
- **HONEST LIMIT — READ THIS.** A generative call cannot *guarantee* D2D by construction; it
  re-synthesises what it draws. This law is therefore enforced **by rejection, not by promise**:
  every render is gated against the source and a drifted render is refused. That is the strongest
  enforcement a generative pipeline admits. Guarantee-by-construction needs the jewellery layer
  placed from source pixels (see `config/pipeline_versions.json` → `composite-v1`), which the
  current delivery profile does not do. Do not claim D2D is guaranteed; claim it is enforced.

## LAW-03 · SOURCE READING IS COMPULSORY BEFORE GENERATION

- **STATUS:** PERMANENT · BINDING · BLOCKING PRECONDITION
- **INSTRUCTION:** No source, no generation. The source must be read **before** any image is
  requested. Generation without a verified source read is prohibited outright.
- **OWNER RULE:** `SOURCE_COVERAGE_GATE` (key `geometry.no_invention`)
- **ENFORCED BY:** `G_INVENT`, `validate_source`, `law_gate`
- **ON VIOLATION:** STOP before generating. Never infer, never fall back to category priors,
  never "fill in" an unread feature.

## LAW-04 · PER-ANGLE SOURCE COVERAGE — WARN, THEN SKIP OR CONTINUE

- **STATUS:** PERMANENT · BINDING
- **INSTRUCTION:** Every angle needs its own source view. When an angle has **no** source
  reference, the pipeline must **warn by name** —
  `SOURCE NOT IDENTIFIED FOR THIS ANGLE: <slot> (<azimuth>/<elevation>) — SKIP or CONTINUE?` —
  and wait for that decision. It must never quietly invent the unseen side.
- **OWNER RULE:** `SOURCE_COVERAGE_GATE` (key `geometry.no_invention`)
- **ENFORCED BY:** `G_INVENT`, `law_gate`
- **ON VIOLATION (silent generation of an uncovered angle):** reject the slot, warn, re-decide.
- **DECISION MEANING:** `SKIP` drops the slot from the catalog and records why. `CONTINUE`
  generates it and stamps the slot `SOURCE_UNVERIFIED` in the manifest, so an uncovered angle is
  never mistaken later for a verified one.

## LAW-05 · ONE CATALOG, ONE PIECE — CONSISTENT THROUGHOUT

- **STATUS:** PERMANENT · BINDING
- **INSTRUCTION:** Every image in a catalog shows the *same* piece: same design, same stone
  clarity and purity, same metal colour, same jewellery shape, same jewellery size and same
  diamond size. Nothing about the piece may drift between slot 01 and slot 10. Only camera,
  scene and light change across the catalog.
- **OWNER RULE:** `CATALOG_CONSISTENCY` (key `geometry.catalog_consistency`)
- **ENFORCED BY:** `G28_CATALOG_CONSISTENCY`, `law_gate`
- **ON VIOLATION:** reject the drifted slot — not the catalog — and regenerate it against the
  established catalog reference.

## LAW-06 · DIAMONDS: CRYSTAL CLEAR, NATURAL, PURE — EVERY IMAGE

- **STATUS:** PERMANENT · BINDING
- **INSTRUCTION:** Every stone in every image reads crystal clear, natural and pure. Never
  cloudy, milky, glassy-fake, grey, yellow-cast, plastic, CZ-like or dulled in shadow.
- **OWNER RULE:** `DIAMOND_CLARITY_ABSOLUTE` (key `realism.clarity`)
- **ENFORCED BY:** `G24_CLARITY_CHECK`
- **ON VIOLATION:** auto-regenerate the slot. Never deliver a dull or cloudy stone.

## LAW-07 · THE LAW IS THE BOUNDARY — ONE RULE PER TOPIC

- **STATUS:** PERMANENT · BINDING · SELF-ENFORCING
- **INSTRUCTION:** Generation may not go outside these clauses. Every topic has exactly **one**
  active owner rule; a second rule on the same topic is a hard STOP, not a preference. A new
  requirement **supersedes** the existing owner (carrying its learning forward) — it never opens
  a parallel rule, and it is never written as prose in a doc instead of as a rule.
- **OWNER RULE:** `GENERATION_LAW_BINDING` (key `policy.generation_law`)
- **ENFORCED BY:** `law_gate`, `ENGINE_LOCK_CHECK`
- **ON VIOLATION:** `run_catalog.py` refuses to start. No catalog runs against a broken law.

---

## PRECEDENCE (highest first)

1. **LAW-01 / LAW-02** — the jewellery design and its preservation. Nothing outranks these.
2. **LAW-03 / LAW-04** — source truth and coverage. No source, no pixels.
3. **LAW-05 / LAW-06** — catalog consistency and stone quality.
4. **LAW-07** — the integrity of the law itself.
5. Everything else in `policy/registry.json` — engine, format, theme, framing, plausibility.

Engine, model, pipeline, resolution, credits, speed and token budget sit **below all of it**.
An engine that cannot satisfy a law clause is refused; the clause is never relaxed to fit an
engine (`POLICY_SUPREMACY`, key `policy.supremacy`).

## CHANGING THIS LAW

Only on the user's explicit instruction, and only by editing the **owner rule** in
`policy/registry.json` through a supersession that carries the old rule's `failure_cases` and
statement forward. Then re-stamp the checksum:

```bash
python policy/law_gate.py --restamp     # after an authorised change
python policy/law_gate.py --check       # must print: generation law OK
```

A change that cannot pass `--check` is not an authorised change.
