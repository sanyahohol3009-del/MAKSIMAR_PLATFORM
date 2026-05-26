from __future__ import annotations

import json

from MAKSIMAR_CORE_LIB.readiness_control.readiness_status_read_model import (
    ReadinessEvidenceEntry,
    build_readiness_status_read_model,
)
from tools.project_readiness_control.dashboard_readiness_export import (
    build_dashboard_readiness_payload,
    write_dashboard_readiness_export,
)


def test_dashboard_readiness_export_is_read_only_dashboard_payload(tmp_path) -> None:
    model = build_readiness_status_read_model(
        batch_id="0.7",
        status="READY",
        generated_at_utc="2026-01-01T00:00:00+00:00",
        evidence=(
            ReadinessEvidenceEntry(
                evidence_id="readiness",
                source="project_file_readiness_map",
                status="passed",
                summary="Ready.",
            ),
        ),
    )

    payload = build_dashboard_readiness_payload(model)

    assert payload["schema_version"] == "project_readiness_dashboard_export.v1"
    assert payload["dashboard_safe"] is True
    assert payload["read_only_dashboard"] is True
    assert payload["runtime_mutation_allowed"] is False
    assert payload["canonical_write_allowed"] is False
    assert payload["dashboard_mutation_allowed"] is False
    assert payload["ui_to_execution_allowed"] is False

    output_path = tmp_path / "readiness.json"
    result = write_dashboard_readiness_export(model, output_path=output_path)

    assert result.bytes_written > 0
    assert result.dashboard_safe is True
    assert result.read_only_dashboard is True
    assert output_path.exists()

    written = json.loads(output_path.read_text(encoding="utf-8"))
    assert written["source_model"]["batch_id"] == "0.7"
    assert written["source_model"]["status"] == "READY"
