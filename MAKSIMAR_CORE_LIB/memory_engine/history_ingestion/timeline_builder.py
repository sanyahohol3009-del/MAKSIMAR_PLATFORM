from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.timeline_models import (
    TimelineEntry,
)


def build_timeline_entry(memory_object: MemoryObject) -> TimelineEntry:
    return TimelineEntry(
        timeline_id=f"TL-{memory_object.memory_id}",
        memory_id=memory_object.memory_id,
        timestamp_utc=memory_object.source.timestamp_utc,
        title=memory_object.title,
        status=memory_object.status,
        timeline_ready=True,
    )


def build_timeline_preview(memory_object: MemoryObject) -> Dict[str, object]:
    entry = build_timeline_entry(memory_object)
    return {
        "timeline_id": entry.timeline_id,
        "memory_id": entry.memory_id,
        "title": entry.title,
        "status": entry.status,
        "timeline_ready": entry.timeline_ready,
    }
