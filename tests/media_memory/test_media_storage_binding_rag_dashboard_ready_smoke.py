from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_storage_binding_preview,
)


def test_media_storage_binding_rag_dashboard_ready_smoke() -> None:
    preview = build_media_storage_binding_preview()

    assert preview["dashboard_visible_bindings"] == preview["total_bindings"]
    assert preview["retrieval_visible_bindings"] >= 1

    storage_kinds = {entry["storage_entry_kind"] for entry in preview["entries"]}

    assert "media_artifact_store" in storage_kinds
    assert "model_store" in storage_kinds
    assert "artifact_collection" in storage_kinds
    assert "retrieval_index" in storage_kinds
