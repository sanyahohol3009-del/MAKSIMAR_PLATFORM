from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_interaction_surface_contract import (
    MainOperatorInteractionSurfaceEntry,
    build_main_operator_interaction_surface_contract,
)


def test_main_operator_interaction_surface_contract_builds() -> None:
    """Main-operator interaction surface contract should build successfully."""
    contract = build_main_operator_interaction_surface_contract()

    assert contract.contract_id == "main_operator_interaction_surface_contract_001"
    assert contract.total_entries == 1
    assert contract.read_only_surface_entries == 0
    assert contract.approval_bound_surface_entries == 1
    assert contract.operator_visible_entries == 1


def test_main_operator_interaction_surface_contract_contains_expected_entry() -> None:
    """Main-operator interaction surface contract should contain expected canonical entry."""
    contract = build_main_operator_interaction_surface_contract()
    entry = contract.entries[0]

    assert entry.interaction_surface_id == "main_operator_interaction_surface_001"
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.interaction_surface_mode == "approval_bound_operator_surface"
    assert entry.interaction_surface_status == "interaction_surface_assembled"
    assert entry.total_interaction_entries == 3
    assert entry.read_only_lane_entries == 2
    assert entry.approval_bound_lane_entries == 1
    assert entry.handoff_ready_entries == 1
    assert entry.operator_visible is True
    assert entry.read_only_surface is False


def test_main_operator_interaction_surface_entry_rejects_blank_id() -> None:
    """Main-operator interaction surface entry should reject blank ids."""
    with pytest.raises(ValueError, match="interaction_surface_id must be a non-empty string."):
        MainOperatorInteractionSurfaceEntry(
            interaction_surface_id="",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            interaction_surface_mode="approval_bound_operator_surface",
            interaction_surface_status="interaction_surface_assembled",
            total_interaction_entries=3,
            read_only_lane_entries=2,
            approval_bound_lane_entries=1,
            handoff_ready_entries=1,
            operator_visible=True,
            read_only_surface=False,
            description="Invalid interaction surface entry.",
        )


def test_main_operator_interaction_surface_entry_rejects_read_only_flag_on_approval_surface() -> None:
    """Approval-bound surfaces must not mark read_only_surface true."""
    with pytest.raises(ValueError, match="approval_bound_operator_surface entries must not mark read_only_surface=True."):
        MainOperatorInteractionSurfaceEntry(
            interaction_surface_id="main_operator_interaction_surface_invalid",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            interaction_surface_mode="approval_bound_operator_surface",
            interaction_surface_status="interaction_surface_assembled",
            total_interaction_entries=3,
            read_only_lane_entries=2,
            approval_bound_lane_entries=1,
            handoff_ready_entries=1,
            operator_visible=True,
            read_only_surface=True,
            description="Invalid read-only flag on approval-bound interaction surface.",
        )
