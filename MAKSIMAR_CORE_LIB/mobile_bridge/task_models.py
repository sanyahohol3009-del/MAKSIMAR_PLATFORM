from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


TaskEnvelopeType = Literal[
    "query_task",
    "automation_task",
    "status_task",
]

TaskExecutionTarget = Literal[
    "home_node",
    "dev_node",
]


@dataclass(frozen=True, slots=True)
class TaskEnvelope:
    """Canonical mobile-to-platform task envelope."""

    envelope_id: str
    request_id: str
    envelope_type: TaskEnvelopeType
    execution_target: TaskExecutionTarget
    core_write_allowed: bool
    mobile_executes_task: bool


@dataclass(frozen=True, slots=True)
class TaskEnvelopeContract:
    """Unified task envelope contract."""

    total_envelopes: int
    envelopes: tuple[TaskEnvelope, ...]
