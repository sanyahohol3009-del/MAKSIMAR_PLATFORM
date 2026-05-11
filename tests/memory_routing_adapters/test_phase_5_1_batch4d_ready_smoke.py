from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_phase_5_1_batch4d_ready_smoke() -> None:
    tool = Path("tools/mempalace_controlled_probe.py")
    report_path = Path("EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_controlled_real_backend_probe_report.json")

    if report_path.exists():
        report_path.unlink()

    completed = subprocess.run(
        [sys.executable, str(tool)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert report_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["probe_id"] == "mempalace_controlled_real_backend_probe_001"
    assert report["controlled_probe_success"] is True
    assert report["child_payload"]["network_operations_blocked"] is True
    assert report["child_payload"]["subprocess_operations_blocked"] is True
    assert report["child_payload"]["destructive_filesystem_operations_blocked"] is True
    assert "EXTERNAL_BACKENDS/mempalace/venv/bin/python" in report["venv_python"]
