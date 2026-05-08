from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_binding import (
    build_history_binding_preview_dict,
)


def test_history_binding_ready_smoke() -> None:
    payload = build_history_binding_preview_dict()

    assert payload["status"] == "ready"
    assert payload["registry_projection"]["registry_ready"] is True
    assert payload["dashboard_projection"]["dashboard_ready"] is True
    assert payload["traceability_projection"]["traceability_ready"] is True
