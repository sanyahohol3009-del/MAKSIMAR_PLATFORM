from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvaluationIntent:
    """Raw evaluation intent before integration-level normalization."""

    query_text: str
    preferred_evaluation: str | None = None


@dataclass(frozen=True, slots=True)
class EvaluationIntegrationRequest:
    """Canonical evaluation request built by integration layer."""

    request_text: str
    evaluation_id: str
    version: str
    source_definition_id: str
