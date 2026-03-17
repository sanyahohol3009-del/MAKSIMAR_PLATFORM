#!/usr/bin/env python3
"""
MAKSIMAR Permission Audit Tool
Checks and optionally fixes file permissions.
"""

from pathlib import Path
import os
import stat

ROOT = Path.home() / "MAKSIMAR_PLATFORM"

EXECUTABLE_PY = {
    "stop_gate_watcher.py",
    "stop_gate.py",
}

DATA_EXT = {".json", ".bin", ".log"}


def perm_str(mode):
    return oct(mode & 0o777)


def check_file(path: Path, fix=False):

    mode = path.stat().st_mode
    current = stat.S_IMODE(mode)

    expected = None

    if path.suffix == ".py":

        if path.name in EXECUTABLE_PY:
            expected = 0o755
        else:
            expected = 0o644

    elif path.suffix in DATA_EXT:
        expected = 0o644

    if expected is None:
        return

    if current != expected:

        print(f"[PERM] {path} " f"{perm_str(current)} -> expected {perm_str(expected)}")

        if fix:
            os.chmod(path, expected)
            print(f"[FIX ] applied {perm_str(expected)}")


def scan(fix=False):

    for path in ROOT.rglob("*"):

        if path.is_file():
            check_file(path, fix)


def main():

    import sys

    fix = "--fix" in sys.argv

    print("[PERM] scanning project...")

    scan(fix)

    print("[PERM] done")


if __name__ == "__main__":
    main()
