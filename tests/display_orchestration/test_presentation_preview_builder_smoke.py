from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_preview,
)


def test_presentation_preview_builder_smoke() -> None:
    preview = build_presentation_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["presentation_requests"] == 3
    assert preview["view_resolutions"] == 3
    assert preview["panel_resolutions"] == 3
    assert preview["display_target_selections"] == 3
    assert preview["action_execution_allowed"] == 0
    assert preview["direct_display_switching_allowed"] == 0
    assert "view_memory_project_architecture" in preview["resolved_view_ids"]
