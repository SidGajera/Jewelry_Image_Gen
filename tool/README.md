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
7. **AUTO-FALLBACK** — on any drift, do NOT ship: run
   `scripts/composite_ring_into_scene.py` (exact source ring) and
   `scripts/print_logo_on_cloth.py` (two-tone logo, black tagline). Re-QC.
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

## Backend modules (to build)
| File | Responsibility |
|---|---|
| `config.py`      | Load repo config (`../../config/*.json`), env, folder IDs |
| `drive.py`       | Find/download source; upload outputs (google-api-python-client) |
| `higgsfield.py`  | Import media, generate, poll, DOWNLOAD renders (REST) |
| `study.py`       | Claude vision → design_profile (Anthropic SDK) |
| `prompts.py`     | Build the 12 prompts from templates + profile + angle rotation |
| `qc.py`          | Claude vision render↔source geometry/logo/lighting verdict |
| `fallback.py`    | Invoke composite_ring_into_scene.py / print_logo_on_cloth.py |
| `pipeline.py`    | Orchestrate stages; emit progress; hold at approval gate |
| `server.py`      | FastAPI app: REST + WebSocket |

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

## Setup (once modules exist)
```
cd tool/backend
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in keys
uvicorn server:app --reload
# then open tool/web/index.html (or the React dev server)
```
