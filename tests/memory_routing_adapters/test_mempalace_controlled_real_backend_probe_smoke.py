from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_mempalace_controlled_real_backend_probe_smoke(tmp_path: Path) -> None:
    tool = Path("tools/mempalace_controlled_probe.py")
    report_path = tmp_path / "mempalace_controlled_real_backend_probe_report.json"

    completed = subprocess.run(
        [sys.executable, str(tool), "--output-report", str(report_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert report_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["controlled_probe_success"] is True
    assert report["backend_subprocess_allowed"] is False
    assert report["backend_network_allowed"] is False
    assert report["backend_destructive_filesystem_allowed"] is False
    assert report["canonical_write_allowed"] is False
    assert report["runtime_mutation_allowed"] is False
    assert report["full_real_backend_enablement_allowed"] is False
    assert report["general_real_backend_query_allowed"] is False
    assert report["child_payload"]["import_success"] is True
    assert report["child_payload"]["denied_env_present_after_scrub"] == []
