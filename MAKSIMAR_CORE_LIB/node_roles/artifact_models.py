from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ArtifactReference:
    """Canonical reference to artifact data stored in data plane."""

    artifact_ref: str
    artifact_type: str
    artifact_size: int
    owner_task_id: str


@dataclass(frozen=True, slots=True)
class ArtifactReferenceContract:
    """Unified artifact / data plane separation contract."""

    total_artifacts: int
    artifacts: tuple[ArtifactReference, ...]
