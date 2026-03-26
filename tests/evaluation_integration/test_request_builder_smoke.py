from __future__ import annotations

from MAKSIMAR_CORE_LIB.evaluation_integration import (
    EvaluationIntent,
    build_evaluation_request,
)


def test_build_evaluation_request_uses_default_definition() -> None:
    """Evaluation request builder should use first available definition by default."""
    request = build_evaluation_request(
        EvaluationIntent(query_text="evaluate simulation result")
    )

    assert request.evaluation_id
    assert request.version.endswith(".v1")
    assert request.source_definition_id


def test_build_evaluation_request_respects_preferred_definition() -> None:
    """Evaluation request builder should respect explicit preferred evaluation."""
    request = build_evaluation_request(
        EvaluationIntent(
            query_text="evaluate code generation",
            preferred_evaluation="codegen_eval",
        )
    )

    assert request.evaluation_id == "codegen_eval"
