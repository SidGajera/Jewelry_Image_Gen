#!/usr/bin/env python3
"""CODE PREVIEW BAN — enforced on the print path (user-locked, permanent).

Only per-catalog status / blocker lines reach the console; everything else
(file bodies, diffs, gate detail, shell echoes, paths, tool noise) is routed
to build/run_output.log on disk. This is a filter, not a habit — install() it
at the top of run_catalog.main() so it cannot drift back.

    ALLOWED to console:  ^LR-\\d+: ...     (status)   and   ^LR-\\d+: BLOCKED — ...
    everything else   -> build/run_output.log
"""
import re
import sys
from pathlib import Path

ALLOWED = re.compile(r"^\s*LR-\d{3,}:")


class _Filter:
    def __init__(self, real, logpath):
        self._real = real
        self._buf = ""
        self._log = open(logpath, "a", encoding="utf-8")

    def write(self, s):
        self._buf += s
        while "\n" in self._buf:
            line, self._buf = self._buf.split("\n", 1)
            if ALLOWED.match(line):
                self._real.write(line + "\n"); self._real.flush()
            else:
                self._log.write(line + "\n"); self._log.flush()
        return len(s)

    def flush(self):
        try:
            self._real.flush()
        except Exception:
            pass

    def __getattr__(self, k):
        return getattr(self._real, k)


def install(logdir="build"):
    Path(logdir).mkdir(parents=True, exist_ok=True)
    if not isinstance(sys.stdout, _Filter):
        sys.stdout = _Filter(sys.stdout, str(Path(logdir) / "run_output.log"))
