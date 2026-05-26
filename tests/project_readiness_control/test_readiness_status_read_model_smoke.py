from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.readiness_control.readiness_status_read_model import (
    ReadinessEvidenceEntry,
    ReadinessStatusReadModel,
    build_readiness_status_read_model,
)


def test_readiness_status_read_model_is_dashboard_safe_and_read_only() -> None:
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
            ReadinessEvidenceEntry(
                evidence_id="dirty",
                source="dirty_surface_classifier",
                status="warning",
                summary="Unrelated dirty surfaces remain visible.",
            ),
        ),
    )

    payload = model.to_dict()

    assert model.evidence_count == 2
    assert model.passed_count == 1
    assert model.warning_count == 1
    assert payload["dashboard_safe"] is True
    assert payload["read_only"] is True
    assert payload["runtime_mutation_allowed"] is False
    assert payload["canonical_write_allowed"] is False
    assert payload["dashboard_mutation_allowed"] is False
    assert payload["ui_to_execution_allowed"] is False


def test_readiness_status_read_model_blocks_execution_flags() -> None:
    with pytest.raises(ValueError, match="ui_to_execution_allowed"):
        ReadinessStatusReadModel(
            schema_version="readiness_status_read_model.v1",
            model_id="bad",
            batch_id="0.7",
            status="READY",
            generated_at_utc="2026-01-01T00:00:00+00:00",
            evidence=(),
            ui_to_execution_allowed=True,
        )
