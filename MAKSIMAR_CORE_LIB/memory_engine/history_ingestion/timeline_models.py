from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class TimelineEntry:
    timeline_id: str
    memory_id: str
    timestamp_utc: str
    title: str
    status: str
    timeline_ready: bool

    def __post_init__(self) -> None:
        timeline_id = _ensure_non_empty_str(self.timeline_id, "timeline_id")
        memory_id = _ensure_non_empty_str(self.memory_id, "memory_id")
        timestamp_utc = _ensure_non_empty_str(self.timestamp_utc, "timestamp_utc")
        title = _ensure_non_empty_str(self.title, "title")
        status = _ensure_non_empty_str(self.status, "status")

        if not self.timeline_ready:
            raise ValueError("timeline_ready must be True")

        object.__setattr__(self, "timeline_id", timeline_id)
        object.__setattr__(self, "memory_id", memory_id)
        object.__setattr__(self, "timestamp_utc", timestamp_utc)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "status", status)
