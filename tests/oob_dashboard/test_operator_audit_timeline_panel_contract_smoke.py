from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_timeline_panel_contract import (
    OperatorAuditTimelinePanelEntry,
    build_operator_audit_timeline_panel_contract,
)


def test_operator_audit_timeline_panel_contract_builds() -> None:
    """Operator audit-timeline panel contract should build successfully."""
    contract = build_operator_audit_timeline_panel_contract()

    assert contract.contract_id == "operator_audit_timeline_panel_contract_001"
    assert contract.total_entries == 1
    assert contract.operator_visible_entries == 1
    assert contract.read_only_entries == 1


def test_operator_audit_timeline_panel_contract_contains_expected_entry() -> None:
    """Operator audit-timeline panel contract should contain expected canonical entry."""
    contract = build_operator_audit_timeline_panel_contract()
    entry = contract.entries[0]

    assert entry.panel_id == "panel_operator_audit_timeline_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.panel_mode == "audit_timeline_read_only"
    assert entry.panel_status == "audit_timeline_visible"
    assert entry.total_timeline_items == 3
    assert entry.read_only_timeline_items == 2
    assert entry.approval_bound_timeline_items == 1
    assert entry.blocked_timeline_items == 0
    assert entry.failure_timeline_items == 0
    assert entry.operator_visible is True
    assert entry.read_only is True


def test_operator_audit_timeline_panel_entry_rejects_bad_total() -> None:
    """Audit-timeline panel entry should reject inconsistent totals."""
    with pytest.raises(ValueError, match="total_timeline_items must equal"):
        OperatorAuditTimelinePanelEntry(
            panel_id="panel_operator_audit_timeline_invalid",
            workspace_id="workspace_operator_main",
            panel_mode="audit_timeline_read_only",
            panel_status="audit_timeline_visible",
            total_timeline_items=3,
            read_only_timeline_items=1,
            approval_bound_timeline_items=1,
            blocked_timeline_items=0,
            failure_timeline_items=0,
            operator_visible=True,
            read_only=True,
            description="Invalid audit timeline total.",
        )
