from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_operator_intent_contract,
)


def test_operator_intent_contract_builds() -> None:
    """Operator intent contract should build successfully."""
    contract = build_operator_intent_contract()

    assert contract.total_entries == 1
    assert contract.read_only_navigation_entries == 0
    assert contract.guarded_operator_mutation_entries == 1
    assert contract.approval_required_entries == 1


def test_operator_intent_entry() -> None:
    """Operator intent entry should remain canonical."""
    contract = build_operator_intent_contract()
    entry = contract.entries[0]

    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.intent_kind == "guarded_operator_mutation"
    assert entry.intent_source == "dashboard_operator_surface"
    assert entry.intent_status == "intent_only"
    assert entry.approval_required is True
    assert entry.direct_execution_allowed is False
