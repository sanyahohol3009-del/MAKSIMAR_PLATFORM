from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_preview,
)


def test_retrieval_batch2_no_backend_execution_smoke() -> None:
    preview = build_retrieval_preview()

    assert preview["backend_execution_required"] is False
    for source in preview["selected_sources"]:
        assert source["backend_adapter_required"] is False
