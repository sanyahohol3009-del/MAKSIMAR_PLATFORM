from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.graph_id_allocator import (
    build_graph_identity_preview,
)


def test_memory_graph_id_preview_smoke() -> None:
    preview = build_graph_identity_preview()
    assert preview["graph_ready"] is True
