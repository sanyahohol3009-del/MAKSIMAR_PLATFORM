from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


TaskResultStatus = Literal[
    "completed",
    "failed",
    "blocked",
]


@dataclass(frozen=True, slots=True)
class TaskResult:
    """Canonical platform-to-mobile task result."""

    result_id: str
    envelope_id: str
    status: TaskResultStatus
    payload_ref: str
    core_write_performed: bool


@dataclass(frozen=True, slots=True)
class TaskResultContract:
    """Unified task result contract."""

    total_results: int
    results: tuple[TaskResult, ...]
