from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_batch2_preview,
)


def test_retrieval_batch2_flow_smoke() -> None:
    preview = build_retrieval_batch2_preview()

    assert preview["flow"] == (
        "retrieval_preview",
        "memory_registry_binding",
        "global_registry_binding",
        "ai_router_binding",
        "memory_skill_metrics_binding",
        "observability_preview",
    )
