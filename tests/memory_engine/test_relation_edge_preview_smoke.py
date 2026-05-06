from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.graph_id_allocator import (
    build_graph_identity_preview,
)


def test_relation_edge_preview_smoke() -> None:
    preview = build_graph_identity_preview()

    assert preview["sample_from_id"] == "HSTORE-RAW-001"
    assert preview["sample_to_id"] == "HSTORE-NORM-001"
