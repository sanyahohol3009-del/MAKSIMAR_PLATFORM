from __future__ import annotations

from MAKSIMAR_CORE_LIB.evaluation_integration.result_models import (
    EvaluationIntegrationResult,
    EvaluationRawResult,
)


def adapt_evaluation_result(
    raw_result: EvaluationRawResult,
) -> EvaluationIntegrationResult:
    """Adapt raw evaluation result into canonical integration result."""
    passed = raw_result.status == "completed" and raw_result.score >= 0.5

    return EvaluationIntegrationResult(
        execution_id=raw_result.execution_id,
        evaluation_id=raw_result.evaluation_id,
        score=raw_result.score,
        status=raw_result.status,
        passed=passed,
    )
