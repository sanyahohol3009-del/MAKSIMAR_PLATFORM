from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_data_plane_web_preview_writes_html(tmp_path: Path) -> None:
    tool = Path("tools/monitor/runtime_input/data_plane_web_preview.py")
    output = tmp_path / "data_plane_preview.html"
    assert tool.exists()

    completed = subprocess.run(
        [sys.executable, str(tool), "--output", str(output)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert output.exists()
    text = output.read_text(encoding="utf-8")
    assert "DATA_PLANE RUNTIME READ MODEL" in text
    assert "Execution from preview" in text
    assert "False" in text
