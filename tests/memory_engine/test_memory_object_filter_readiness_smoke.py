from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)


def test_memory_object_filter_readiness_smoke() -> None:
    obj = build_minimal_memory_object()
    assert obj.filter_ready is True
