from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ArtifactOwnership:
    """Canonical artifact ownership entry."""

    artifact_ref: str
    owner_task_id: str
    owner_worker_id: str
    retained: bool


@dataclass(frozen=True, slots=True)
class ArtifactOwnershipContract:
    """Unified artifact ownership contract."""

    total_artifacts: int
    artifacts: tuple[ArtifactOwnership, ...]
