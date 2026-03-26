from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProposalPackage:
    """Canonical proposal package produced by evolution loop."""

    package_id: str
    selected_execution_id: str
    selected_evaluation_id: str
    selected_score: float
    selected_passed: bool
    status: str
