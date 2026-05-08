from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_binding import (
    build_history_binding_projection,
    build_history_binding_summary,
)


def test_history_binding_builders_smoke() -> None:
    projection = build_history_binding_projection()
    summary = build_history_binding_summary(projection)

    assert summary.source_layer == "history_ingestion"
    assert summary.memory_id == projection.memory_object.memory_id
    assert summary.storage_node_count >= 1
    assert summary.registry_ready is True
    assert summary.dashboard_ready is True
