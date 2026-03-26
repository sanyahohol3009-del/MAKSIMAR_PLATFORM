from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_loop import (
    RankedEvaluationResult,
    select_best_evaluation_result,
)


def test_select_best_evaluation_result_by_score() -> None:
    """Ranking selector should choose highest-score result."""
    result = select_best_evaluation_result(
        [
            RankedEvaluationResult(
                execution_id="eval_exec_001",
                evaluation_id="benchmark_case",
                score=0.4,
                passed=False,
            ),
            RankedEvaluationResult(
                execution_id="eval_exec_002",
                evaluation_id="codegen_eval",
                score=0.9,
                passed=True,
            ),
        ]
    )

    assert result.total_candidates == 2
    assert result.selected_execution_id == "eval_exec_002"
    assert result.selected_evaluation_id == "codegen_eval"
    assert result.selected_score == 0.9
    assert result.selected_passed is True


def test_select_best_evaluation_result_prefers_passed_when_score_matches() -> None:
    """Ranking selector should prefer passed result when score is equal."""
    result = select_best_evaluation_result(
        [
            RankedEvaluationResult(
                execution_id="eval_exec_003",
                evaluation_id="benchmark_case",
                score=0.8,
                passed=False,
            ),
            RankedEvaluationResult(
                execution_id="eval_exec_004",
                evaluation_id="workflow_eval",
                score=0.8,
                passed=True,
            ),
        ]
    )

    assert result.selected_execution_id == "eval_exec_004"
    assert result.selected_passed is True
