from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RankedEvaluationResult:
    """Evaluation result prepared for ranking and selection."""

    execution_id: str
    evaluation_id: str
    score: float
    passed: bool


@dataclass(frozen=True, slots=True)
class RankingSelectionResult:
    """Final selection result from ranked evaluation results."""

    total_candidates: int
    selected_execution_id: str
    selected_evaluation_id: str
    selected_score: float
    selected_passed: bool
