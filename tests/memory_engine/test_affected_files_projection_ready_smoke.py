from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.panel_projection_builder import (
    build_panel_projection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)


def test_affected_files_projection_ready_smoke() -> None:
    projection = build_panel_projection(build_minimal_memory_object())
    assert len(projection.affected_files) >= 1
