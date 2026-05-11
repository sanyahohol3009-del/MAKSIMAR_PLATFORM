from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_phase_acceptance_runner_help_smoke() -> None:
    tool = Path("tools/phase_acceptance_runner.py")

    completed = subprocess.run(
        [sys.executable, str(tool), "--help"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0
    assert "MAKSIMAR phase acceptance runner" in completed.stdout
