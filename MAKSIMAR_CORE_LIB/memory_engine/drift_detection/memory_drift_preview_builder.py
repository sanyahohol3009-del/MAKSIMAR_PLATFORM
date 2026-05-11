from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.drift_detection.memory_drift_report_models import (
    build_memory_drift_report,
)
from MAKSIMAR_CORE_LIB.memory_engine.drift_detection.memory_drift_validators import (
    validate_memory_drift_report,
)


def build_memory_drift_preview() -> Dict[str, object]:
    report = build_memory_drift_report()
    validation_ready = validate_memory_drift_report(report)

    return {
        "report_id": report.report_id,
        "preview_ready": validation_ready,
        "total_signals": report.total_signals,
        "total_categories": report.total_categories,
        "total_candidates": report.total_candidates,
        "human_review_required": report.human_review_required,
        "canonical_truth_change_allowed": report.canonical_truth_change_allowed,
        "auto_resolution_allowed": report.auto_resolution_allowed,
        "candidate_ids": tuple(candidate.candidate_id for candidate in report.candidates),
        "signal_kinds": tuple(signal.signal_kind for signal in report.signals),
        "category_ids": tuple(category.category_id for category in report.categories),
        "flow": (
            "memory_drift_signal",
            "memory_drift_category",
            "memory_contradiction_candidate",
            "memory_drift_report",
            "memory_drift_validation",
            "memory_drift_preview",
        ),
    }
