from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_memory_core_binding_contract,
)


def test_evidence_memory_core_truth_projection_gate_smoke() -> None:
    contract = build_evidence_memory_core_binding_contract()

    assert contract.memory_truth_bindings == contract.total_bindings
    assert contract.knowledge_graph_projection_bindings == contract.total_bindings

    for entry in contract.entries:
        assert entry.memory_truth is True
        assert entry.knowledge_graph_projection_only is True
