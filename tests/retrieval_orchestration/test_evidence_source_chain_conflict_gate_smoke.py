from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_source_chain_contract,
)


def test_evidence_source_chain_conflict_gate_smoke() -> None:
    contract = build_evidence_source_chain_contract()

    assert contract.conflict_marked_items == 0

    for entry in contract.entries:
        assert entry.conflict_marker == ""
