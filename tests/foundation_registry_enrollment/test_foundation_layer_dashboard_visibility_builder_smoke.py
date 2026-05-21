from __future__ import annotations

import json
import subprocess
import sys

import pytest

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_dashboard_visibility_builder import (
    FoundationLayerDashboardVisibilityEntry,
    FoundationLayerDashboardVisibilityReadModel,
    build_foundation_layer_dashboard_visibility_read_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_readiness_summary_builder import (
    build_foundation_layer_readiness_summary_read_model,
)


def test_foundation_layer_dashboard_visibility_is_mandatory_and_read_only() -> None:
    read_model = build_foundation_layer_dashboard_visibility_read_model()

    assert read_model.read_model_id == "foundation_layer_dashboard_visibility_read_model_v1"
    assert read_model.total_layers == 5
    assert read_model.dashboard_visible_layers == 5
    assert read_model.dashboard_visibility_mandatory is True
    assert read_model.all_foundation_layers_dashboard_visible is True
    assert read_model.dashboard_read_only is True
    assert read_model.dashboard_control_allowed is False
    assert read_model.execution_allowed is False
    assert read_model.registry_write_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.preview_tools_read_only is True

    for entry in read_model.visibility_entries:
        assert entry.dashboard_visible is True
        assert entry.dashboard_read_only is True
        assert entry.dashboard_control_allowed is False
        assert entry.execution_allowed is False
        assert entry.registry_write_allowed is False
        assert entry.runtime_mutation_allowed is False


def test_foundation_layer_dashboard_visibility_to_dict_is_non_executing() -> None:
    payload = build_foundation_layer_dashboard_visibility_read_model().to_dict()

    assert payload["dashboard_visibility_mandatory"] is True
    assert payload["all_foundation_layers_dashboard_visible"] is True
    assert payload["dashboard_read_only"] is True
    assert payload["dashboard_control_allowed"] is False
    assert payload["execution_allowed"] is False
    assert payload["registry_write_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["preview_tools_read_only"] is True
    assert len(payload["visibility_entries"]) == 5


def test_foundation_layer_dashboard_visibility_entry_rejects_control() -> None:
    with pytest.raises(ValueError, match="dashboard_control_allowed"):
        FoundationLayerDashboardVisibilityEntry(
            layer_id="security_layer",
            dashboard_visible=True,
            dashboard_read_only=True,
            dashboard_control_allowed=True,
            execution_allowed=False,
            registry_write_allowed=False,
            runtime_mutation_allowed=False,
        )


def test_foundation_layer_dashboard_visibility_summary_rejects_missing_mandatory_visibility() -> None:
    source = build_foundation_layer_readiness_summary_read_model()
    entry = FoundationLayerDashboardVisibilityEntry(
        layer_id="security_layer",
        dashboard_visible=True,
        dashboard_read_only=True,
        dashboard_control_allowed=False,
        execution_allowed=False,
        registry_write_allowed=False,
        runtime_mutation_allowed=False,
    )

    with pytest.raises(ValueError, match="dashboard_visibility_mandatory"):
        FoundationLayerDashboardVisibilityReadModel(
            read_model_id="bad",
            visibility_entries=(entry,),
            source_readiness_summary=source,
            total_layers=1,
            dashboard_visible_layers=1,
            dashboard_visibility_mandatory=False,
            all_foundation_layers_dashboard_visible=True,
            dashboard_read_only=True,
            dashboard_control_allowed=False,
            execution_allowed=False,
            registry_write_allowed=False,
            runtime_mutation_allowed=False,
            preview_tools_read_only=True,
            reason_codes=("bad",),
        )


def test_foundation_registry_enrollment_preview_tool_is_read_only_json() -> None:
    result = subprocess.run(
        [sys.executable, "tools/foundation_registry_enrollment_preview.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["preview_id"] == "foundation_registry_enrollment_preview_v1"
    assert payload["preview_mode"] == "read_only"
    assert payload["registry_write_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["dashboard_control_allowed"] is False
    assert payload["source_read_model"]["total_layers"] == 5


def test_foundation_layer_dashboard_visibility_preview_tool_is_read_only_json() -> None:
    result = subprocess.run(
        [sys.executable, "tools/foundation_layer_dashboard_visibility_preview.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["preview_id"] == "foundation_layer_dashboard_visibility_preview_v1"
    assert payload["preview_mode"] == "read_only"
    assert payload["registry_write_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["dashboard_control_allowed"] is False
    assert payload["source_read_model"]["dashboard_visibility_mandatory"] is True
    assert payload["source_read_model"]["dashboard_visible_layers"] == 5
