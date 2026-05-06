from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.timeline_builder import (
    build_timeline_entry,
)


def test_timeline_ready_smoke() -> None:
    entry = build_timeline_entry(build_minimal_memory_object())
    assert entry.timeline_ready is True
