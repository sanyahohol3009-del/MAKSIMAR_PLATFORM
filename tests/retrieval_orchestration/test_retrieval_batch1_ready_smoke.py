from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_preview,
    build_retrieval_route_plan,
    build_retrieval_summary,
)


def test_retrieval_batch1_ready_smoke() -> None:
    route_plan = build_retrieval_route_plan()
    summary = build_retrieval_summary()
    preview = build_retrieval_preview()

    assert route_plan.route_ready is True
    assert summary["retrieval_summary_ready"] is True
    assert preview["preview_ready"] is True
    assert preview["backend_execution_required"] is False
