from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_storage_binding_preview,
)


def test_media_storage_binding_preview_smoke() -> None:
    preview = build_media_storage_binding_preview()

    assert preview["preview_ready"] is True
    assert preview["binding_ready"] is True
    assert preview["total_bindings"] == len(preview["entries"])
    assert preview["storage_ready_bindings"] == preview["total_bindings"]
    assert preview["binary_external_bindings"] == preview["total_bindings"]
    assert preview["flow"] == (
        "media_memory_read_model",
        "storage_registry_lookup",
        "storage_binding_contract",
        "dashboard_rag_read_only_preview",
    )
