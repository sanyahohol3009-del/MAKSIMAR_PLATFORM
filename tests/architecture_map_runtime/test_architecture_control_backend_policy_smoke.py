from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_architecture_control_phase_readiness,
)


def test_architecture_control_backend_policy_smoke() -> None:
    readiness = build_architecture_control_phase_readiness()

    assert readiness.mgrep_blocked is True
    assert readiness.sqlite_vec_blocked is True
    assert readiness.retrieval_ready is True
