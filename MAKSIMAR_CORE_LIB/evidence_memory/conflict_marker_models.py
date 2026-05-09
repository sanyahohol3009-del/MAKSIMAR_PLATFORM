from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


ConflictState = Literal["none", "detected", "resolved"]

_CONFLICT_MARKER_ID_PATTERN = re.compile(r"^conflict_marker_[a-z][a-z0-9_]*$")
_EVIDENCE_ID_PATTERN = re.compile(r"^evidence_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class ConflictMarkerRecord:
    conflict_marker_id: str
    evidence_id: str
    conflict_state: ConflictState
    conflict_marker: str
    conflict_detected: bool
    resolution_required: bool
    conflict_ready: bool

    def __post_init__(self) -> None:
        conflict_marker_id = _ensure_non_empty_str(
            self.conflict_marker_id,
            "conflict_marker_id",
        )
        evidence_id = _ensure_non_empty_str(self.evidence_id, "evidence_id")

        if not _CONFLICT_MARKER_ID_PATTERN.fullmatch(conflict_marker_id):
            raise ValueError(f"Invalid conflict_marker_id: {conflict_marker_id}")
        if not _EVIDENCE_ID_PATTERN.fullmatch(evidence_id):
            raise ValueError(f"Invalid evidence_id: {evidence_id}")

        conflict_detected = _ensure_bool(
            self.conflict_detected,
            "conflict_detected",
        )
        resolution_required = _ensure_bool(
            self.resolution_required,
            "resolution_required",
        )
        conflict_ready = _ensure_bool(self.conflict_ready, "conflict_ready")

        if self.conflict_state == "none":
            if self.conflict_marker:
                raise ValueError("conflict_marker must be empty for none state")
            if conflict_detected:
                raise ValueError("conflict_detected must be False for none state")
            if resolution_required:
                raise ValueError("resolution_required must be False for none state")

        if not conflict_ready:
            raise ValueError("conflict_ready must be True")

        object.__setattr__(self, "conflict_marker_id", conflict_marker_id)
        object.__setattr__(self, "evidence_id", evidence_id)


@dataclass(frozen=True, slots=True)
class ConflictMarkerContract:
    total_markers: int
    conflict_detected_markers: int
    ready_markers: int
    markers: tuple[ConflictMarkerRecord, ...]

    def __post_init__(self) -> None:
        if self.total_markers != len(self.markers):
            raise ValueError("total_markers must match markers length")
        if self.total_markers <= 0:
            raise ValueError("total_markers must be >= 1")
        if self.conflict_detected_markers != sum(
            1 for marker in self.markers if marker.conflict_detected
        ):
            raise ValueError("conflict_detected_markers must match computed count")
        if self.ready_markers != sum(
            1 for marker in self.markers if marker.conflict_ready
        ):
            raise ValueError("ready_markers must match computed count")
        if self.conflict_detected_markers != 0:
            raise ValueError("Batch 3 canonical layer must start conflict-clear")
        if self.ready_markers != self.total_markers:
            raise ValueError("all conflict markers must be ready")
