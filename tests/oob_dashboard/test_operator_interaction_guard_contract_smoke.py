from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_operator_interaction_guard_contract,
)


def test_operator_interaction_guard_contract_builds() -> None:
    """Operator interaction guard contract should build successfully."""
    contract = build_operator_interaction_guard_contract()

    assert contract.total_entries == 1
    assert contract.allowed_read_only_entries == 0
    assert contract.allowed_with_approval_entries == 1
    assert contract.blocked_direct_execution_entries == 0


def test_operator_interaction_guard_entry() -> None:
    """Operator interaction guard entry should remain canonical."""
    contract = build_operator_interaction_guard_contract()
    entry = contract.entries[0]

    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.interaction_surface == "dashboard_read_model"
    assert entry.guard_decision == "allowed_with_approval"
    assert entry.direct_execution_allowed is False
    assert entry.approval_required_for_mutation is True
