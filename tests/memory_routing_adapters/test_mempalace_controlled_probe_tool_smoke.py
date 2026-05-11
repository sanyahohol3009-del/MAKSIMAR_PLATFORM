from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_mempalace_controlled_probe_tool_smoke() -> None:
    tool = Path("tools/mempalace_controlled_probe.py")

    assert tool.exists()

    completed = subprocess.run(
        [sys.executable, str(tool), "--help"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0
    assert "Run controlled MemPalace real backend probe" in completed.stdout
