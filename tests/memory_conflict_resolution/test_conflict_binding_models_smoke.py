from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION import (
    build_conflict_binding_contract,
)


def test_conflict_binding_models_smoke() -> None:
    contract = build_conflict_binding_contract()

    assert contract.total_bindings == 2
    assert contract.ready_bindings == contract.total_bindings
    assert contract.evidence_bound_bindings == contract.total_bindings
    assert contract.governance_bound_bindings == contract.total_bindings
    assert contract.approval_required_bindings == contract.total_bindings
    assert contract.approval_granted_bindings == contract.total_bindings
    assert contract.resolved_bindings == contract.total_bindings
