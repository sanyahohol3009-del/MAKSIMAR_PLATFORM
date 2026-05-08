from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_binding import (
    build_history_binding_registry_projection,
)


def test_history_binding_registry_projection_smoke() -> None:
    payload = build_history_binding_registry_projection()

    assert payload["source_layer"] == "history_ingestion"
    assert isinstance(payload["storage_node_ids"], tuple)
    assert payload["registry_ready"] is True
    assert payload["readable_by_jarvis"] is True
