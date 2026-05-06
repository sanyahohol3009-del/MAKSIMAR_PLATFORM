from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.graph_id_allocator import (
    build_graph_identity_preview,
)


def test_graph_id_allocator_smoke() -> None:
    preview = build_graph_identity_preview()

    assert preview["storage_node_count"] == 3
    assert preview["sample_relation_id"] == "REL-0001"
    assert preview["graph_ready"] is True
