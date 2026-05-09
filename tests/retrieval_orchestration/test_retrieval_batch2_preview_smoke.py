from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_batch2_preview,
)


def test_retrieval_batch2_preview_smoke() -> None:
    preview = build_retrieval_batch2_preview()

    assert preview["preview_ready"] is True
    assert preview["batch2_ready"] is True
    assert preview["retrieval_preview_ready"] is True
    assert preview["retrieval_route_ready"] is True
    assert preview["registry_binding_ready"] is True
    assert preview["observability_ready"] is True
    assert preview["trace_binding_ready"] is True
