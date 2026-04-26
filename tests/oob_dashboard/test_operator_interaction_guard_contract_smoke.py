from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_guard_contract import (
    build_operator_interaction_guard_contract,
)


def test_operator_interaction_guard_contract_builds() -> None:
    contract = build_operator_interaction_guard_contract()

    assert len(contract.entries) == 1
    assert contract.entries[0].dashboard_id == "main_operator_dashboard"


def test_operator_interaction_guard_contract_values() -> None:
    contract = build_operator_interaction_guard_contract()
    entry = contract.entries[0]

    assert entry.interaction_surface_id == "main_operator_interaction_surface"
    assert entry.guard_mode == "guarded_operator_interaction"
    assert entry.direct_execution_allowed is False
    assert entry.approval_required is True
    assert entry.policy_gate_required is True
    assert entry.forbidden_state_visible is True
