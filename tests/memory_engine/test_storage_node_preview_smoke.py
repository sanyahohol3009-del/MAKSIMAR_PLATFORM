from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_builder import (
    build_default_storage_nodes,
    build_storage_node_preview,
)


def test_storage_node_preview_smoke() -> None:
    node = build_default_storage_nodes()[0]
    preview = build_storage_node_preview(node)

    assert preview["storage_node_id"] == "HSTORE-RAW-001"
    assert preview["storage_node_type"] == "raw_archive_store"
    assert preview["portable"] is True
