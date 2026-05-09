from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_bound_memory_phase_readiness,
)


def test_evidence_bound_memory_citation_conflict_gate_smoke() -> None:
    readiness = build_evidence_bound_memory_phase_readiness()

    assert readiness.citation_gate_ready is True
    assert readiness.conflict_gate_ready is True
    assert readiness.citation_required_items == readiness.total_items
    assert readiness.conflict_marked_items == 0
