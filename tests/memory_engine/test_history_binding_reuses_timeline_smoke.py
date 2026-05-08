from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_binding import (
    build_history_binding_projection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.timeline_models import (
    TimelineEntry,
)


def test_history_binding_reuses_timeline_smoke() -> None:
    projection = build_history_binding_projection()

    assert isinstance(projection.timeline_entry, TimelineEntry)
    assert projection.timeline_entry.memory_id == projection.memory_object.memory_id
