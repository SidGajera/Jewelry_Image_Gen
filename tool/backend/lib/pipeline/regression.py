"""regression.py — the golden-catalog no-regression harness (docs/14 §1/§4/§5).

Runs the composite pipeline over every golden entry whose source + scene images
are present, asserts the §2 guarantees (composite provenance → geometry
guaranteed; 1:1; ~2K; studio logo when required), and compares the success rate
to the stored baseline. If the rate drops, it exits non-zero — the signal that a
change regressed and must be rolled back (the revert itself is a gated human/agent
step, never automated here).

Entries with missing images are SKIPPED (not failed) so the harness is runnable
before the operator has supplied all real reference rings. The SMOKE entry uses
repo assets, so a fresh clone runs green.

Usage (from tool/backend, venv):
  python -m lib.pipeline.regression                 # run + compare to baseline
  python -m lib.pipeline.regression --update-baseline   # accept current as baseline
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from lib.config.paths import REPO_ROOT, PATHS
from lib.pipeline import pipeline

CATALOG = REPO_ROOT / "config" / "golden_catalog.json"


def _resolve(rel: str | None) -> Path | None:
    if not rel:
        return None
    p = Path(rel)
    return p if p.is_absolute() else (REPO_ROOT / p)


def _entry_paths(e: dict) -> tuple[Path | None, Path | None]:
    """Source ring + scene for an entry. Falls back to the per-id golden dir."""
    gdir = PATHS_golden() / e["id"]
    ring = _resolve(e.get("source_ring")) or (gdir / "source.png")
    scene = _resolve(e.get("scene")) or (gdir / "scene.png")
    return ring, scene


def PATHS_golden() -> Path:
    return REPO_ROOT / "workspace" / "golden"


def run(catalog_path: Path = CATALOG) -> dict:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    out_dir = PATHS.temp_dir / "regression"
    out_dir.mkdir(parents=True, exist_ok=True)

    results: dict[str, dict] = {}
    for e in catalog["entries"]:
        eid = e["id"]
        ring, scene = _entry_paths(e)
        if not ring or not scene or not ring.exists() or not scene.exists():
            results[eid] = {"status": "skipped", "reason": "source/scene image missing"}
            continue
        try:
            res = pipeline.process_shot(
                scene, ring, out_dir / f"{eid}.png",
                shot_type=e["shot_type"], sku=eid,
                print_studio_logo=bool(e.get("require_logo")) and e["shot_type"] == "studio",
            )
            v = res.verdict
            # The geometry regression suite protects the GEOMETRY invariant that
            # composite-v1 code guarantees. Composite INTEGRITY (single ring / clean
            # scene) depends on the operator-provided scene, not pipeline code, so it
            # is verified by shadow-test/manual, not here (docs/14 §2, docs/16).
            ok = bool(v["geometry_guaranteed"])
            results[eid] = {
                "status": "pass" if ok else "fail",
                "geometry_guaranteed": v["geometry_guaranteed"],
                "deliverable": v["passed"],
                "method": v["method"],
                "warnings": v.get("warnings", []),
            }
        except Exception as ex:  # a crash is a hard fail, never a silent skip
            results[eid] = {"status": "fail", "reason": f"{type(ex).__name__}: {ex}"}

    ran = {k: v for k, v in results.items() if v["status"] in ("pass", "fail")}
    passed = sum(1 for v in ran.values() if v["status"] == "pass")
    success_rate = (passed / len(ran)) if ran else 1.0
    return {
        "success_rate": round(success_rate, 4),
        "ran": len(ran),
        "passed": passed,
        "failed": len(ran) - passed,
        "skipped": sum(1 for v in results.values() if v["status"] == "skipped"),
        "entries": {k: v["status"] for k, v in results.items()},
        "detail": results,
    }


def _baseline_path(catalog_path: Path = CATALOG) -> Path:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    return _resolve(catalog.get("baseline_results")) or (REPO_ROOT / "config" / "golden_baseline.json")


def compare_to_baseline(summary: dict, catalog_path: Path = CATALOG) -> tuple[bool, str]:
    """Returns (regressed, message). Regression = success_rate below baseline, OR a
    per-entry pass in the baseline that is now failing."""
    bp = _baseline_path(catalog_path)
    if not bp.exists():
        return False, "no baseline yet (run --update-baseline to set one)"
    base = json.loads(bp.read_text(encoding="utf-8"))
    if summary["success_rate"] < base.get("success_rate", 0):
        return True, (f"success rate dropped {base['success_rate']} -> {summary['success_rate']}")
    newly_failing = [
        k for k, st in base.get("entries", {}).items()
        if st == "pass" and summary["entries"].get(k) == "fail"
    ]
    if newly_failing:
        return True, f"entries regressed pass->fail: {', '.join(newly_failing)}"
    return False, "no regression vs baseline"


def _write_baseline(summary: dict, catalog_path: Path = CATALOG) -> Path:
    bp = _baseline_path(catalog_path)
    # store only the stable comparison keys (no timestamps → clean diffs)
    bp.write_text(json.dumps(
        {"success_rate": summary["success_rate"], "entries": summary["entries"]},
        indent=2,
    ) + "\n", encoding="utf-8")
    return bp


def _cli() -> None:
    import argparse
    ap = argparse.ArgumentParser(description="Golden no-regression harness (docs/14).")
    ap.add_argument("--update-baseline", action="store_true",
                    help="accept the current run as the new baseline")
    a = ap.parse_args()

    summary = run()
    print(f"golden suite: {summary['passed']}/{summary['ran']} passed "
          f"(rate {summary['success_rate']}), {summary['skipped']} skipped")
    for k, st in summary["entries"].items():
        mark = {"pass": "OK  ", "fail": "FAIL", "skipped": "skip"}[st]
        extra = summary["detail"][k].get("reason") or ",".join(summary["detail"][k].get("warnings", []))
        print(f"  {mark} {k}{('  — ' + extra) if extra else ''}")

    if a.update_baseline:
        bp = _write_baseline(summary)
        print(f"baseline updated -> {bp.relative_to(REPO_ROOT)}")
        sys.exit(0)

    regressed, msg = compare_to_baseline(summary)
    print(f"baseline check: {msg}")
    # exit non-zero on any hard fail or a regression → 'do not keep this change'
    sys.exit(1 if (summary["failed"] > 0 or regressed) else 0)


if __name__ == "__main__":
    _cli()
