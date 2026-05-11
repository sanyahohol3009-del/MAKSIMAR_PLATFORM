from __future__ import annotations

from pathlib import Path


def test_mempalace_security_reports_exist_smoke() -> None:
    root = Path("EXTERNAL_BACKENDS/mempalace/security_reports")

    assert (root / "mempalace_integrity_security_report.json").exists()
    assert (root / "mempalace_bandit_report.json").exists()
    assert (root / "mempalace_pip_audit_report.json").exists()
    assert (root / "mempalace_clamscan_report.txt").exists()
