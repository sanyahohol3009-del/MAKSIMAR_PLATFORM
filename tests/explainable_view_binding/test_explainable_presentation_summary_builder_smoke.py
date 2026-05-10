from __future__ import annotations

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_presentation_summary,
)


def test_explainable_presentation_summary_builder_smoke() -> None:
    summary = build_explainable_presentation_summary()

    assert summary["summary_ready"] is True
    assert summary["explainable_presentation_bindings"] == 3
    assert summary["explainable_presentation_ready_bindings"] == 3
    assert summary["presentation_route_bound_bindings"] == 3
    assert summary["explainable_source_bound_bindings"] == 3
    assert summary["dashboard_bound_bindings"] == 2
    assert summary["route_bound_bindings"] == 1
    assert summary["action_execution_allowed_bindings"] == 0
    assert summary["direct_display_switching_allowed_bindings"] == 0
