from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_binding import (
    build_history_binding_dashboard_projection,
)


def test_history_binding_dashboard_projection_smoke() -> None:
    payload = build_history_binding_dashboard_projection()

    assert payload["memory_id"]
    assert payload["title"]
    assert payload["timeline_ready"] is True
    assert payload["panel_ready"] is True
    assert payload["dashboard_ready"] is True
