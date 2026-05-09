from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_bound_memory_phase_readiness,
)


def test_evidence_bound_memory_backend_policy_smoke() -> None:
    readiness = build_evidence_bound_memory_phase_readiness()

    assert readiness.mgrep_blocked is True
    assert readiness.sqlite_vec_blocked is True
    assert readiness.backend_execution_allowed is False
