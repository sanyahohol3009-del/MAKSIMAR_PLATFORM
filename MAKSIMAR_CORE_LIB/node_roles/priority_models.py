from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


TaskPriority = Literal[
    "critical",
    "high",
    "normal",
    "background",
    "deferred",
]


@dataclass(frozen=True, slots=True)
class TaskPriorityRule:
    """Canonical task priority rule."""

    task_type: str
    priority: TaskPriority


@dataclass(frozen=True, slots=True)
class TaskPriorityContract:
    """Unified task priority contract."""

    total_rules: int
    rules: tuple[TaskPriorityRule, ...]
