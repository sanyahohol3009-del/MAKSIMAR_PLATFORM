from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_validators import (
    validate_memory_object_minimum_required_fields,
)


def test_memory_object_minimum_required_fields_ready_smoke() -> None:
    obj = build_minimal_memory_object()
    validate_memory_object_minimum_required_fields(obj)

    assert obj.panel_ready is True
