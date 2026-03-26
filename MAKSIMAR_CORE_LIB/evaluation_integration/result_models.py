from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvaluationRawResult:
    """Raw evaluation outcome before integration-level adaptation."""

    execution_id: str
    evaluation_id: str
    score: float
    status: str


@dataclass(frozen=True, slots=True)
class EvaluationIntegrationResult:
    """Canonical evaluation result adapted by integration layer."""

    execution_id: str
    evaluation_id: str
    score: float
    status: str
    passed: bool
