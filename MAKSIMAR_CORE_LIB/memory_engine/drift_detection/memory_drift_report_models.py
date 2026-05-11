from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.memory_engine.drift_detection.memory_contradiction_candidate_models import (
    MemoryContradictionCandidate,
    build_memory_contradiction_candidate_sample,
)
from MAKSIMAR_CORE_LIB.memory_engine.drift_detection.memory_drift_category_models import (
    MemoryDriftCategory,
    build_memory_drift_categories,
)
from MAKSIMAR_CORE_LIB.memory_engine.drift_detection.memory_drift_signal_models import (
    MemoryDriftSignal,
    build_memory_drift_signal_sample,
)


@dataclass(frozen=True, slots=True)
class MemoryDriftReport:
    report_id: str
    signals: Tuple[MemoryDriftSignal, ...]
    categories: Tuple[MemoryDriftCategory, ...]
    candidates: Tuple[MemoryContradictionCandidate, ...]
    total_signals: int
    total_categories: int
    total_candidates: int
    human_review_required: bool
    canonical_truth_change_allowed: bool
    auto_resolution_allowed: bool
    report_ready: bool

    def __post_init__(self) -> None:
        if not self.report_id:
            raise ValueError("report_id must be non-empty")
        if self.total_signals != len(self.signals):
            raise ValueError("total_signals mismatch")
        if self.total_categories != len(self.categories):
            raise ValueError("total_categories mismatch")
        if self.total_candidates != len(self.candidates):
            raise ValueError("total_candidates mismatch")
        if not self.human_review_required:
            raise ValueError("human_review_required must be True")
        if self.canonical_truth_change_allowed:
            raise ValueError("canonical_truth_change_allowed must be False")
        if self.auto_resolution_allowed:
            raise ValueError("auto_resolution_allowed must be False")
        if not self.report_ready:
            raise ValueError("report_ready must be True")


def build_memory_drift_report() -> MemoryDriftReport:
    signals = (build_memory_drift_signal_sample(),)
    categories = build_memory_drift_categories()
    candidates = (build_memory_contradiction_candidate_sample(),)

    return MemoryDriftReport(
        report_id="memory_drift_report_001",
        signals=signals,
        categories=categories,
        candidates=candidates,
        total_signals=len(signals),
        total_categories=len(categories),
        total_candidates=len(candidates),
        human_review_required=True,
        canonical_truth_change_allowed=False,
        auto_resolution_allowed=False,
        report_ready=True,
    )
