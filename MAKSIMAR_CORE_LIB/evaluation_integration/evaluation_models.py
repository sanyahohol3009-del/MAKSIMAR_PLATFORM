from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvaluationDefinitionRecord:
    """One evaluation-oriented registry record."""

    evaluation_id: str
    version: str
    source_definition_id: str


@dataclass(frozen=True, slots=True)
class EvaluationRegistrySummary:
    """Unified summary of evaluation definitions."""

    total_evaluations: int
    records: list[EvaluationDefinitionRecord]
