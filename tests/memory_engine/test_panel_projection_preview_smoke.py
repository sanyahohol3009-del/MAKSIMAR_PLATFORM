from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.panel_projection_builder import (
    build_panel_projection_preview,
)


def test_panel_projection_preview_smoke() -> None:
    preview = build_panel_projection_preview(build_minimal_memory_object())
    assert preview["panel_ready"] is True
