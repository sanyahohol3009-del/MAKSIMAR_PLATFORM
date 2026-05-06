from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_id_allocator import (
    build_memory_object_id,
)


def test_memory_id_uniqueness_ready_smoke() -> None:
    first = build_memory_object_id("ARCH", 1)
    second = build_memory_object_id("ARCH", 2)

    assert first.value != second.value
