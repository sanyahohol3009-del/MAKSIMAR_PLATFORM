from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_vendor_security_gate_tool_smoke() -> None:
    tool = Path("tools/vendor_security_gate.py")

    assert tool.exists()

    completed = subprocess.run(
        [sys.executable, str(tool), "--help"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0
    assert "Run MAKSIMAR vendor security gate" in completed.stdout
