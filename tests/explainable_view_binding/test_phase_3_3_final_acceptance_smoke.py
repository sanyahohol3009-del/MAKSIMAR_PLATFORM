from __future__ import annotations

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_phase_preview,
    build_explainable_phase_readiness,
    build_explainable_presentation_preview,
    build_explainable_presentation_summary,
)


def test_phase_3_3_final_acceptance_smoke() -> None:
    summary = build_explainable_presentation_summary()
    preview = build_explainable_presentation_preview()
    readiness = build_explainable_phase_readiness()
    phase_preview = build_explainable_phase_preview()

    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert readiness.phase_ready is True
    assert phase_preview["phase_ready"] is True
    assert phase_preview["preview_ready"] is True
