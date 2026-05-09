from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_source_chain_contract,
)


def test_evidence_source_chain_builder_smoke() -> None:
    contract = build_evidence_source_chain_contract()

    assert contract.total_items >= 1
    assert contract.ready_items == contract.total_items
    assert contract.source_bound_items == contract.total_items
    assert contract.provenance_bound_items == contract.total_items
    assert contract.trace_bound_items == contract.total_items
