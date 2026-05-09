from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION import (
    build_conflict_binding_contract,
)


def test_conflict_governance_binding_ready_smoke() -> None:
    contract = build_conflict_binding_contract()

    assert contract.governance_bound_bindings == contract.total_bindings
    assert contract.memory_truth_required_bindings == contract.total_bindings
    assert contract.knowledge_graph_projection_bindings == contract.total_bindings
    assert contract.read_only_bindings == contract.total_bindings
