#!/usr/bin/env python3
"""ONE-TIME / OCCASIONAL ref sync (token-optimization, user-locked 2026-07-31).

Problem: fetching pose/studio references from Google Drive every catalog costs
~6k tokens/catalog and breaks whenever a docs/06 Drive ID goes stale (404).

Fix: cache every reference locally ONCE. Per catalog the pipeline reads refs
from refs/ on disk — NO Drive calls, NO media_import_url for refs. Only the
SOURCE piece is imported per SKU.

    python scripts/sync_refs.py            # download all refs, write manifest, prune dead IDs
    python scripts/sync_refs.py --check    # no network; just report manifest coverage

What it does:
  * parses docs/06_CACHE.md ref tables (studio pose, lifestyle wider, lifestyle closeup)
  * downloads each Drive ID -> refs/studio/ or refs/lifestyle/ (redirect-following,
    uc?export=download then thumbnail fallback; validates real image bytes)
  * writes refs/manifest.json: pool + per-category per-slot {slot, local_path, sha256, drive_id}
  * prunes stale IDs from docs/06_CACHE.md and reports exactly what died

The per-slot assignment honors docs/06: studio branded refs may repeat across the
studio slots (fixed branded set); lifestyle slots get DISTINCT refs cycled from the
lifestyle pool. run_catalog --stage prompts hard-fails if any slot is uncovered.
"""
import argparse
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS06 = ROOT / "docs" / "06_CACHE.md"
REFS = ROOT / "refs"
MANIFEST = REFS / "manifest.json"
ANGLE_MATRIX = ROOT / "config" / "angle_matrix.json"

ID_RE = re.compile(r"`([A-Za-z0-9_-]{20,})`")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
IMG_MAGIC = (b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n", b"RIFF", b"GIF8")

# docs/06 section header -> ref group
SECTIONS = [
    ("STUDIO / OFFICE POSE REFERENCES", "studio"),
    ("WIDER SCENE REFERENCES", "lifestyle"),
    ("CLOSE-UP REFERENCES", "lifestyle"),
]


def _sections(text):
    """Return {group: [drive_id,...]} for the ref tables in docs/06 (order-preserving).

    Each ref section is bounded by the NEXT '## ' header (any level-2 heading),
    NOT the next ref-section header — otherwise the last ref section (close-up)
    would sweep every Drive id in the rest of the file (source folders, design
    profiles, logo) into the pool. Only the three ref tables must be read."""
    lines = text.splitlines()
    heads = []
    for i, ln in enumerate(lines):
        for key, grp in SECTIONS:
            if ln.startswith("## ") and key in ln:
                heads.append((i, grp))
    out = {"studio": [], "lifestyle": []}
    for start, grp in heads:
        # end at the next level-2 header after this one
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if lines[j].startswith("## "):
                end = j
                break
        seen = set()
        for ln in lines[start + 1:end]:
            for m in ID_RE.findall(ln):
                if m not in seen:
                    seen.add(m)
                    out[grp].append(m)
    # de-dup across groups, keep first group a given id appears in
    used = set()
    for grp in ("studio", "lifestyle"):
        uniq = []
        for i in out[grp]:
            if i not in used:
                used.add(i)
                uniq.append(i)
        out[grp] = uniq
    return out


def _fetch(drive_id):
    """Return image bytes for a Drive id or None. Tries uc?export=download then
    the thumbnail endpoint (both redirect-followed by urllib)."""
    urls = [
        f"https://drive.google.com/uc?export=download&id={drive_id}",
        f"https://drive.google.com/thumbnail?id={drive_id}&sz=w1600",
    ]
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
        except Exception:
            continue
        if data and any(data.startswith(m) for m in IMG_MAGIC):
            return data
    return None


def _ext(data):
    if data.startswith(b"\x89PNG"):
        return ".png"
    if data.startswith(b"GIF8"):
        return ".gif"
    if data.startswith(b"RIFF"):
        return ".webp"
    return ".jpg"


def _prune_docs06(dead):
    """Remove any docs/06 line that carries a dead Drive id. Returns count removed."""
    if not dead:
        return 0
    text = DOCS06.read_text(encoding="utf-8")
    out, removed = [], 0
    for ln in text.splitlines(keepends=True):
        if any(d in ln for d in dead):
            removed += 1
            continue
        out.append(ln)
    DOCS06.write_text("".join(out), encoding="utf-8")
    return removed


def _slot_groups():
    """{category: [(slot, group), ...]} from the angle matrix."""
    m = json.loads(ANGLE_MATRIX.read_text(encoding="utf-8"))
    return {cat: [(s["slot"], s["group"]) for s in v["slots"]]
            for cat, v in m["categories"].items()}


def sync():
    REFS.mkdir(exist_ok=True)
    (REFS / "studio").mkdir(exist_ok=True)
    (REFS / "lifestyle").mkdir(exist_ok=True)
    ids = _sections(DOCS06.read_text(encoding="utf-8"))
    pool = {"studio": [], "lifestyle": []}
    dead = []
    for grp in ("studio", "lifestyle"):
        for did in ids[grp]:
            data = _fetch(did)
            if not data:
                dead.append(did)
                print(f"  DEAD  {grp:9s} {did}")
                continue
            dest = REFS / grp / f"{did}{_ext(data)}"
            dest.write_bytes(data)
            sha = hashlib.sha256(data).hexdigest()
            pool[grp].append({"drive_id": did, "local_path": str(dest.relative_to(ROOT)).replace("\\", "/"),
                              "sha256": sha, "bytes": len(data)})
            print(f"  ok    {grp:9s} {did} -> {dest.name} ({len(data)} B)")
    if not pool["studio"] or not pool["lifestyle"]:
        sys.exit(f"STOP: empty ref pool (studio={len(pool['studio'])} lifestyle={len(pool['lifestyle'])}); "
                 f"cannot build a usable manifest.")

    # per-slot assignment: studio refs may repeat; lifestyle refs distinct (cycled)
    slot_groups = _slot_groups()
    slots = {}
    for cat, sg in slot_groups.items():
        li = 0
        slots[cat] = {}
        for slot, grp in sg:
            if grp == "studio":
                ref = pool["studio"][0]            # branded set, may repeat
            else:
                ref = pool["lifestyle"][li % len(pool["lifestyle"])]
                li += 1
            slots[cat][slot] = {"slot": slot, "group": grp, "drive_id": ref["drive_id"],
                                "local_path": ref["local_path"], "sha256": ref["sha256"]}

    removed = _prune_docs06(dead)
    # carry forward cached Higgsfield media_ids (never re-import a ref that has one)
    prior = _media_map()
    for grp in pool:
        for e in pool[grp]:
            e["media_id"] = prior.get(e["drive_id"])
    for cat in slots:
        for sl in slots[cat]:
            slots[cat][sl]["media_id"] = prior.get(slots[cat][sl]["drive_id"])
    manifest = {
        "_note": "Locally cached pose/studio references. Per catalog, refs are read from disk "
                 "(no Drive calls, no media_import_url for refs). Regenerate with scripts/sync_refs.py.",
        "source": "docs/06_CACHE.md",
        "pool": pool,
        "slots": slots,
        "pruned_dead_ids": dead,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nwrote {MANIFEST.relative_to(ROOT)} — pool: {len(pool['studio'])} studio + "
          f"{len(pool['lifestyle'])} lifestyle; slots per category: "
          f"{ {c: len(s) for c, s in slots.items()} }")
    if dead:
        print(f"pruned {removed} docs/06 line(s) for {len(dead)} dead id(s): {dead}")
    else:
        print("no dead ids — docs/06 unchanged")
    return manifest


def _media_map():
    """{drive_id: media_id} from the current manifest (empty if none/absent)."""
    if not MANIFEST.exists():
        return {}
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    out = {}
    for grp in man.get("pool", {}).values():
        for e in grp:
            if e.get("media_id"):
                out[e["drive_id"]] = e["media_id"]
    return out


def set_media_id(drive_id, media_id):
    """Persist a Higgsfield media_id for a drive_id across pool + every slot entry.
    Called ONCE after a first import so the ref is never re-imported again."""
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for grp in man.get("pool", {}).values():
        for e in grp:
            if e["drive_id"] == drive_id:
                e["media_id"] = media_id
    for cat in man.get("slots", {}).values():
        for sl in cat.values():
            if sl["drive_id"] == drive_id:
                sl["media_id"] = media_id
    MANIFEST.write_text(json.dumps(man, indent=2), encoding="utf-8")
    return media_id


def media_plan(sku_category="ring"):
    """Per-catalog ref plan with ZERO Drive calls: {slot: {media_id|None, drive_id,
    local_path}}. Slots whose media_id is None still need a ONE-TIME import; the rest
    are reused as-is. run_catalog / the agent reads this instead of importing refs."""
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return man.get("slots", {}).get(sku_category, {})


def check(category=None):
    """No-network coverage check. Returns (ok, missing) for the given category
    (or every category). Used by run_catalog --stage prompts preflight."""
    if not MANIFEST.exists():
        return False, ["<refs/manifest.json missing — run: python scripts/sync_refs.py>"]
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    slot_groups = _slot_groups()
    cats = [category] if category else list(slot_groups.keys())
    missing = []
    for cat in cats:
        have = man.get("slots", {}).get(cat, {})
        for slot, _ in slot_groups.get(cat, []):
            entry = have.get(slot)
            if not entry:
                missing.append(f"{cat}/{slot}:no-entry")
            elif not (ROOT / entry["local_path"]).exists():
                missing.append(f"{cat}/{slot}:file-missing({entry['local_path']})")
    return (not missing), missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="no network; report manifest coverage and exit")
    ap.add_argument("--category", help="limit --check to one category")
    ap.add_argument("--set-media", nargs=2, metavar=("DRIVE_ID", "MEDIA_ID"),
                    help="cache a Higgsfield media_id for a drive_id (one-time, after first import)")
    ap.add_argument("--media-status", action="store_true",
                    help="list drive_ids still missing a cached media_id (need a one-time import)")
    args = ap.parse_args()
    if args.set_media:
        set_media_id(args.set_media[0], args.set_media[1])
        print(f"cached media_id {args.set_media[1]} for {args.set_media[0]}")
        sys.exit(0)
    if args.media_status:
        mm = _media_map()
        man = json.loads(MANIFEST.read_text(encoding="utf-8"))
        allids = {e["drive_id"] for grp in man.get("pool", {}).values() for e in grp}
        need = sorted(allids - set(mm))
        print("all refs have media_id (zero Drive imports needed)" if not need
              else "need one-time import (drive_id -> media_id): " + ", ".join(need))
        sys.exit(0)
    if args.check:
        ok, missing = check(args.category)
        if ok:
            print("refs/manifest.json: all slots covered, all local files present")
            sys.exit(0)
        print("refs/manifest.json INCOMPLETE:")
        for m in missing:
            print(f"  [ ] {m}")
        sys.exit(2)
    sync()


if __name__ == "__main__":
    main()
