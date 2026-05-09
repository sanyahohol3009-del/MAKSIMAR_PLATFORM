from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_memory_preview,
    build_media_storage_binding_preview,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_media_memory_artifact_routing_binding_preview,
)


def test_media_memory_storage_artifact_flow_ready_smoke() -> None:
    media_preview = build_media_memory_preview()
    storage_preview = build_media_storage_binding_preview()
    routing_preview = build_media_memory_artifact_routing_binding_preview()

    assert media_preview["media_memory_ready"] is True
    assert storage_preview["binding_ready"] is True
    assert routing_preview["binding_ready"] is True
    assert storage_preview["total_bindings"] == media_preview["total_records"]
    assert routing_preview["total_entries"] == media_preview["total_records"]
