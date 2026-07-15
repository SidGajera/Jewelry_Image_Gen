"""Single source of truth for every filesystem path the tool touches.

No other module may build a path independently — import PATHS from here.
Every path is overridable via an environment variable so the app can point
at any mounted/cloud/relative/absolute location without a code change.
"""
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
_DEFAULT_WORKSPACE = REPO_ROOT / "workspace"


def _env_path(var: str, default: Path) -> Path:
    raw = os.getenv(var)
    if not raw:
        return default
    p = Path(raw)
    return p if p.is_absolute() else (REPO_ROOT / p)


class PathConfig:
    def __init__(self):
        self.source_dir = _env_path("SOURCE_DIR", _DEFAULT_WORKSPACE / "source")
        self.reference_dir = _env_path("REFERENCE_DIR", _DEFAULT_WORKSPACE / "reference")
        self.input_dir = _env_path("INPUT_DIR", _DEFAULT_WORKSPACE / "input")
        self.output_dir = _env_path("OUTPUT_DIR", _DEFAULT_WORKSPACE / "output")
        self.cache_dir = _env_path("CACHE_DIR", _DEFAULT_WORKSPACE / "cache")
        self.temp_dir = _env_path("TEMP_DIR", _DEFAULT_WORKSPACE / "temp")
        self.delivery_dir = _env_path("DELIVERY_DIR", _DEFAULT_WORKSPACE / "deliveries")
        # Locked brand assets live in the repo proper, not the scratch workspace.
        self.logo_dir = _env_path("LOGO_DIR", REPO_ROOT / "assets" / "logo")
        self.background_dir = _env_path("BACKGROUND_DIR", REPO_ROOT / "assets" / "background")
        # File-based job state (no SQL database in this tool; each job is one JSON file).
        self.jobs_dir = _env_path("JOBS_DIR", Path(__file__).resolve().parents[2] / "jobs")

    def writable_dirs(self):
        """Dirs the app creates/writes into at runtime (excludes locked asset dirs)."""
        return [
            self.source_dir, self.reference_dir, self.input_dir, self.output_dir,
            self.cache_dir, self.temp_dir, self.delivery_dir, self.jobs_dir,
        ]

    def ensure_dirs(self):
        for d in self.writable_dirs():
            d.mkdir(parents=True, exist_ok=True)

    def as_dict(self):
        return {
            "source_dir": str(self.source_dir),
            "reference_dir": str(self.reference_dir),
            "input_dir": str(self.input_dir),
            "output_dir": str(self.output_dir),
            "cache_dir": str(self.cache_dir),
            "temp_dir": str(self.temp_dir),
            "delivery_dir": str(self.delivery_dir),
            "logo_dir": str(self.logo_dir),
            "background_dir": str(self.background_dir),
            "jobs_dir": str(self.jobs_dir),
        }


PATHS = PathConfig()
