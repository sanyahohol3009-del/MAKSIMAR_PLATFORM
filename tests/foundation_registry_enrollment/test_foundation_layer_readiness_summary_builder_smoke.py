from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_readiness_summary_builder import (
    FoundationLayerReadinessEntry,
    FoundationLayerReadinessSummaryReadModel,
    build_foundation_layer_readiness_summary_read_model,
)


def test_foundation_layer_readiness_summary_covers_all_enrolled_foundation_layers() -> None:
    read_model = build_foundation_layer_readiness_summary_read_model()

    assert read_model.read_model_id == "foundation_layer_readiness_summary_read_model_v1"
    assert read_model.total_layers == 5
    assert read_model.registry_visible_layers == 5
    assert read_model.dashboard_visible_layers == 5
    assert read_model.read_only_layers == 5
    assert read_model.dashboard_safe_layers == 5
    assert read_model.execution_allowed_layers == 0
    assert read_model.all_foundation_layers_ready is True
    assert read_model.all_foundation_layers_registry_visible is True
    assert read_model.all_foundation_layers_dashboard_visible is True
    assert read_model.registry_write_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.dashboard_control_allowed is False
    assert read_model.read_only is True
    assert read_model.dashboard_safe is True

    layer_ids = {entry.layer_id for entry in read_model.readiness_entries}
    assert layer_ids == {
        "security_layer",
        "data_plane",
        "update_recovery_infra",
        "network_containerization",
        "ai_orchestration",
    }


def test_foundation_layer_readiness_summary_to_dict_is_dashboard_safe() -> None:
    payload = build_foundation_layer_readiness_summary_read_model().to_dict()

    assert payload["total_layers"] == 5
    assert payload["registry_visible_layers"] == 5
    assert payload["dashboard_visible_layers"] == 5
    assert payload["execution_allowed_layers"] == 0
    assert payload["registry_write_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["dashboard_control_allowed"] is False
    assert payload["read_only"] is True
    assert payload["dashboard_safe"] is True
    assert len(payload["readiness_entries"]) == 5


def test_foundation_layer_readiness_entry_rejects_execution_allowed() -> None:
    with pytest.raises(ValueError, match="execution_allowed"):
        FoundationLayerReadinessEntry(
            layer_id="bad_layer",
            read_model_id="bad_read_model",
            registry_visible=True,
            dashboard_visible=True,
            existing_surfaces_accounted=True,
            read_only=True,
            dashboard_safe=True,
            registry_write_allowed=False,
            runtime_mutation_allowed=False,
            execution_allowed=True,
        )


def test_foundation_layer_readiness_summary_rejects_wrong_counts() -> None:
    entry = FoundationLayerReadinessEntry(
        layer_id="security_layer",
        read_model_id="security_foundation_enrollment_read_model_v1",
        registry_visible=True,
        dashboard_visible=True,
        existing_surfaces_accounted=True,
        read_only=True,
        dashboard_safe=True,
        registry_write_allowed=False,
        runtime_mutation_allowed=False,
        execution_allowed=False,
    )

    with pytest.raises(ValueError, match="total_layers"):
        FoundationLayerReadinessSummaryReadModel(
            read_model_id="bad",
            readiness_entries=(entry,),
            total_layers=2,
            registry_visible_layers=1,
            dashboard_visible_layers=1,
            read_only_layers=1,
            dashboard_safe_layers=1,
            execution_allowed_layers=0,
            all_foundation_layers_ready=True,
            all_foundation_layers_registry_visible=True,
            all_foundation_layers_dashboard_visible=True,
            registry_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            read_only=True,
            dashboard_safe=True,
            reason_codes=("bad",),
        )
