from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_memory_object_preview,
    build_minimal_memory_object,
)


def test_memory_object_preview_smoke() -> None:
    obj = build_minimal_memory_object()
    preview = build_memory_object_preview(obj)

    assert preview["memory_id"] == "ARCH-0001"
    assert preview["panel_ready"] is True
    assert preview["timeline_ready"] is True
    assert preview["filter_ready"] is True
