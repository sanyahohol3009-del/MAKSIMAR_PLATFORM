from __future__ import annotations

import re
from dataclasses import dataclass


_SOURCE_EVENT_ID_PATTERN = re.compile(r"^source_event_[a-z][a-z0-9_]*$")
_SOURCE_ID_PATTERN = re.compile(r"^retrieval_source_[a-z][a-z0-9_]*$")


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
class SourceEventRecord:
    source_event_id: str
    source_id: str
    source_layer: str
    source_event_ref: str
    artifact_ref: str
    event_summary: str
    event_ready: bool

    def __post_init__(self) -> None:
        source_event_id = _ensure_non_empty_str(
            self.source_event_id,
            "source_event_id",
        )
        source_id = _ensure_non_empty_str(self.source_id, "source_id")
        source_layer = _ensure_non_empty_str(self.source_layer, "source_layer")
        source_event_ref = _ensure_non_empty_str(
            self.source_event_ref,
            "source_event_ref",
        )
        artifact_ref = _ensure_non_empty_str(self.artifact_ref, "artifact_ref")
        event_summary = _ensure_non_empty_str(self.event_summary, "event_summary")

        if not _SOURCE_EVENT_ID_PATTERN.fullmatch(source_event_id):
            raise ValueError(f"Invalid source_event_id: {source_event_id}")
        if not _SOURCE_ID_PATTERN.fullmatch(source_id):
            raise ValueError(f"Invalid source_id: {source_id}")
        if not source_event_ref.startswith("source_event://"):
            raise ValueError("source_event_ref must start with source_event://")
        if not artifact_ref.startswith("artifact://"):
            raise ValueError("artifact_ref must start with artifact://")

        event_ready = _ensure_bool(self.event_ready, "event_ready")
        if not event_ready:
            raise ValueError("event_ready must be True")

        object.__setattr__(self, "source_event_id", source_event_id)
        object.__setattr__(self, "source_id", source_id)
        object.__setattr__(self, "source_layer", source_layer)
        object.__setattr__(self, "source_event_ref", source_event_ref)
        object.__setattr__(self, "artifact_ref", artifact_ref)
        object.__setattr__(self, "event_summary", event_summary)


@dataclass(frozen=True, slots=True)
class SourceEventContract:
    total_events: int
    ready_events: int
    events: tuple[SourceEventRecord, ...]

    def __post_init__(self) -> None:
        if self.total_events != len(self.events):
            raise ValueError("total_events must match events length")
        if self.total_events <= 0:
            raise ValueError("total_events must be >= 1")
        if self.ready_events != sum(1 for event in self.events if event.event_ready):
            raise ValueError("ready_events must match computed count")
        if self.ready_events != self.total_events:
            raise ValueError("all source events must be ready")

        event_ids = tuple(event.source_event_id for event in self.events)
        if len(set(event_ids)) != len(event_ids):
            raise ValueError("duplicate source_event_id values detected")
