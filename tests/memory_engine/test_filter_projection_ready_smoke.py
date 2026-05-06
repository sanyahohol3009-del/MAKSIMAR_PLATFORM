from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.filter_projection_builder import (
    build_filter_projection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)


def test_filter_projection_ready_smoke() -> None:
    projection = build_filter_projection(build_minimal_memory_object())
    assert projection.filter_ready is True
