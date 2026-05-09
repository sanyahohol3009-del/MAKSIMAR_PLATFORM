from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_bound_memory_phase_preview,
    build_evidence_bound_memory_phase_readiness,
)


def test_phase_2_1_evidence_bound_memory_ready_smoke() -> None:
    readiness = build_evidence_bound_memory_phase_readiness()
    preview = build_evidence_bound_memory_phase_preview()

    assert readiness.phase_ready is True
    assert preview["phase_ready"] is True
    assert readiness.total_items == preview["total_items"]
    assert readiness.ready_items == readiness.total_items
