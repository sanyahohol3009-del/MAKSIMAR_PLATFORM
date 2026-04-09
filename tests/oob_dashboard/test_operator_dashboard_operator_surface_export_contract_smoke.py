from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_operator_surface_export_contract import (
    OperatorDashboardOperatorSurfaceExportEntry,
    build_operator_dashboard_operator_surface_export_contract,
)


def test_operator_dashboard_operator_surface_export_contract_builds() -> None:
    contract = build_operator_dashboard_operator_surface_export_contract()

    assert contract.contract_id == (
        "operator_dashboard_operator_surface_export_contract_001"
    )
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.export_ready_entries == 1
    assert contract.operator_visible_entries == 1


def test_operator_dashboard_operator_surface_export_contract_contains_expected_entry() -> None:
    contract = build_operator_dashboard_operator_surface_export_contract()
    entry = contract.entries[0]

    assert entry.operator_surface_export_id == (
        "operator_dashboard_operator_surface_export_001"
    )
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.operator_surface_export_state == "operator_surface_export_ready"
    assert entry.operator_surface_export_class == "main_operator_surface_export"
    assert entry.system_view_artifact_ready is True
    assert entry.operator_visible is True
    assert entry.truth_bound is True
    assert entry.read_only_boundary is True
    assert entry.oob_safe is True
    assert entry.export_ready is True


def test_operator_dashboard_operator_surface_export_entry_rejects_non_truth_bound() -> None:
    with pytest.raises(ValueError, match="truth_bound must remain true"):
        OperatorDashboardOperatorSurfaceExportEntry(
            operator_surface_export_id="invalid_surface_export",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            operator_surface_export_state="operator_surface_export_ready",
            operator_surface_export_class="main_operator_surface_export",
            system_view_artifact_ready=True,
            operator_visible=True,
            truth_bound=False,
            read_only_boundary=True,
            oob_safe=True,
            export_ready=True,
            description="Invalid operator-surface export entry.",
        )


def test_operator_dashboard_operator_surface_export_entry_rejects_non_read_only_boundary() -> None:
    with pytest.raises(ValueError, match="read_only_boundary must remain true"):
        OperatorDashboardOperatorSurfaceExportEntry(
            operator_surface_export_id="invalid_surface_export",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            operator_surface_export_state="operator_surface_export_ready",
            operator_surface_export_class="main_operator_surface_export",
            system_view_artifact_ready=True,
            operator_visible=True,
            truth_bound=True,
            read_only_boundary=False,
            oob_safe=True,
            export_ready=True,
            description="Invalid operator-surface export entry.",
        )


def test_operator_dashboard_operator_surface_export_entry_rejects_non_export_ready() -> None:
    with pytest.raises(ValueError, match="export_ready must remain true"):
        OperatorDashboardOperatorSurfaceExportEntry(
            operator_surface_export_id="invalid_surface_export",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            operator_surface_export_state="operator_surface_export_ready",
            operator_surface_export_class="main_operator_surface_export",
            system_view_artifact_ready=True,
            operator_visible=True,
            truth_bound=True,
            read_only_boundary=True,
            oob_safe=True,
            export_ready=False,
            description="Invalid operator-surface export entry.",
        )
