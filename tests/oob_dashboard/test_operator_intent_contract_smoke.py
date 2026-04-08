from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_contract import (
    OperatorIntentEntry,
    build_operator_intent_contract,
)


def test_operator_intent_contract_builds() -> None:
    """Operator intent contract should build successfully."""
    contract = build_operator_intent_contract()

    assert contract.total_entries == 3
    assert contract.view_request_entries == 1
    assert contract.navigation_request_entries == 1
    assert contract.control_request_entries == 1
    assert contract.approval_required_entries == 1


def test_operator_intent_contract_contains_expected_entries() -> None:
    """Operator intent contract should contain expected canonical entries."""
    contract = build_operator_intent_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    view_entry = entry_map["operator_intent_001"]
    navigation_entry = entry_map["operator_intent_002"]
    control_entry = entry_map["operator_intent_003"]

    assert view_entry.dashboard_id == "dashboard_main_operator_001"
    assert view_entry.workspace_id == "workspace_operator_main"
    assert view_entry.intent_kind == "view_request"
    assert view_entry.intent_source == "dashboard_operator_surface"
    assert view_entry.intent_status == "intent_only"
    assert view_entry.approval_required is False
    assert view_entry.direct_execution_allowed is False

    assert navigation_entry.intent_kind == "navigation_request"
    assert navigation_entry.approval_required is False
    assert navigation_entry.direct_execution_allowed is False

    assert control_entry.intent_kind == "control_request"
    assert control_entry.approval_required is True
    assert control_entry.direct_execution_allowed is False


def test_operator_intent_contract_preserves_trace_ids() -> None:
    """Operator intent contract should preserve canonical trace ids."""
    contract = build_operator_intent_contract()

    for entry in contract.entries:
        assert entry.trace_id.startswith("trace_operator_intent_")


def test_operator_intent_entry_rejects_blank_operator_intent_id() -> None:
    """Operator intent entry should reject blank operator intent ids."""
    with pytest.raises(ValueError, match="operator_intent_id must be a non-empty string."):
        OperatorIntentEntry(
            operator_intent_id="",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            intent_kind="view_request",
            intent_source="dashboard_operator_surface",
            intent_status="intent_only",
            approval_required=False,
            direct_execution_allowed=False,
            trace_id="trace_operator_intent_invalid",
            description="Invalid operator intent entry.",
        )


def test_operator_intent_entry_rejects_direct_execution() -> None:
    """Operator intent entry should reject direct execution."""
    with pytest.raises(ValueError, match="direct_execution_allowed must remain false"):
        OperatorIntentEntry(
            operator_intent_id="operator_intent_invalid_execution",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            intent_kind="view_request",
            intent_source="dashboard_operator_surface",
            intent_status="intent_only",
            approval_required=False,
            direct_execution_allowed=True,
            trace_id="trace_operator_intent_invalid_execution",
            description="Invalid operator intent entry with direct execution.",
        )


def test_operator_intent_entry_rejects_approval_on_view_request() -> None:
    """View requests must not require approval."""
    with pytest.raises(ValueError, match="view_request and navigation_request intents must not require approval."):
        OperatorIntentEntry(
            operator_intent_id="operator_intent_invalid_view_approval",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            intent_kind="view_request",
            intent_source="dashboard_operator_surface",
            intent_status="intent_only",
            approval_required=True,
            direct_execution_allowed=False,
            trace_id="trace_operator_intent_invalid_view_approval",
            description="Invalid view request with approval requirement.",
        )


def test_operator_intent_entry_rejects_missing_approval_on_control_request() -> None:
    """Control requests must require approval."""
    with pytest.raises(ValueError, match="control_request intents must require approval."):
        OperatorIntentEntry(
            operator_intent_id="operator_intent_invalid_control_approval",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            intent_kind="control_request",
            intent_source="dashboard_operator_surface",
            intent_status="intent_only",
            approval_required=False,
            direct_execution_allowed=False,
            trace_id="trace_operator_intent_invalid_control_approval",
            description="Invalid control request without approval requirement.",
        )
