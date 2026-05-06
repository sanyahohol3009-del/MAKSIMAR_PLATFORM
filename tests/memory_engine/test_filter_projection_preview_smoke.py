from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.filter_projection_builder import (
    build_filter_projection_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)


def test_filter_projection_preview_smoke() -> None:
    preview = build_filter_projection_preview(build_minimal_memory_object())
    assert preview["filter_ready"] is True
