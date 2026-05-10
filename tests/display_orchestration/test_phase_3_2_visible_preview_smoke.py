from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_phase_preview,
    build_presentation_preview,
)


def test_phase_3_2_visible_preview_smoke() -> None:
    preview = build_presentation_preview()
    phase_preview = build_presentation_phase_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["presentation_routes"] == 3
    assert preview["presentation_ready_routes"] == 3
    assert preview["presentation_dashboard_bound_routes"] == 2
    assert preview["presentation_route_bound_routes"] == 1
    assert preview["action_execution_allowed"] == 0
    assert preview["direct_display_switching_allowed"] == 0

    assert phase_preview["preview_ready"] is True
    assert phase_preview["phase_ready"] is True
    assert phase_preview["multi_display_selection_ready"] is True
    assert phase_preview["no_new_presentation_roots"] is True
