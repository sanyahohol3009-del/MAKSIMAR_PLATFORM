from __future__ import annotations

import uuid

from MAKSIMAR_CORE_LIB.evaluation_integration.execution_models import (
    EvaluationExecutionEnvelope,
)
from MAKSIMAR_CORE_LIB.evaluation_integration.request_builder import (
    build_evaluation_request,
)
from MAKSIMAR_CORE_LIB.evaluation_integration.request_models import (
    EvaluationIntent,
)


def _generate_execution_id() -> str:
    """Generate unique execution id."""
    return f"eval_exec_{uuid.uuid4().hex}"


def build_evaluation_execution_envelope(
    intent: EvaluationIntent,
) -> EvaluationExecutionEnvelope:
    """Build execution envelope from evaluation intent."""
    request = build_evaluation_request(intent)

    return EvaluationExecutionEnvelope(
        request_text=request.request_text,
        evaluation_id=request.evaluation_id,
        version=request.version,
        source_definition_id=request.source_definition_id,
        execution_id=_generate_execution_id(),
        status="created",
    )
