from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


QueueType = Literal[
    "critical_queue",
    "high_queue",
    "normal_queue",
    "background_queue",
    "deferred_queue",
]


@dataclass(frozen=True, slots=True)
class QueuePolicyRule:
    """Canonical queue policy rule."""

    queue_type: QueueType
    max_items: int
    overflow_action: str


@dataclass(frozen=True, slots=True)
class QueuePolicyContract:
    """Unified queue policy contract."""

    total_rules: int
    rules: tuple[QueuePolicyRule, ...]
