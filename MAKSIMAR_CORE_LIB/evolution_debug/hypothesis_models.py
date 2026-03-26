from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DebugHypothesis:
    """One structured debug hypothesis."""

    hypothesis_id: str
    error_code: str
    reasoning_summary: str
    proposed_patch_scope: str


@dataclass(frozen=True, slots=True)
class DebugHypothesisContract:
    """Unified hypothesis contract for evolution debug layer."""

    total_hypotheses: int
    hypotheses: tuple[DebugHypothesis, ...]
    sandbox_required: bool
