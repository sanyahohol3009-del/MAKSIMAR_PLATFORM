from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


CanonicalQueueName = Literal[
    "critical_queue",
    "high_queue",
    "normal_queue",
    "background_queue",
    "deferred_queue",
]


@dataclass(frozen=True, slots=True)
class CanonicalQueueIdentity:
    """Canonical queue identity entry."""

    queue_name: CanonicalQueueName
    priority_class: str


@dataclass(frozen=True, slots=True)
class CanonicalQueueIdentityContract:
    """Unified canonical queue identity contract."""

    total_queues: int
    queues: tuple[CanonicalQueueIdentity, ...]
