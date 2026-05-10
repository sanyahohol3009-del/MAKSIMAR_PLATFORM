from __future__ import annotations

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_presentation_preview,
)


def test_explainable_presentation_preview_builder_smoke() -> None:
    preview = build_explainable_presentation_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["explainable_presentation_bindings"] == 3
    assert preview["dashboard_bound_bindings"] == 2
    assert preview["route_bound_bindings"] == 1
    assert preview["action_execution_allowed_bindings"] == 0
    assert preview["direct_display_switching_allowed_bindings"] == 0

    assert preview["command_intents"] == (
        "show_memory",
        "show_simulation",
        "show_monitoring",
    )
    assert preview["resolution_sources"] == (
        "dashboard_read_only_view",
        "dashboard_read_only_view",
        "display_orchestration_route",
    )
