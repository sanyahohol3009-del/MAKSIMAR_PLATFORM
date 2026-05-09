from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_batch2_preview,
    build_retrieval_observability_binding,
    build_retrieval_registry_binding_contract,
)


def test_retrieval_batch2_ready_smoke() -> None:
    registry_binding = build_retrieval_registry_binding_contract()
    observability_binding = build_retrieval_observability_binding()
    preview = build_retrieval_batch2_preview()

    assert registry_binding.binding_ready is True
    assert observability_binding.observability_ready is True
    assert preview["batch2_ready"] is True
