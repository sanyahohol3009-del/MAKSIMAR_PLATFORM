from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_data_plane_terminal_preview_outputs_read_only_state() -> None:
    tool = Path("tools/monitor/runtime_input/data_plane_terminal_preview.py")
    assert tool.exists()

    completed = subprocess.run(
        [sys.executable, str(tool)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "DATA_PLANE RUNTIME READ MODEL" in completed.stdout
    assert "dashboard_safe: True" in completed.stdout
    assert "execution_allowed_from_preview: False" in completed.stdout
