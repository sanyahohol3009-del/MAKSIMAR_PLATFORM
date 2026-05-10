from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_display_target_selection_contract,
    build_panel_resolution_contract,
    build_presentation_preview,
    build_presentation_request_contract,
    build_presentation_summary,
    build_view_resolution_contract,
)


def test_phase_3_2_batch1_ready_smoke() -> None:
    requests = build_presentation_request_contract()
    views = build_view_resolution_contract()
    panels = build_panel_resolution_contract()
    targets = build_display_target_selection_contract()
    summary = build_presentation_summary()
    preview = build_presentation_preview()

    assert requests.ready_requests == requests.total_requests
    assert views.ready_resolutions == views.total_resolutions
    assert panels.ready_panels == panels.total_panels
    assert targets.ready_selections == targets.total_selections
    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert preview["action_execution_allowed"] == 0
    assert preview["direct_display_switching_allowed"] == 0
