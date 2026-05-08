from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_binding import (
    build_history_binding_projection,
)


def test_history_binding_models_smoke() -> None:
    projection = build_history_binding_projection()

    assert projection.source_layer == "history_ingestion"
    assert projection.memory_object.memory_id
    assert projection.storage_nodes
    assert projection.timeline_entry.timeline_ready is True
    assert projection.panel_projection.panel_ready is True
    assert projection.traceability_projection.traceability_ready is True
