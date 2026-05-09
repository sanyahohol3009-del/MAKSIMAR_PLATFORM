from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_memory_core_binding_contract,
)


def test_evidence_memory_core_citation_conflict_gate_smoke() -> None:
    contract = build_evidence_memory_core_binding_contract()

    assert contract.citation_required_bindings == contract.total_bindings
    assert contract.conflict_clear_bindings == contract.total_bindings
