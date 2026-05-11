from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.drift_detection.memory_drift_signal_models import (
    MemoryDriftSignal,
    build_memory_drift_signal_sample,
)


ContradictionCandidateStatus = Literal["candidate_only", "rejected", "approved_for_review"]


@dataclass(frozen=True, slots=True)
class MemoryContradictionCandidate:
    candidate_id: str
    signal: MemoryDriftSignal
    category_id: str
    status: ContradictionCandidateStatus
    evidence_refs: Tuple[str, ...]
    human_review_required: bool
    canonical_truth_change_allowed: bool
    auto_resolution_allowed: bool
    candidate_ready: bool

    def __post_init__(self) -> None:
        if not self.candidate_id:
            raise ValueError("candidate_id must be non-empty")
        if not self.category_id:
            raise ValueError("category_id must be non-empty")
        if not self.evidence_refs:
            raise ValueError("evidence_refs must be non-empty")
        if not self.human_review_required:
            raise ValueError("human_review_required must be True")
        if self.canonical_truth_change_allowed:
            raise ValueError("canonical_truth_change_allowed must be False")
        if self.auto_resolution_allowed:
            raise ValueError("auto_resolution_allowed must be False")
        if not self.candidate_ready:
            raise ValueError("candidate_ready must be True")


def build_memory_contradiction_candidate_sample() -> MemoryContradictionCandidate:
    signal = build_memory_drift_signal_sample()

    return MemoryContradictionCandidate(
        candidate_id="memory_contradiction_candidate_001",
        signal=signal,
        category_id="scope_conflict",
        status="candidate_only",
        evidence_refs=signal.evidence_refs,
        human_review_required=True,
        canonical_truth_change_allowed=False,
        auto_resolution_allowed=False,
        candidate_ready=True,
    )
