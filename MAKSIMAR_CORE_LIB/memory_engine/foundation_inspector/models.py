from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


MemoryInspectorSeverity = Literal["info", "warning", "critical"]
MemoryInspectorStatus = Literal["fresh", "stale", "missing"]
MemoryTruthLevel = Literal[
    "validated_project_fact",
    "canonical_rule",
    "derived_observation",
]
MemoryObjectType = Literal[
    "architecture_decision",
    "incident",
    "roadmap_checkpoint",
    "foundation_checkpoint",
]


@dataclass(frozen=True, slots=True)
class MemoryHeartbeatSnapshot:
    """Canonical heartbeat snapshot for the memory foundation inspector."""

    source_name: str
    status: MemoryInspectorStatus
    age_seconds: float | None
    timestamp_wall: str | None
    timestamp_monotonic: float | None
    pid: int | None

    def __post_init__(self) -> None:
        if not self.source_name.strip():
            raise ValueError("source_name must not be empty")

        if self.status == "fresh":
            if self.age_seconds is None:
                raise ValueError("fresh heartbeat must provide age_seconds")
            if self.age_seconds < 0:
                raise ValueError("age_seconds must be >= 0")

        if self.status == "stale":
            if self.age_seconds is None:
                raise ValueError("stale heartbeat must provide age_seconds")
            if self.age_seconds < 0:
                raise ValueError("age_seconds must be >= 0")

        if self.status == "missing":
            if self.age_seconds is not None:
                raise ValueError("missing heartbeat must not provide age_seconds")
            if self.timestamp_wall is not None:
                raise ValueError("missing heartbeat must not provide timestamp_wall")
            if self.timestamp_monotonic is not None:
                raise ValueError(
                    "missing heartbeat must not provide timestamp_monotonic"
                )
            if self.pid is not None:
                raise ValueError("missing heartbeat must not provide pid")


@dataclass(frozen=True, slots=True)
class MemoryInspectorAlert:
    """Canonical alert emitted by the memory foundation inspector."""

    severity: MemoryInspectorSeverity
    code: str
    summary: str
    details: str | None = None

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise ValueError("code must not be empty")
        if not self.summary.strip():
            raise ValueError("summary must not be empty")


@dataclass(frozen=True, slots=True)
class MemoryObjectPreview:
    """Minimal preview object for future dashboard/timeline surfaces."""

    memory_id: str
    memory_type: MemoryObjectType
    title: str
    one_line_summary: str
    truth_level: MemoryTruthLevel
    status: str

    def __post_init__(self) -> None:
        if not self.memory_id.strip():
            raise ValueError("memory_id must not be empty")
        if not self.title.strip():
            raise ValueError("title must not be empty")
        if not self.one_line_summary.strip():
            raise ValueError("one_line_summary must not be empty")
        if not self.status.strip():
            raise ValueError("status must not be empty")


@dataclass(frozen=True, slots=True)
class MemoryFoundationInspectorReadModel:
    """Read-only memory foundation inspector state for preview/observability."""

    heartbeat: MemoryHeartbeatSnapshot
    memory_engine_alive: bool
    memory_registry_alive: bool
    retrieval_path_ready: bool
    preview: MemoryObjectPreview | None
    alert: MemoryInspectorAlert | None

    def __post_init__(self) -> None:
        if self.heartbeat.status == "missing" and self.retrieval_path_ready:
            raise ValueError(
                "retrieval_path_ready must not be True when heartbeat is missing"
            )
