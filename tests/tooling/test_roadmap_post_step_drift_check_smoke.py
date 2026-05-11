from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_roadmap_post_step_drift_check_tool_smoke() -> None:
    tool = Path("tools/roadmap_post_step_drift_check.py")

    assert tool.exists()

    completed = subprocess.run(
        [sys.executable, str(tool)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "ROADMAP POST-STEP FULL DRIFT CHECK" in completed.stdout
    assert "drift_check_passed" in completed.stdout
