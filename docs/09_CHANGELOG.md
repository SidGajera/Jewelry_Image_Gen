# 09 — CHANGELOG

## v1.1.0 — 2026-07-10 (STABLE MILESTONE: portable export + printed-logo policy)
- **Logo policy finalized → PRINTED-ON-CLOTH.** The logo must always appear, composited from the locked asset to look physically printed on the fabric (follows folds/perspective/lighting, partial crop/occlusion OK, off-center). Supersedes the interim "generate clean cloth, no logo at all" idea — the logo is NOT removed, it is composited.
- **Locked brand logo asset added** (`logo_official.png`, exact user upload, 1,079,081 bytes; Drive id `1QZgjplaFWenZHt048tzQntk-L-Ezy_qH`) + transparent derivative (`logo_official_transparent.png`, background-keyed, ink pixels preserved).
- **`scripts/print_logo_on_cloth.py`** added — multiply-blend + brightness-modulation + optional fold displacement so the logo reads as printed, not pasted.
- **MASTER BACKGROUND STANDARD locked** — cloth material + neutral-white color + texture/fold style are canonical and consistent across all catalogs.
- **All images standardized to 1:1 / 2K** (previously 4:5 for lifestyle).
- **Canonical base prompt locked** (user-provided VVS/fidelity wording).
- **Token-optimization rules (10)** locked as highest-priority efficiency layer; cache of Drive IDs documented.
- **Full portable documentation exported** to `docs/` + `NEW_PROJECT.md`, `RECOVERY.md`, `VERSION.md`, `README.md`.
- **Catalogs generated this session:** LR-0156 (round solitaire, bead-set shoulders), LR-0136 (oval + green emeralds), LR-0137 (oval + tapered baguettes).
- **Repo created & pushed:** `SidGajera/Claude_Lucent_Image_Gen` (private, branch `main`).

## Earlier learnings folded in (2026-07-08/09/10)
- **Diamond doubling fix:** enforce single real facet pattern; no CGI kaleidoscope. Benchmark = LR-0156 studio shot.
- **Logo hallucination:** model renders fake logos ("ELLYREID") → never let AI render the logo; composite locally.
- **Lifestyle theme fix:** cozy warm US-home; forbid laptop/desk/office scenes.
- **Model/resolution coercion:** set `params.model:"nano_banana_2"` AND explicit `resolution:"2k"` (default is 1k); server may label the edit path `nano_banana_flash`.
- **Cloth warmth:** fix locally with `whiten_cloth.py` (0 credits), never regenerate for color.
- **Correct source file:** ignore stray/mislabeled images (LR-0167 "Copy of 7/4" belonged to another ring).
- **media_id expiry:** durable cache = Drive file IDs; re-import when rejected.

## v1.0.0 — Initial checkpoint
- Repo initialized; website files committed; `LUCENT_MASTER.md` (merged master spec) + `whiten_cloth.py` added.

## Prior sessions (pre-repo)
- SKUs LR-0160/0162/0164/0165/0166/0167/0168/0190/0191/0192 generated; workflow, diamond standard, cloth/logo rules, lean workflow, and 6-doc consolidation established (captured in `LUCENT_MASTER.md`).
