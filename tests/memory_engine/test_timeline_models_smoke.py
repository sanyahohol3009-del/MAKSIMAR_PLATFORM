from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.timeline_models import (
    TimelineEntry,
)


def test_timeline_models_smoke() -> None:
    entry = TimelineEntry(
        timeline_id="TL-ARCH-0001",
        memory_id="ARCH-0001",
        timestamp_utc="2026-05-04T00:00:00Z",
        title="Runtime truth path fixed",
        status="validated",
        timeline_ready=True,
    )

    assert entry.timeline_ready is True
