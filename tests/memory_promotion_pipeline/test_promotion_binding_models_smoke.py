from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE import (
    build_promotion_binding_contract,
)


def test_promotion_binding_models_smoke() -> None:
    contract = build_promotion_binding_contract()

    assert contract.total_bindings >= 1
    assert contract.ready_bindings == contract.total_bindings
    assert contract.evidence_bound_bindings == contract.total_bindings
    assert contract.governance_bound_bindings == contract.total_bindings
    assert contract.approval_required_bindings == contract.total_bindings
    assert contract.auto_promotion_allowed_bindings == 0
    assert contract.controlled_promotion_bindings == contract.total_bindings
    assert contract.read_only_bindings == contract.total_bindings
