from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ArtifactStoragePolicy = Literal[
    "ephemeral",
    "retained",
    "archival",
]

ArtifactIntegrityPolicy = Literal[
    "checksum_required",
    "signature_required",
]


@dataclass(frozen=True, slots=True)
class ArtifactReferenceEntry:
    """Canonical artifact reference entry for heavy payload routing."""

    artifact_ref: str
    artifact_type: str
    artifact_size_kb: int
    owner_task_id: str
    storage_policy: ArtifactStoragePolicy
    integrity_policy: ArtifactIntegrityPolicy


@dataclass(frozen=True, slots=True)
class ArtifactReferenceContract:
    """Unified canonical artifact reference contract."""

    total_references: int
    references: tuple[ArtifactReferenceEntry, ...]
