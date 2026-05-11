from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_project_git_hooks_exist_and_configured() -> None:
    pre_commit = Path(".githooks/pre-commit")
    pre_push = Path(".githooks/pre-push")

    assert pre_commit.exists()
    assert pre_push.exists()
    assert os.access(pre_commit, os.X_OK)
    assert os.access(pre_push, os.X_OK)

    configured = subprocess.check_output(["git", "config", "core.hooksPath"], text=True).strip()
    assert configured == ".githooks"
