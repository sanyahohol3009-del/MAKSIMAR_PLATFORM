from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_phase_readiness,
)


def test_retrieval_phase_readiness_gate_smoke() -> None:
    readiness = build_retrieval_phase_readiness()

    assert readiness.phase_ready is True
    assert readiness.route_ready is True
    assert readiness.preview_ready is True
    assert readiness.batch2_ready is True
    assert readiness.registry_binding_ready is True
    assert readiness.observability_ready is True
    assert readiness.trace_ready is True
    assert readiness.backend_policy_ready is True
