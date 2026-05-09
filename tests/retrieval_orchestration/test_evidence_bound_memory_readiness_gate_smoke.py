from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_bound_memory_phase_readiness,
)


def test_evidence_bound_memory_readiness_gate_smoke() -> None:
    readiness = build_evidence_bound_memory_phase_readiness()

    assert readiness.phase_ready is True
    assert readiness.retrieval_phase_ready is True
    assert readiness.evidence_source_chain_ready is True
