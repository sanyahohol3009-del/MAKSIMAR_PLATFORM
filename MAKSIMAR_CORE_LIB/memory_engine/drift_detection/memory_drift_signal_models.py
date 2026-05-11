from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


MemoryDriftSignalKind = Literal[
    "semantic_conflict",
    "source_date_conflict",
    "jurisdiction_conflict",
    "scope_conflict",
    "artifact_version_conflict",
]


@dataclass(frozen=True, slots=True)
class MemoryDriftSignal:
    signal_id: str
    source_memory_ref: str
    candidate_memory_ref: str
    signal_kind: MemoryDriftSignalKind
    confidence: float
    evidence_refs: Tuple[str, ...]
    human_review_required: bool
    auto_resolution_allowed: bool
    canonical_truth_change_allowed: bool
    signal_ready: bool

    def __post_init__(self) -> None:
        if not self.signal_id:
            raise ValueError("signal_id must be non-empty")
        if not self.source_memory_ref:
            raise ValueError("source_memory_ref must be non-empty")
        if not self.candidate_memory_ref:
            raise ValueError("candidate_memory_ref must be non-empty")
        if self.source_memory_ref == self.candidate_memory_ref:
            raise ValueError("source_memory_ref and candidate_memory_ref must differ")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if not self.evidence_refs:
            raise ValueError("evidence_refs must be non-empty")
        if not self.human_review_required:
            raise ValueError("human_review_required must be True")
        if self.auto_resolution_allowed:
            raise ValueError("auto_resolution_allowed must be False")
        if self.canonical_truth_change_allowed:
            raise ValueError("canonical_truth_change_allowed must be False")
        if not self.signal_ready:
            raise ValueError("signal_ready must be True")


def build_memory_drift_signal_sample() -> MemoryDriftSignal:
    return MemoryDriftSignal(
        signal_id="memory_drift_signal_001",
        source_memory_ref="memory::project_notes::roadmap_v5_phase_4",
        candidate_memory_ref="memory::implementation::phase_4_3_memory_sync",
        signal_kind="scope_conflict",
        confidence=0.82,
        evidence_refs=(
            "roadmap_v5::phase_4_memory_drift_contradiction_candidate_readiness",
            "implementation::phase_4_3_memory_sync_final_acceptance",
        ),
        human_review_required=True,
        auto_resolution_allowed=False,
        canonical_truth_change_allowed=False,
        signal_ready=True,
    )
