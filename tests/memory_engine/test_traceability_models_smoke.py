from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.traceability_models import (
    TraceabilityProjection,
)


def test_traceability_models_smoke() -> None:
    projection = TraceabilityProjection(
        memory_id="ARCH-0001",
        source_ref="working_chat_memory_track_01",
        affected_files=("CORE_ROOT/core_guard.py",),
        related_flow_nodes=("HSTORE-RAW-001", "HSTORE-NORM-001"),
        timeline_id="TL-ARCH-0001",
        traceability_ready=True,
    )

    assert projection.traceability_ready is True
