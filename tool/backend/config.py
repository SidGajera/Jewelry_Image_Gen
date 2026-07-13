"""Load Lucent Carat Lab tool config from the repo's single source of truth.

The web tool never re-invents settings — it reads the same JSON the chat workflow
uses, so behaviour stays identical. Secrets come from tool/.env (git-ignored).
"""
import json
import os
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]      # .../Jewelery-Website
load_dotenv(REPO_ROOT / "tool" / ".env")


def _load(rel: str) -> dict:
    with open(REPO_ROOT / rel, encoding="utf-8") as f:
        return json.load(f)


MANIFEST = _load("config/project_manifest.json")
QUALITY_MEMORY = _load("config/QUALITY_MEMORY.json")

DRIVE_FOLDERS = MANIFEST["drive_folders"]            # source_parent, output, verify_inbox, ...
GEN = MANIFEST["generation_settings"]                # model, resolution, aspect_ratio, counts
IMAGES_PER_CATALOG = GEN["images_per_catalog"]       # {studio:5, lifestyle:4, closeup:3}

SCRIPTS = {
    "composite_ring": REPO_ROOT / "scripts" / "composite_ring_into_scene.py",
    "print_logo":     REPO_ROOT / "scripts" / "print_logo_on_cloth.py",
}
LOGO_ASSET = REPO_ROOT / "assets" / "logo" / "logo_official.png"

# secrets
HIGGSFIELD_API_KEY = os.getenv("HIGGSFIELD_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_CREDS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def require_secrets():
    missing = [k for k, v in {
        "HIGGSFIELD_API_KEY": HIGGSFIELD_API_KEY,
        "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY,
        "GOOGLE_APPLICATION_CREDENTIALS": GOOGLE_CREDS,
    }.items() if not v]
    if missing:
        raise RuntimeError(f"Missing secrets in tool/.env: {', '.join(missing)}")
