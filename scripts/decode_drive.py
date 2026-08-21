#!/usr/bin/env python3
"""Decode a Drive-connector download_file_content result (saved to a temp file
because it was too large for context) into an image on disk.

    python scripts/decode_drive.py <tool_result_txt> <out_path>

The tool-result file is JSON {content: base64, id, mimeType, title}. Base64
never enters the agent context — it is read from the temp file and written to
<out_path> as raw bytes. Validates image magic.
"""
import base64
import json
import sys
from pathlib import Path

MAGIC = (b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n", b"RIFF", b"GIF8")


def main():
    src, out = sys.argv[1], sys.argv[2]
    d = json.loads(Path(src).read_text(encoding="utf-8"))
    raw = base64.b64decode(d["content"])
    if not any(raw.startswith(m) for m in MAGIC):
        print(f"WARN: {out} does not start with image magic ({raw[:12]!r})")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_bytes(raw)
    print(f"wrote {out}  {len(raw)} bytes  (mime {d.get('mimeType')}, title {d.get('title')})")


if __name__ == "__main__":
    main()
