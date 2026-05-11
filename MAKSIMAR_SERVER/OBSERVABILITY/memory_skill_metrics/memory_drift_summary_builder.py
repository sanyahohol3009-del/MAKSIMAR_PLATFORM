from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.drift_detection import (
    build_memory_drift_preview,
    build_memory_drift_report,
    validate_memory_drift_report,
)


def build_memory_drift_summary() -> Dict[str, object]:
    report = build_memory_drift_report()
    preview = build_memory_drift_preview()

    summary_ready = (
        validate_memory_drift_report(report)
        and preview["preview_ready"] is True
        and preview["canonical_truth_change_allowed"] is False
        and preview["auto_resolution_allowed"] is False
    )

    return {
        "summary_id": "memory_drift_summary_001",
        "summary_ready": summary_ready,
        "preview_ready": preview["preview_ready"],
        "total_signals": report.total_signals,
        "total_candidates": report.total_candidates,
        "human_review_required": report.human_review_required,
        "canonical_truth_change_allowed": report.canonical_truth_change_allowed,
        "auto_resolution_allowed": report.auto_resolution_allowed,
        "candidate_ids": preview["candidate_ids"],
        "signal_kinds": preview["signal_kinds"],
    }
