from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.drift_detection import build_memory_drift_report


def test_history_source_not_canonical_truth_smoke() -> None:
    report = build_memory_drift_report()

    assert report.report_ready is True
    assert report.human_review_required is True
    assert report.canonical_truth_change_allowed is False
    assert report.auto_resolution_allowed is False

    for candidate in report.candidates:
        assert candidate.canonical_truth_change_allowed is False
        assert candidate.auto_resolution_allowed is False
