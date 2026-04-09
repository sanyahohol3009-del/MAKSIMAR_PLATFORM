from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_final_assembled_state_contract import (
    OperatorDashboardFinalAssembledStateEntry,
    build_operator_dashboard_final_assembled_state_contract,
)


def test_operator_dashboard_final_assembled_state_contract_builds() -> None:
    """Operator dashboard final assembled-state contract should build successfully."""
    contract = build_operator_dashboard_final_assembled_state_contract()

    assert contract.contract_id == (
        "operator_dashboard_final_assembled_state_contract_001"
    )
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1
    assert contract.truth_bound_entries == 1
    assert contract.system_view_artifact_ready_entries == 1


def test_operator_dashboard_final_assembled_state_contract_contains_expected_entry() -> None:
    """Final assembled-state contract should contain expected canonical entry."""
    contract = build_operator_dashboard_final_assembled_state_contract()
    entry = contract.entries[0]

    assert entry.assembled_state_id == (
        "operator_dashboard_final_assembled_state_001"
    )
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.assembled_state == "final_assembled_state_ready"
    assert entry.assembled_class == "main_operator_final_assembled_state"
    assert entry.interaction_surface_ready is True
    assert entry.visible_output_ready is True
    assert entry.first_real_picture_ready is True
    assert entry.system_view_artifact_ready is True
    assert entry.operator_visible is True
    assert entry.truth_bound is True
    assert entry.read_only_boundary is True
    assert entry.oob_safe is True


def test_operator_dashboard_final_assembled_state_entry_rejects_non_truth_bound() -> None:
    """Final assembled-state entries must remain truth-bound."""
    with pytest.raises(ValueError, match="truth_bound must remain true"):
        OperatorDashboardFinalAssembledStateEntry(
            assembled_state_id="operator_dashboard_final_assembled_state_invalid",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_main_operator_001",
            assembled_state="final_assembled_state_ready",
            assembled_class="main_operator_final_assembled_state",
            interaction_surface_ready=True,
            visible_output_ready=True,
            first_real_picture_ready=True,
            system_view_artifact_ready=True,
            operator_visible=True,
            truth_bound=False,
            read_only_boundary=True,
            oob_safe=True,
            description="Invalid final assembled-state entry.",
        )


def test_operator_dashboard_final_assembled_state_entry_rejects_non_read_only_boundary() -> None:
    """Final assembled-state entries must remain read-only at the boundary."""
    with pytest.raises(ValueError, match="read_only_boundary must remain true"):
        OperatorDashboardFinalAssembledStateEntry(
            assembled_state_id="operator_dashboard_final_assembled_state_invalid",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_main_operator_001",
            assembled_state="final_assembled_state_ready",
            assembled_class="main_operator_final_assembled_state",
            interaction_surface_ready=True,
            visible_output_ready=True,
            first_real_picture_ready=True,
            system_view_artifact_ready=True,
            operator_visible=True,
            truth_bound=True,
            read_only_boundary=False,
            oob_safe=True,
            description="Invalid final assembled-state entry.",
        )


def test_operator_dashboard_final_assembled_state_entry_rejects_non_oob_safe() -> None:
    """Final assembled-state entries must remain OOB-safe."""
    with pytest.raises(ValueError, match="oob_safe must remain true"):
        OperatorDashboardFinalAssembledStateEntry(
            assembled_state_id="operator_dashboard_final_assembled_state_invalid",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_main_operator_001",
            assembled_state="final_assembled_state_ready",
            assembled_class="main_operator_final_assembled_state",
            interaction_surface_ready=True,
            visible_output_ready=True,
            first_real_picture_ready=True,
            system_view_artifact_ready=True,
            operator_visible=True,
            truth_bound=True,
            read_only_boundary=True,
            oob_safe=False,
            description="Invalid final assembled-state entry.",
        )


def test_operator_dashboard_final_assembled_state_entry_rejects_not_artifact_ready() -> None:
    """Final assembled-state entries must remain ready for system-view artifact handoff."""
    with pytest.raises(ValueError, match="system_view_artifact_ready must remain true"):
        OperatorDashboardFinalAssembledStateEntry(
            assembled_state_id="operator_dashboard_final_assembled_state_invalid",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_main_operator_001",
            assembled_state="final_assembled_state_ready",
            assembled_class="main_operator_final_assembled_state",
            interaction_surface_ready=True,
            visible_output_ready=True,
            first_real_picture_ready=True,
            system_view_artifact_ready=False,
            operator_visible=True,
            truth_bound=True,
            read_only_boundary=True,
            oob_safe=True,
            description="Invalid final assembled-state entry.",
        )
