from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class WorkflowStep:
    """Canonical workflow step."""

    step_id: str
    action_ref: str
    payload: dict[str, Any]


@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    """Canonical workflow definition."""

    workflow_id: str
    version: str
    file_path: Path
    trigger_phrases: list[str]
    steps: list[WorkflowStep]
    payload: dict[str, Any]


@dataclass(slots=True)
class WorkflowLoadResult:
    """Result of loading one workflow definition."""

    definition: WorkflowDefinition | None
    is_valid: bool
    error: str | None = None
