from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import os
import pytest


@pytest.mark.skipif(os.environ.get("MAKSIMAR_VENDOR_ONLINE_CHECK") != "1", reason="online vendor remote check is opt-in")
def test_vendor_security_gate_mempalace_smoke() -> None:
    tool = Path("tools/vendor_security_gate.py")
    output = Path("EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_vendor_gate_report.json")

    completed = subprocess.run(
        [
            sys.executable,
            str(tool),
            "--vendor-name",
            "MemPalace",
            "--source-dir",
            "EXTERNAL_BACKENDS/mempalace/source",
            "--expected-remote",
            "https://github.com/MemPalace/mempalace.git",
            "--reports-dir",
            "EXTERNAL_BACKENDS/mempalace/security_reports",
            "--venv-python",
            "EXTERNAL_BACKENDS/mempalace/venv/bin/python",
            "--output",
            str(output),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=900,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert output.exists()

    report = json.loads(output.read_text(encoding="utf-8"))

    assert report["vendor_name"] == "MemPalace"
    assert report["official_remote_verified"] is True
    assert report["commit_seen_in_remote_refs"] is True
    assert report["non_empty_project"] is True
    assert report["external_code_not_committed"] is True
    assert report["canonical_memory_access"] is False
    assert report["runtime_mutation_allowed"] is False
    assert report["hard_gate_passed"] is True
    assert report["manual_security_review_required"] is True
