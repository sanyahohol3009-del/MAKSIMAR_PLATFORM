from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_loop.ranking_models import (
    RankedEvaluationResult,
    RankingSelectionResult,
)


def select_best_evaluation_result(
    results: list[RankedEvaluationResult],
) -> RankingSelectionResult:
    """Select best evaluation result by score, then by pass status."""
    if not results:
        raise ValueError("No evaluation results provided for ranking.")

    sorted_results = sorted(
        results,
        key=lambda item: (item.score, item.passed),
        reverse=True,
    )
    best = sorted_results[0]

    return RankingSelectionResult(
        total_candidates=len(results),
        selected_execution_id=best.execution_id,
        selected_evaluation_id=best.evaluation_id,
        selected_score=best.score,
        selected_passed=best.passed,
    )
