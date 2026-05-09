from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_source_chain_contract,
)


def test_evidence_source_chain_citation_gate_smoke() -> None:
    contract = build_evidence_source_chain_contract()

    assert contract.citation_required_items == contract.total_items

    for entry in contract.entries:
        assert entry.citation_required is True
