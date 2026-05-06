from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)


def test_memory_object_builder_smoke() -> None:
    obj = build_minimal_memory_object()

    assert obj.memory_id == "ARCH-0001"
    assert obj.memory_type == "architecture_decision"
    assert obj.status == "validated"
