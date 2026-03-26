from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvaluationExecutionEnvelope:
    """Execution-level container for evaluation request."""

    request_text: str
    evaluation_id: str
    version: str
    source_definition_id: str

    execution_id: str
    status: str
