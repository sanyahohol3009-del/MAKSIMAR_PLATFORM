from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
)


def validate_memory_object_minimum_required_fields(
    memory_object: MemoryObject,
) -> None:
    if not memory_object.panel_ready:
        raise ValueError("memory object must be panel_ready")
    if not memory_object.timeline_ready:
        raise ValueError("memory object must be timeline_ready")
    if not memory_object.filter_ready:
        raise ValueError("memory object must be filter_ready")
