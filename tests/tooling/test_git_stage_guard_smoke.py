from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from tools.git_stage_guard import check_files


def test_git_stage_guard_help_smoke() -> None:
    tool = Path("tools/git_stage_guard.py")

    completed = subprocess.run(
        [sys.executable, str(tool), "--help"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0
    assert "MAKSIMAR git stage guard" in completed.stdout


def test_git_stage_guard_blocks_forbidden_paths() -> None:
    result = check_files(
        (
            ".pymon",
            "EXTERNAL_BACKENDS/mempalace/source/file.py",
            "EXTERNAL_BACKENDS/mempalace/venv/bin/python",
            "tests/runtime_core/test_tmp.py",
        )
    )

    assert result.passed is False
    assert len(result.violations) == 4
