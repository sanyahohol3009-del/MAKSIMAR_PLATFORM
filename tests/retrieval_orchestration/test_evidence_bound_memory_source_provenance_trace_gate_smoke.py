from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_bound_memory_phase_readiness,
)


def test_evidence_bound_memory_source_provenance_trace_gate_smoke() -> None:
    readiness = build_evidence_bound_memory_phase_readiness()

    assert readiness.source_bound_ready is True
    assert readiness.provenance_bound_ready is True
    assert readiness.trace_bound_ready is True
    assert readiness.source_bound_items == readiness.total_items
    assert readiness.provenance_bound_items == readiness.total_items
    assert readiness.trace_bound_items == readiness.total_items
