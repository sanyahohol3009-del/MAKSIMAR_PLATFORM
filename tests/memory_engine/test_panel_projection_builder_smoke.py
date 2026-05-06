from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.panel_projection_builder import (
    build_panel_projection,
)


def test_panel_projection_builder_smoke() -> None:
    projection = build_panel_projection(build_minimal_memory_object())
    assert projection.memory_id == "ARCH-0001"
