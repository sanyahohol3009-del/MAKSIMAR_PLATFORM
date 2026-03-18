from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


ExecutionStatus = Literal["planned", "blocked"]


@dataclass(frozen=True, slots=True)
class ActionExecutionRequest:
    """Canonical action execution request."""

    action_id: str
    parameters: dict[str, Any]
    context: dict[str, Any]


@dataclass(frozen=True, slots=True)
class DryRunExecutionResult:
    """Canonical dry-run execution result."""

    action_id: str
    status: ExecutionStatus
    resolved: bool
    message: str
