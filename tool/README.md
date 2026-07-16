# Lucent Carat Lab — Catalog Generator (Web App)

A dashboard that runs the full per-SKU catalog pipeline (the workflow currently
done by hand in chat) with **auto generation + auto-QC + auto-fallback and one
approval gate before delivery**. Runs on your own machine/server, so — unlike the
chat sandbox — it CAN download Higgsfield renders, which unblocks automatic QC and
the geometry-immutable composite fallback.

> This tool does not replace the rules in the repo root — it EXECUTES them.
> Prompts, quality rules, angle standards, and the two composite scripts remain
> the single source of truth (`prompts/07_PROMPTS.md`, `config/QUALITY_MEMORY.json`,
> `docs/12_STUDIO_ANGLES_STANDARD.md`, `scripts/*.py`).

## Quick Start (portable — any clean machine)

No manual folder recreation, no hidden local state: clone → configure secrets →
one setup command → one start command → generation-ready.

**Windows (PowerShell):**
```powershell
git clone https://github.com/SidGajera/Claude_Lucent_Image_Gen.git
cd Claude_Lucent_Image_Gen
.\scripts\setup.ps1          # creates the venv, installs deps, copies .env, runs a health check
notepad tool\.env            # fill in HIGGSFIELD_API_KEY / ANTHROPIC_API_KEY / GOOGLE_APPLICATION_CREDENTIALS
.\scripts\start.ps1          # serves the API — open the printed http://127.0.0.1:8000
```

**macOS / Linux:**
```bash
git clone https://github.com/SidGajera/Claude_Lucent_Image_Gen.git
cd Claude_Lucent_Image_Gen
./scripts/setup.sh           # creates the venv, installs deps, copies .env, runs a health check
$EDITOR tool/.env            # fill in HIGGSFIELD_API_KEY / ANTHROPIC_API_KEY / GOOGLE_APPLICATION_CREDENTIALS
./scripts/start.sh           # serves the API — open the printed http://127.0.0.1:8000
```

Re-run `scripts/health-check.sh` (or `.ps1`) any time to verify the repo is intact
without starting the server — it checks required files, the locked logo/cloth
asset checksums, and that every workspace path is writable, and never calls a
provider or spends a credit. Missing provider keys are reported as warnings, not
failures — the app still starts, it just refuses to generate until they're set.

All input/output/reference/cache paths are configurable — see
[`tool/backend/lib/config/paths.py`](backend/lib/config/paths.py) and the
commented overrides in [`tool/backend/.env.example`](backend/.env.example).
Nothing in this tool depends on the original developer's machine, absolute paths,
or any state that isn't in this Git repo.

## Pipeline (job stages)
1. **FETCH** — Google Drive: find `LR-XXXX` folder, download CAD source views.
2. **STUDY** — Claude vision → `design_profile` (center cut, prong count, halo,
   band, metal, gallery). Editable by the operator before generation.
3. **IMPORT** — Higgsfield: source + branded cloth + logo + lifestyle/close-up poses
   (rotate poses vs the previous SKU).
4. **GENERATE** — `nano_banana_2`, 2K, 1:1, 5 studio + 4 lifestyle + 3 close-up,
   using the locked prompt templates + design profile + rotated camera angles.
5. **DOWNLOAD** — pull every render locally (no CDN block here).
6. **AUTO-QC** — Claude vision compares each render to the source across the
   `geometry-immutable-auto-fallback` checklist (prong count, halo diameter+rim,
   center-to-halo ratio, shank, gallery, silhouette) + lighting + logo two-tone.
7. **AUTO-FALLBACK / DEFAULT-COMPOSITE** — the composite path is the DEFAULT, not
   only a drift fallback (user-locked 2026-07-16, after 5 rejected renders across 4
   SKUs). `lib/pipeline/pipeline.process_shot()` composites the real source-CAD ring
   into the AI scene so geometry is identical to source by construction; lifestyle +
   close-up ALWAYS composite. Studio also stamps the two-tone logo
   (`scripts/print_logo_on_cloth.py`). Reachable via `POST /composite`. Manual
   `fallback.py` CLI is debug-only.
8. **APPROVAL GATE** — dashboard shows the 12 with pass/fail badges; operator
   Approves / Rejects / Redoes per image.
9. **DELIVER** — upload approved set to the Drive Output folder, write
   `config/deliveries/LR-XXXX.json`, commit to `main`.

## Architecture
- **Backend:** FastAPI. REST for actions, WebSocket for live stage/progress events.
  Jobs are stateful (one per SKU run) and persist to `tool/backend/jobs/<sku>.json`
  so a run survives a restart and holds at the approval gate.
- **Frontend:** `tool/web/` — SKU input, live pipeline progress, 12-image review
  grid with QC badges and Approve/Reject/Redo, Deliver button.
- **Reuse:** loads repo `config/project_manifest.json` for folder IDs + generation
  settings; calls the existing Python composite scripts as the fallback engine.

## Backend modules
| File | Responsibility | Status |
|---|---|---|
| `config.py`             | Load repo config (`../../config/*.json`), env, folder IDs | built |
| `lib/config/paths.py`   | `PathConfig` — single source of truth for every filesystem path (env-overridable) | built |
| `health_check.py`       | Standalone startup validation; never spends credits | built |
| `drive.py`              | Find/download source; upload outputs (google-api-python-client) | to build |
| `higgsfield.py`         | Import media, generate, poll, DOWNLOAD renders (REST) | to build |
| `study.py`              | Claude vision → design_profile (Anthropic SDK) | to build |
| `prompts.py`            | Build the 12 prompts from templates + profile + angle rotation | to build |
| `lib/pipeline/qc.py`       | Provenance-first geometry gate (composite = guaranteed; raw render = unverified) + optional vision hook | **built** |
| `lib/pipeline/fallback.py` | Composite engine: wraps composite_ring_into_scene.py / print_logo_on_cloth.py as importable fns + debug CLI | **built** |
| `lib/pipeline/pipeline.py` | Default-composite policy: `process_shot()` composites the real source ring into the AI scene, then QC | **built** |
| `server.py`                | FastAPI app: REST + WebSocket; `POST /composite` live | `/health` + `/composite` live |

All path-bearing modules above must import `PATHS` from `lib.config.paths` rather
than building a path independently — that's the one place folder locations live.

## REST / WS surface (draft)
- `POST /jobs {sku}` → start a run
- `GET  /jobs/{sku}` → job state + per-image QC
- `POST /jobs/{sku}/study` → edit/confirm design profile, then continue
- `POST /jobs/{sku}/approve {image_ids}` / `POST .../reject {image_id}` / `POST .../redo {image_id}`
- `POST /jobs/{sku}/deliver` → upload + delivery record + commit
- `WS   /jobs/{sku}/events` → stage/progress/log stream

## Credentials (`tool/.env`, git-ignored)
```
HIGGSFIELD_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
```

## Build milestones
1. **M1 — Backend core (no UI):** config + drive + higgsfield + prompts; CLI that
   fetches, generates 12, downloads. (Proves the APIs + unblocks downloads.)
2. **M2 — QC + fallback:** qc.py + fallback.py wired; drift auto-composites.
3. **M3 — Server + job state:** FastAPI, WebSocket progress, approval gate.
4. **M4 — Dashboard:** review grid, approve/reject/redo, deliver + commit.
5. **M5 — Polish:** pose-rotation tracking, retries for the flaky Higgsfield
   connection, delivery logging, auth on the dashboard.

Setup/start commands are covered by the **Quick Start** section at the top of
this file — `scripts/setup.*` and `scripts/start.*` replace manual venv steps.
