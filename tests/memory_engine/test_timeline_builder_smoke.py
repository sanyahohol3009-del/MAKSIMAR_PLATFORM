from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.timeline_builder import (
    build_timeline_entry,
)


def test_timeline_builder_smoke() -> None:
    memory_object = build_minimal_memory_object()
    entry = build_timeline_entry(memory_object)

    assert entry.memory_id == "ARCH-0001"
    assert entry.timeline_ready is True
