from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MediaQuarantineStatus(str, Enum):
    CLEAN = "clean"
    QUARANTINED = "quarantined"


@dataclass(frozen=True, slots=True)
class MediaArtifactScan:
    artifact_id: str
    content_hash: str
    media_type: str
    scanner_ids: tuple[str, ...]
    threat_labels: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name, value in (
            ("artifact_id", self.artifact_id),
            ("content_hash", self.content_hash),
            ("media_type", self.media_type),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not isinstance(self.scanner_ids, tuple):
            raise TypeError("scanner_ids must be a tuple")
        if not isinstance(self.threat_labels, tuple):
            raise TypeError("threat_labels must be a tuple")


@dataclass(frozen=True, slots=True)
class MediaQuarantineDecision:
    artifact_id: str
    status: MediaQuarantineStatus
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.artifact_id:
            raise ValueError("artifact_id must not be empty")
        if not isinstance(self.status, MediaQuarantineStatus):
            raise TypeError("status must be MediaQuarantineStatus")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")


def evaluate_media_quarantine(scan: MediaArtifactScan) -> MediaQuarantineDecision:
    if scan.threat_labels:
        return MediaQuarantineDecision(
            artifact_id=scan.artifact_id,
            status=MediaQuarantineStatus.QUARANTINED,
            reason_codes=("media_threat_detected",),
        )

    return MediaQuarantineDecision(
        artifact_id=scan.artifact_id,
        status=MediaQuarantineStatus.CLEAN,
        reason_codes=("media_clean",),
    )
