from __future__ import annotations

from MAKSIMAR_CORE_LIB.evaluation_integration import (
    EvaluationIntent,
    build_evaluation_execution_envelope,
)


def test_execution_envelope_builds() -> None:
    """Evaluation execution envelope should be created correctly."""
    envelope = build_evaluation_execution_envelope(
        EvaluationIntent(query_text="evaluate simulation result")
    )

    assert envelope.execution_id.startswith("eval_exec_")
    assert envelope.status == "created"
    assert envelope.evaluation_id


def test_execution_envelope_respects_preferred_definition() -> None:
    """Evaluation execution envelope should respect preferred evaluation."""
    envelope = build_evaluation_execution_envelope(
        EvaluationIntent(
            query_text="evaluate code generation",
            preferred_evaluation="codegen_eval",
        )
    )

    assert envelope.evaluation_id == "codegen_eval"
