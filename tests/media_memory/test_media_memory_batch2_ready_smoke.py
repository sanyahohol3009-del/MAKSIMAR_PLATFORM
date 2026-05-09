from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_storage_binding_preview,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_media_memory_artifact_routing_binding_preview,
)


def test_media_memory_batch2_ready_smoke() -> None:
    storage_preview = build_media_storage_binding_preview()
    routing_preview = build_media_memory_artifact_routing_binding_preview()

    assert storage_preview["preview_ready"] is True
    assert storage_preview["binding_ready"] is True
    assert routing_preview["preview_ready"] is True
    assert routing_preview["binding_ready"] is True
    assert routing_preview["route_required_entries"] >= 1
