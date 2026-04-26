from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.action_queue_panel_content_contract import (
    ActionQueuePanelContentEntry,
    build_action_queue_panel_content_contract,
)


def test_action_queue_panel_content_contract_builds() -> None:
    """Action queue panel content contract should build successfully."""
    contract = build_action_queue_panel_content_contract()

    assert contract.contract_id == "action_queue_panel_content_contract_001"
    assert contract.total_entries == 3
    assert contract.read_only_entries == 2
    assert contract.approval_bound_entries == 1
    assert contract.handoff_ready_entries == 3
    assert contract.operator_visible_entries == 3


def test_action_queue_panel_content_contract_contains_expected_entries() -> None:
    """Action queue should preserve read-only and approval-bound semantics."""
    contract = build_action_queue_panel_content_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    assert entry_map["operator_intent_001"].action_queue_class == "read_only_action_entry"
    assert entry_map["operator_intent_001"].intent_kind == "view_request"
    assert entry_map["operator_intent_001"].approval_required is False

    assert entry_map["operator_intent_002"].action_queue_class == "read_only_action_entry"
    assert entry_map["operator_intent_002"].intent_kind == "navigation_request"
    assert entry_map["operator_intent_002"].approval_required is False

    assert entry_map["operator_intent_003"].action_queue_class == "approval_bound_action_entry"
    assert entry_map["operator_intent_003"].intent_kind == "control_request"
    assert entry_map["operator_intent_003"].approval_required is True


def test_action_queue_panel_content_entry_rejects_invalid_approval_bound_flag() -> None:
    """Approval-bound queue entries must require approval."""
    with pytest.raises(
        ValueError,
        match="approval_bound_action_entry must have approval_required=True.",
    ):
        ActionQueuePanelContentEntry(
            action_queue_entry_id="action_queue_entry_invalid",
            operator_intent_id="operator_intent_003",
            dashboard_id="main_operator_dashboard",
            workspace_id="workspace_operator_main",
            action_queue_state="action_queue_ready",
            action_queue_class="approval_bound_action_entry",
            intent_kind="control_request",
            approval_required=False,
            handoff_ready=True,
            operator_visible=True,
            trace_id="trace_operator_intent_003",
            description="Invalid action queue entry.",
        )
