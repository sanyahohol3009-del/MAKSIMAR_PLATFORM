from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.approval_queue_panel_content_contract import (
    ApprovalQueuePanelContentEntry,
    build_approval_queue_panel_content_contract,
)


def test_approval_queue_panel_content_contract_builds() -> None:
    """Approval queue panel content contract should build successfully."""
    contract = build_approval_queue_panel_content_contract()

    assert contract.contract_id == "approval_queue_panel_content_contract_001"
    assert contract.total_entries == 1
    assert contract.pending_approval_entries == 1
    assert contract.handoff_ready_entries == 1
    assert contract.operator_visible_entries == 1


def test_approval_queue_panel_content_contract_contains_expected_entry() -> None:
    """Approval queue should expose only pending approval control requests."""
    contract = build_approval_queue_panel_content_contract()
    entry = contract.entries[0]

    assert entry.operator_intent_id == "operator_intent_003"
    assert entry.intent_kind == "control_request"
    assert entry.pending_approval_visible is True
    assert entry.approval_required is True
    assert entry.handoff_ready is True


def test_approval_queue_panel_content_entry_rejects_non_control_request() -> None:
    """Approval queue entries must remain control requests."""
    with pytest.raises(
        ValueError,
        match="approval queue panel entries must remain limited to control_request.",
    ):
        ApprovalQueuePanelContentEntry(
            approval_queue_entry_id="approval_queue_entry_invalid",
            operator_intent_id="operator_intent_001",
            dashboard_id="main_operator_dashboard",
            workspace_id="workspace_operator_main",
            approval_queue_state="approval_queue_ready",
            approval_queue_class="pending_approval_entry",
            intent_kind="view_request",
            pending_approval_visible=True,
            approval_required=True,
            handoff_ready=True,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Invalid approval queue entry.",
        )
