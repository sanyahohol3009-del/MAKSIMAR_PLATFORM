from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_summary,
)


def test_retrieval_summary_smoke() -> None:
    summary = build_retrieval_summary()

    assert summary["retrieval_summary_ready"] is True
    assert summary["route_ready"] is True
    assert summary["policy_gate_passed"] is True
    assert summary["evidence_item_count"] >= 1
