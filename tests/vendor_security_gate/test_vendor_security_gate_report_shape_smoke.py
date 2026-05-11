from __future__ import annotations

import json
from pathlib import Path


def test_vendor_security_gate_report_shape_smoke() -> None:
    report_path = Path("EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_vendor_gate_report.json")

    assert report_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))

    for key in (
        "schema_version",
        "vendor_name",
        "official_remote_verified",
        "commit",
        "commit_seen_in_remote_refs",
        "commit_in_remote_ref_tips",
        "commit_matches_version_lock",
        "version_lock_paths",
        "archive_sha256",
        "tracked_file_count",
        "python_file_count",
        "required_files_present",
        "non_empty_project",
        "external_code_not_committed",
        "risky_static_findings_count",
        "scanner_results",
        "hard_gate_passed",
        "manual_security_review_required",
        "hard_blockers",
        "manual_review_reasons",
    ):
        assert key in report

    assert report["commit_seen_in_remote_refs"] is True
    assert report["commit_matches_version_lock"] is True
    assert report["hard_blockers"] == []
