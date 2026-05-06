from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_memory_object_preview,
    build_minimal_memory_object,
)


def test_memory_object_minimal_fields_preview_smoke() -> None:
    obj = build_minimal_memory_object()
    preview = build_memory_object_preview(obj)

    assert preview["affects_count"] == 2
    assert preview["project_area_count"] == 2
    assert preview["tag_count"] == 3
