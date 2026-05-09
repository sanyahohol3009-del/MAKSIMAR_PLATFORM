from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_bound_memory_phase_readiness,
)


def test_evidence_bound_memory_no_mutation_surface_smoke() -> None:
    readiness = build_evidence_bound_memory_phase_readiness()

    assert readiness.read_only is True
    assert readiness.no_mutation_surface is True
