from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_summary_builder import (
    build_memory_object_summary,
)


def test_memory_object_summary_builder_smoke() -> None:
    obj = build_minimal_memory_object()
    summary = build_memory_object_summary(obj)

    assert summary["memory_id"] == "ARCH-0001"
    assert summary["source_ref"] == "working_chat_memory_track_01"
    assert summary["next_step_id"] == "PHASE3-BATCH1"
