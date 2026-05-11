from __future__ import annotations

import json
from pathlib import Path


def test_mempalace_integrity_security_report_smoke() -> None:
    report_path = Path("EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_integrity_security_report.json")

    assert report_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["official_remote_verified"] is True
    assert report["commit_seen_in_remote_refs"] is True
    assert report["non_empty_project"] is True
    assert report["tracked_file_count"] > 20
    assert report["python_file_count"] > 5
    assert report["required_files_present"]["README.md"] is True
    assert report["required_files_present"]["pyproject.toml"] is True
    assert report["canonical_memory_access"] is False
    assert report["runtime_mutation_allowed"] is False
    assert report["archive_sha256"]
