from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.audit_timeline_panel_content_contract import (
    AuditTimelinePanelContentEntry,
    build_audit_timeline_panel_content_contract,
)


def test_audit_timeline_panel_content_contract_builds() -> None:
    """Audit timeline panel content contract should build successfully."""
    contract = build_audit_timeline_panel_content_contract()

    assert contract.contract_id == "audit_timeline_panel_content_contract_001"
    assert contract.total_entries == 3
    assert contract.audit_visible_entries == 3
    assert contract.approval_required_entries == 1
    assert contract.operator_visible_entries == 3


def test_audit_timeline_panel_content_contract_contains_expected_entries() -> None:
    """Audit timeline should expose canonical operator action audit content."""
    contract = build_audit_timeline_panel_content_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    assert entry_map["operator_intent_001"].intent_kind == "view_request"
    assert entry_map["operator_intent_001"].audit_visible is True
    assert entry_map["operator_intent_001"].approval_required is False

    assert entry_map["operator_intent_002"].intent_kind == "navigation_request"
    assert entry_map["operator_intent_002"].audit_visible is True
    assert entry_map["operator_intent_002"].approval_required is False

    assert entry_map["operator_intent_003"].intent_kind == "control_request"
    assert entry_map["operator_intent_003"].audit_visible is True
    assert entry_map["operator_intent_003"].approval_required is True


def test_audit_timeline_panel_content_entry_rejects_hidden_audit() -> None:
    """Audit timeline entries must remain audit-visible."""
    with pytest.raises(
        ValueError,
        match="audit_visible must remain true for canonical audit timeline entries.",
    ):
        AuditTimelinePanelContentEntry(
            audit_timeline_entry_id="audit_timeline_entry_invalid",
            operator_intent_id="operator_intent_001",
            dashboard_id="main_operator_dashboard",
            workspace_id="workspace_operator_main",
            audit_timeline_state="audit_timeline_ready",
            audit_timeline_class="operator_action_audit_entry",
            intent_kind="view_request",
            audit_visible=False,
            approval_required=False,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Invalid audit timeline entry.",
        )
