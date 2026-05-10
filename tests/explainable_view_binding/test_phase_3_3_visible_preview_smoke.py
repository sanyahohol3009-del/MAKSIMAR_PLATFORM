from __future__ import annotations

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_phase_preview,
    build_explainable_presentation_preview,
)


def test_phase_3_3_visible_preview_smoke() -> None:
    preview = build_explainable_presentation_preview()
    phase_preview = build_explainable_phase_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["explainable_presentation_bindings"] == 3
    assert preview["dashboard_bound_bindings"] == 2
    assert preview["route_bound_bindings"] == 1

    assert phase_preview["preview_ready"] is True
    assert phase_preview["phase_ready"] is True
    assert phase_preview["route_bound_monitoring_ready"] is True
    assert phase_preview["no_new_explainability_roots"] is True
