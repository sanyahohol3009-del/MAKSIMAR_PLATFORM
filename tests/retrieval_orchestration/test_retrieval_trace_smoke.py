from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_trace,
)


def test_retrieval_trace_smoke() -> None:
    trace = build_retrieval_trace()

    assert trace.preview_trace_ready is True
    assert trace.policy_gate_passed is True
    assert trace.trace_steps == (
        "query",
        "intent",
        "scope",
        "source_policy",
        "source_selection",
        "evidence_pack",
        "preview_trace",
    )
