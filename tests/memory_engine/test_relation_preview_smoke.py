from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_builders import (
    build_relation_preview,
)


def test_relation_preview_smoke() -> None:
    preview = build_relation_preview(build_minimal_memory_object())

    assert preview["relation_count"] == 2
    assert preview["graph_ready"] is True
