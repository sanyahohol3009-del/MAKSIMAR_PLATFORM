from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_binding import (
    build_history_binding_preview,
    build_history_binding_preview_dict,
)


def test_history_binding_preview_builder_smoke() -> None:
    preview = build_history_binding_preview()
    payload = build_history_binding_preview_dict()

    assert preview.status == "ready"
    assert payload["status"] == "ready"
    assert payload["summary"]["source_layer"] == "history_ingestion"
    assert payload["summary"]["registry_ready"] is True
    assert payload["summary"]["dashboard_ready"] is True
