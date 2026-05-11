from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.drift_detection.memory_drift_report_models import (
    MemoryDriftReport,
)


def validate_memory_drift_report(report: MemoryDriftReport) -> bool:
    if not report.report_ready:
        return False
    if not report.human_review_required:
        return False
    if report.canonical_truth_change_allowed:
        return False
    if report.auto_resolution_allowed:
        return False
    if report.total_signals < 1:
        return False
    if report.total_candidates < 1:
        return False

    return all(
        candidate.human_review_required
        and candidate.canonical_truth_change_allowed is False
        and candidate.auto_resolution_allowed is False
        for candidate in report.candidates
    )
