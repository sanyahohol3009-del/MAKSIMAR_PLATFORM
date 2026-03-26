from __future__ import annotations

from MAKSIMAR_CORE_LIB.evaluation_integration import (
    EvaluationRawResult,
    adapt_evaluation_result,
)


def test_result_adapter_marks_passed() -> None:
    """Result adapter should mark completed high-score result as passed."""
    result = adapt_evaluation_result(
        EvaluationRawResult(
            execution_id="eval_exec_001",
            evaluation_id="codegen_eval",
            score=0.9,
            status="completed",
        )
    )

    assert result.passed is True
    assert result.evaluation_id == "codegen_eval"


def test_result_adapter_marks_not_passed() -> None:
    """Result adapter should mark low-score or incomplete result as not passed."""
    result = adapt_evaluation_result(
        EvaluationRawResult(
            execution_id="eval_exec_002",
            evaluation_id="benchmark_case",
            score=0.2,
            status="completed",
        )
    )

    assert result.passed is False
    assert result.evaluation_id == "benchmark_case"
