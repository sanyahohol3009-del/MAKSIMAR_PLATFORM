from __future__ import annotations

import json
from pathlib import Path


def test_mempalace_vendor_smoke_report_smoke() -> None:
    report_path = Path("EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_sandbox_smoke_report.json")

    assert report_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["official_source_verified"] is True
    assert report["version_or_commit_pinned"] is True
    assert report["external_code_not_committed"] is True
    assert report["separate_venv"] is True
    assert report["sandbox_data_only"] is True
    assert report["canonical_memory_access"] is False
    assert report["runtime_mutation_allowed"] is False
    assert report["network_access_reviewed"] is True
    assert report["cli_import_smoke_passed"] is True
    assert report["adapter_fake_backend_passed"] is True
    assert report["real_backend_query_smoke_passed"] is True
