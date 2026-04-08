from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_action_queue_panel_contract import (
    OperatorActionQueuePanelEntry,
    build_operator_action_queue_panel_contract,
)


def test_operator_action_queue_panel_contract_builds() -> None:
    """Operator action-queue panel contract should build successfully."""
    contract = build_operator_action_queue_panel_contract()

    assert contract.contract_id == "operator_action_queue_panel_contract_001"
    assert contract.total_entries == 1
    assert contract.operator_visible_entries == 1
    assert contract.read_only_entries == 1


def test_operator_action_queue_panel_contract_contains_expected_entry() -> None:
    """Operator action-queue panel contract should contain expected canonical entry."""
    contract = build_operator_action_queue_panel_contract()
    entry = contract.entries[0]

    assert entry.panel_id == "panel_operator_action_queue_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.interaction_surface_id == "main_operator_interaction_surface_001"
    assert entry.panel_mode == "read_only_action_queue"
    assert entry.panel_status == "action_queue_visible"
    assert entry.total_queue_items == 3
    assert entry.read_only_queue_items == 2
    assert entry.approval_bound_queue_items == 1
    assert entry.handoff_ready_queue_items == 1
    assert entry.operator_visible is True
    assert entry.read_only is True


def test_operator_action_queue_panel_entry_rejects_bad_total() -> None:
    """Action-queue panel entry should reject inconsistent totals."""
    with pytest.raises(ValueError, match="total_queue_items must equal"):
        OperatorActionQueuePanelEntry(
            panel_id="panel_operator_action_queue_invalid",
            workspace_id="workspace_operator_main",
            interaction_surface_id="main_operator_interaction_surface_001",
            panel_mode="read_only_action_queue",
            panel_status="action_queue_visible",
            total_queue_items=3,
            read_only_queue_items=1,
            approval_bound_queue_items=1,
            handoff_ready_queue_items=1,
            operator_visible=True,
            read_only=True,
            description="Invalid action queue total.",
        )
