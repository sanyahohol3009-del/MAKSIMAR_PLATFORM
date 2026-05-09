from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_backend_policy_gate,
    build_retrieval_phase_readiness,
    build_retrieval_preview,
)


def test_retrieval_phase_1_7_no_backend_execution_smoke() -> None:
    preview = build_retrieval_preview()
    backend_gate = build_retrieval_backend_policy_gate()
    readiness = build_retrieval_phase_readiness()

    assert preview["backend_execution_required"] is False
    assert backend_gate.backend_execution_allowed is False
    assert readiness.backend_execution_allowed is False

    for source in preview["selected_sources"]:
        assert source["backend_adapter_required"] is False
