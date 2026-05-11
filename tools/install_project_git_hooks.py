from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path


HOOKS = (
    ".githooks/pre-commit",
    ".githooks/pre-push",
)


def main() -> int:
    hooks_dir = Path(".githooks")
    if not hooks_dir.exists():
        raise FileNotFoundError(".githooks directory missing")

    for hook in HOOKS:
        path = Path(hook)
        if not path.exists():
            raise FileNotFoundError(f"hook missing: {path}")

        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    subprocess.check_call(["git", "config", "core.hooksPath", ".githooks"])

    configured = subprocess.check_output(["git", "config", "core.hooksPath"], text=True).strip()
    if configured != ".githooks":
        raise RuntimeError(f"core.hooksPath not set correctly: {configured}")

    print("OK: MAKSIMAR git hooks installed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
