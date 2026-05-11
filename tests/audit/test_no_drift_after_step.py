from __future__ import annotations

from tools.roadmap_post_step_drift_check import build_roadmap_post_step_drift_report


def test_no_drift_after_step_full_drift_report_smoke() -> None:
    report = build_roadmap_post_step_drift_report()

    assert report.structural_drift_check_ready is True
    assert report.roadmap_semantic_drift_check_ready is True
    assert report.critical_surfaces_present is True
    assert report.forbidden_staged_paths == ()
    assert report.missing_required_docs == ()
    assert report.missing_required_tests == ()
    assert report.original_phase_4_closed is True
    assert report.original_phase_5_closed is True
    assert report.phase_5_1_closed is True
    assert report.mempalace_is_extension_not_replacement is True
    assert report.drift_check_passed is True
