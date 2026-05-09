from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy import build_governance_binding_contract


def test_governance_binding_models_smoke() -> None:
    contract = build_governance_binding_contract()

    assert contract.total_bindings >= 1
    assert contract.ready_bindings == contract.total_bindings
    assert contract.approval_required_bindings == contract.total_bindings
    assert contract.controlled_promotion_bindings == contract.total_bindings
    assert contract.auto_promotion_allowed_bindings == 0
    assert contract.conflict_resolution_required_bindings == contract.total_bindings
    assert contract.conflict_detected_bindings == 0
    assert contract.memory_truth_required_bindings == contract.total_bindings
    assert contract.knowledge_graph_projection_bindings == contract.total_bindings
    assert contract.read_only_bindings == contract.total_bindings
