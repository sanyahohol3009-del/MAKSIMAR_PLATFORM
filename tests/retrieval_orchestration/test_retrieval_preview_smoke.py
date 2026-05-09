from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_preview,
)


def test_retrieval_preview_smoke() -> None:
    preview = build_retrieval_preview()

    assert preview["preview_ready"] is True
    assert preview["route_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["preview_trace_ready"] is True
    assert preview["flow"] == (
        "query",
        "intent",
        "domain_scope",
        "policy_gate",
        "source_priority",
        "retrieval_source",
        "evidence_pack",
        "preview_trace",
    )
