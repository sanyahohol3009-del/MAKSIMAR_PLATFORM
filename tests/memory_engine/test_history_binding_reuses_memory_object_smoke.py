from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_binding import (
    build_history_binding_projection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
)


def test_history_binding_reuses_memory_object_smoke() -> None:
    projection = build_history_binding_projection()

    assert isinstance(projection.memory_object, MemoryObject)
