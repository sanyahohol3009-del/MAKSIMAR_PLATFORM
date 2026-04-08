from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_approval_queue_panel_contract import (
    OperatorApprovalQueuePanelEntry,
    build_operator_approval_queue_panel_contract,
)


def test_operator_approval_queue_panel_contract_builds() -> None:
    """Operator approval-queue panel contract should build successfully."""
    contract = build_operator_approval_queue_panel_contract()

    assert contract.contract_id == "operator_approval_queue_panel_contract_001"
    assert contract.total_entries == 1
    assert contract.operator_visible_entries == 1
    assert contract.read_only_entries == 1


def test_operator_approval_queue_panel_contract_contains_expected_entry() -> None:
    """Operator approval-queue panel contract should contain expected canonical entry."""
    contract = build_operator_approval_queue_panel_contract()
    entry = contract.entries[0]

    assert entry.panel_id == "panel_operator_approval_queue_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.panel_mode == "approval_queue_read_only"
    assert entry.panel_status == "approval_queue_visible"
    assert entry.total_queue_items == 3
    assert entry.pending_approval_items == 1
    assert entry.executable_after_approval_items == 1
    assert entry.operator_visible is True
    assert entry.read_only is True


def test_operator_approval_queue_panel_entry_rejects_excess_pending_count() -> None:
    """Approval-queue panel entry should reject pending counts above total."""
    with pytest.raises(ValueError, match="pending_approval_items cannot exceed total_queue_items."):
        OperatorApprovalQueuePanelEntry(
            panel_id="panel_operator_approval_queue_invalid",
            workspace_id="workspace_operator_main",
            panel_mode="approval_queue_read_only",
            panel_status="approval_queue_visible",
            total_queue_items=1,
            pending_approval_items=2,
            executable_after_approval_items=1,
            operator_visible=True,
            read_only=True,
            description="Invalid approval queue pending count.",
        )
