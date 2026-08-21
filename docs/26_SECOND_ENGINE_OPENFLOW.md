# 26 — SECOND GENERATION ENGINE: openflow (Google Flow bridge)

**Scope.** This file owns ONE thing: **the existence, limits and permitted uses of engine 2.**
It does not weaken `docs/21` (which engine renders production images) or `docs/15` +
`config/pipeline_versions.json` (pipeline version). Machine-readable form:
[`config/engines.json`](../config/engines.json). Resolver: [`scripts/engine.py`](../scripts/engine.py).

Added on user instruction 2026-08-21: *"Make 2nd image generation pipeline with above github url — 1st one is higgsfield."*

## 1. The two engines

| # | id | role | backend | catalog stills |
|---|---|---|---|---|
| 1 | `higgsfield` | production default | Higgsfield MCP, model locked in `config/model.json` | **yes — only engine allowed** |
| 2 | `openflow` | secondary, opt-in | Google Flow via [molkex/mcp-flow-google](https://github.com/molkex/mcp-flow-google) (Veo video, Nano Banana images) | **no** |

Engine 1 is unchanged by this document. Its frozen call — 2K, 1:1, `count: 1`, one batch,
medias `[pose_studio_ref, SOURCE_piece]`, no img2img, no denoise, no compositing — is
recorded verbatim in `config/engines.json` and is what `run_catalog.py --emit-plan` emits
when no `--engine` is given.

## 2. Why engine 2 cannot produce catalog stills

Its native output is **1376×768 / 16:9**. The locked delivery format is **1:1, 2048×2048,
native, no upscale** (`FORMAT_ASPECT`, gate `G1_FORMAT`). Routing a delivered still through
engine 2 would degrade output, which the same instruction that created engine 2 forbids
("output should not degrade, only upscale"). `scripts/engine.py` therefore raises
`EngineViolation` for `purpose="catalog_stills"` on any engine whose `catalog_approved` is
false, and `run_catalog.py` calls that gate before it emits a plan or writes a manifest.

Its `generate_image` tools also run Nano Banana Pro / Lite outside Higgsfield, which would
breach both `docs/21` and MODEL_LOCK. Engine 2 image tools are for **non-delivery
exploration only**, and their output must never be written into `deliveries/` or a
`workspace/golden/<SKU>/` render slot.

## 3. What engine 2 is for

* **Video** — Veo clips at 4 / 6 / 8 / 10 s (7 / 10 / 12 / 15 credits), including
  `generate_video_from_image` off an already-approved still, frame interpolation, extension.
* **Non-delivery exploration** — moodboards, pose or scene tests that never ship.

Engine 1 also generates video and remains the default for it. Engine 2 is used only when the
user names it. Video of any kind still needs **per-request permission** before generating.

## 3a. Switching engines (one command)

```bash
python scripts/engine.py --use openflow      # exploration / video work
python scripts/engine.py --use higgsfield    # back to engine 1
python scripts/engine.py --show              # what is active right now
```

The selection is stored in `config/active_engine.json` and read by
`engine.resolve()` whenever no engine is named explicitly.

**The switch only moves switchable work.** `catalog_stills`, `macro`,
`lifestyle_stills` and `any_delivered_image` are in `engine.LOCKED_PURPOSES`:
they resolve to engine 1 no matter what is active. Verified behaviour with
`--use openflow` selected:

| call | resolves to |
|---|---|
| `run_catalog.py <SKU> --emit-plan` | `higgsfield`, model `nano_banana_2` |
| `resolve(purpose="video")` | `openflow` |

That is why the switch can stay cheap: flipping it cannot degrade a delivered
image, so nobody has to remember to flip it back before a catalog. `--check`
asserts this by switching to every non-default engine in turn and confirming a
`catalog_stills` resolve still returns engine 1.

To point a *delivered* catalog at another engine you still need the
authorization phrase in §4.5 — that is a policy change, not a switch.

## 4. Hard rules

1. **Never auto-selected.** Engine 2 runs only when named — `--engine openflow` on a command, or selected with `--use openflow` (§3a). Nothing selects it implicitly.
2. **Never a fallback.** On any engine-1 failure — generation, timeout, API, connector,
   quality, geometry — the engine does not change. Retry inside engine 1 (`docs/21` §1a).
3. **Never mixed inside one catalog.**
4. **Never writes a delivered image.**
5. Changing which engine is *production* still requires the authorization phrase:
   **"Change the image generation pipeline."** Adding engine 2 did not use that phrase and
   did not change production.

## 5. Connecting it (user action, not automatable here)

```bash
claude mcp add --transport http openflow https://openflowmcp.com/mcp
```

Then connect the Google account through the server's local login script (`onboard_local.js`
— upstream ships mac/linux Chrome paths only, so Windows needs the `ONBOARD_CHROME` override
or a patched `findChrome()`), and hand the printed `{email, oauth_token}` to
`add_account_token`.

**Done on 2026-08-21** for `gajerasiddharth10@gmail.com` (owner key `gh-sidgajera-3dc9`),
so `config/engines.json` status is now `active`. Observed capability at that point:
images unmetered; **video refused** (`can_generate_video: false`) pending a paid openflow
subscription, and thereafter costing 7–15 Google credits per clip against a 50-credit
monthly tier. Revoke the grant at `myaccount.google.com/device-activity` — it appears as a
device session, not an app.

**The service's `visible_watermark: false` flag is unreliable.** Every image generated on
2026-08-21 carried Google's sparkle mark in the bottom-right despite that flag. Check the
corner of a render before trusting it.

**Security note.** Google publishes no API for Flow, so this is an unofficial hosted bridge.
The password is typed into Google's own page, but the resulting session is exercised by
`openflowmcp.com`. Do not connect an account the user has not deliberately chosen to expose.
Concurrency is 8 simultaneous generations per Google account.

## 6. Verification

```bash
python scripts/engine.py --list
python scripts/engine.py --check
```

`--check` asserts: default is `higgsfield`, `auto_fallback` is false, the catalog-approved set
is exactly `['higgsfield']`, engine 1's constraints are still 2K / 1:1 / count 1, and every
other engine actually refuses a `catalog_stills` resolve. It runs inside `run_catalog.py`'s
regression step, so a catalog cannot complete with the engine lock broken.
