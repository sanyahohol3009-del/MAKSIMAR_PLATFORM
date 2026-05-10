from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_summary,
)


def test_presentation_summary_builder_smoke() -> None:
    summary = build_presentation_summary()

    assert summary["summary_ready"] is True
    assert summary["presentation_requests"] == 3
    assert summary["view_resolutions"] == 3
    assert summary["panel_resolutions"] == 3
    assert summary["display_target_selections"] == 3
    assert summary["presentation_action_execution_allowed_requests"] == 0
    assert summary["display_target_direct_switching_allowed"] == 0
