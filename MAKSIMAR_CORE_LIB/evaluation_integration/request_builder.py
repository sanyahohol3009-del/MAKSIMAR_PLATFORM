from __future__ import annotations

from MAKSIMAR_CORE_LIB.evaluation_integration.evaluation_registry_summary import (
    build_evaluation_registry_summary,
)
from MAKSIMAR_CORE_LIB.evaluation_integration.request_models import (
    EvaluationIntent,
    EvaluationIntegrationRequest,
)


def _resolve_evaluation(
    intent: EvaluationIntent,
) -> tuple[str, str, str]:
    """Resolve evaluation definition from intent and evaluation registry."""
    summary = build_evaluation_registry_summary()
    if not summary.records:
        raise RuntimeError("No evaluation definitions available.")

    if intent.preferred_evaluation is not None:
        for record in summary.records:
            if record.evaluation_id == intent.preferred_evaluation:
                return (
                    record.evaluation_id,
                    record.version,
                    record.source_definition_id,
                )

    record = summary.records[0]
    return record.evaluation_id, record.version, record.source_definition_id


def build_evaluation_request(
    intent: EvaluationIntent,
) -> EvaluationIntegrationRequest:
    """Build canonical evaluation integration request."""
    evaluation_id, version, source_definition_id = _resolve_evaluation(intent)

    return EvaluationIntegrationRequest(
        request_text=intent.query_text,
        evaluation_id=evaluation_id,
        version=version,
        source_definition_id=source_definition_id,
    )
