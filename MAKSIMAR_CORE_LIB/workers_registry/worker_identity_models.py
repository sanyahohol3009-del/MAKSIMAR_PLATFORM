from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


CanonicalWorkerId = Literal[
    "worker_ai_001",
    "worker_sim_001",
    "worker_voice_001",
]

CanonicalWorkerType = Literal[
    "ai_worker",
    "simulation_worker",
    "media_worker",
    "automation_worker",
    "evaluation_worker",
    "voice_worker",
]


@dataclass(frozen=True, slots=True)
class CanonicalWorkerIdentity:
    """Canonical worker identity entry."""

    worker_id: CanonicalWorkerId
    worker_type: CanonicalWorkerType


@dataclass(frozen=True, slots=True)
class CanonicalWorkerIdentityContract:
    """Unified canonical worker identity contract."""

    total_workers: int
    workers: tuple[CanonicalWorkerIdentity, ...]
