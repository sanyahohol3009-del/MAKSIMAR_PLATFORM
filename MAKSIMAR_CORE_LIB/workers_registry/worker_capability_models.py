from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


WorkerCapabilityType = Literal[
    "inference",
    "simulation",
    "media_processing",
    "automation",
    "evaluation",
    "voice_io",
]


@dataclass(frozen=True, slots=True)
class WorkerCapability:
    """Canonical worker capability entry."""

    worker_id: str
    capability_type: WorkerCapabilityType
    max_concurrency: int
    requires_gpu: bool


@dataclass(frozen=True, slots=True)
class WorkerCapabilityContract:
    """Unified worker capability contract."""

    total_capabilities: int
    capabilities: tuple[WorkerCapability, ...]
