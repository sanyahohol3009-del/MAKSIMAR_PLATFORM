from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_backend_policy_gate,
)


def test_retrieval_backend_policy_gate_smoke() -> None:
    gate = build_retrieval_backend_policy_gate()

    assert gate.policy_gate_ready is True
    assert gate.backend_execution_allowed is False
    assert gate.approved_backends >= 1
    assert gate.blocked_backends >= 1
    assert gate.total_backends == len(gate.entries)
