from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from tools.foundation_roadmap_ci_check import build_ci_report


def test_foundation_roadmap_ci_report_smoke() -> None:
    report = build_ci_report()

    assert report.roadmap_id == "batched_foundation_roadmap_v2_1_correction_patch"
    assert report.version == "2.1"
    assert report.phases_count >= 2
    assert report.batches_count >= 10
    assert "0.2" in report.active_batches
    assert "0.1" in report.closed_batches
    assert report.forbidden_paths_present == ()
    assert report.check_passed is True


def test_foundation_roadmap_ci_check_cli_smoke() -> None:
    tool = Path("tools/foundation_roadmap_ci_check.py")
    assert tool.exists()

    completed = subprocess.run(
        [sys.executable, str(tool)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "FOUNDATION ROADMAP CI CHECK" in completed.stdout
    assert '"check_passed": true' in completed.stdout


def test_foundation_roadmap_ci_check_closed_batch_0_1_required_files_smoke() -> None:
    tool = Path("tools/foundation_roadmap_ci_check.py")
    assert tool.exists()

    completed = subprocess.run(
        [sys.executable, str(tool), "--batch-id", "0.1", "--require-files"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert '"missing_required_files": []' in completed.stdout
    assert '"check_passed": true' in completed.stdout
