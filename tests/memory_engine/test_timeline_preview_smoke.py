from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.timeline_builder import (
    build_timeline_preview,
)


def test_timeline_preview_smoke() -> None:
    preview = build_timeline_preview(build_minimal_memory_object())

    assert preview["memory_id"] == "ARCH-0001"
    assert preview["timeline_ready"] is True
