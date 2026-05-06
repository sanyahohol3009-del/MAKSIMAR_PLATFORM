from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_status_models import (
    SUPPORTED_MEMORY_STATUSES,
    MemoryStatus,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_type_models import (
    SUPPORTED_MEMORY_TYPES,
    MemoryType,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.project_area_models import (
    SUPPORTED_PROJECT_AREAS,
    ProjectArea,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.truth_level_models import (
    SUPPORTED_TRUTH_LEVELS,
    TruthLevel,
)


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_empty_unique_tuple(values: Tuple[str, ...], field_name: str) -> Tuple[str, ...]:
    if not values:
        raise ValueError(f"{field_name} must not be empty")
    normalized = tuple(v.strip() for v in values)
    if any(not v for v in normalized):
        raise ValueError(f"{field_name} must not contain empty values")
    unique_values = tuple(dict.fromkeys(normalized))
    if len(unique_values) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return unique_values


@dataclass(frozen=True)
class MemorySource:
    source_type: str
    source_ref: str
    timestamp_utc: str

    def __post_init__(self) -> None:
        source_type = _ensure_non_empty_str(self.source_type, "source_type")
        source_ref = _ensure_non_empty_str(self.source_ref, "source_ref")
        timestamp_utc = _ensure_non_empty_str(self.timestamp_utc, "timestamp_utc")

        object.__setattr__(self, "source_type", source_type)
        object.__setattr__(self, "source_ref", source_ref)
        object.__setattr__(self, "timestamp_utc", timestamp_utc)


@dataclass(frozen=True)
class MemoryObject:
    memory_id: str
    memory_type: MemoryType
    title: str
    one_line_summary: str
    status: MemoryStatus
    truth_level: TruthLevel
    project_area: Tuple[ProjectArea, ...]
    source: MemorySource
    affects: Tuple[str, ...]
    next_step_id: str
    next_step_summary: str
    tags: Tuple[str, ...]

    def __post_init__(self) -> None:
        memory_id = _ensure_non_empty_str(self.memory_id, "memory_id")
        title = _ensure_non_empty_str(self.title, "title")
        one_line_summary = _ensure_non_empty_str(
            self.one_line_summary,
            "one_line_summary",
        )
        next_step_id = _ensure_non_empty_str(self.next_step_id, "next_step_id")
        next_step_summary = _ensure_non_empty_str(
            self.next_step_summary,
            "next_step_summary",
        )

        if self.memory_type not in SUPPORTED_MEMORY_TYPES:
            raise ValueError(f"memory_type must be one of {SUPPORTED_MEMORY_TYPES}")

        if self.status not in SUPPORTED_MEMORY_STATUSES:
            raise ValueError(f"status must be one of {SUPPORTED_MEMORY_STATUSES}")

        if self.truth_level not in SUPPORTED_TRUTH_LEVELS:
            raise ValueError(f"truth_level must be one of {SUPPORTED_TRUTH_LEVELS}")

        project_area = _ensure_non_empty_unique_tuple(
            self.project_area,
            "project_area",
        )
        for area in project_area:
            if area not in SUPPORTED_PROJECT_AREAS:
                raise ValueError(f"project_area contains unsupported value: {area}")

        affects = _ensure_non_empty_unique_tuple(self.affects, "affects")
        tags = _ensure_non_empty_unique_tuple(self.tags, "tags")

        object.__setattr__(self, "memory_id", memory_id)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "one_line_summary", one_line_summary)
        object.__setattr__(self, "project_area", project_area)
        object.__setattr__(self, "affects", affects)
        object.__setattr__(self, "tags", tags)
        object.__setattr__(self, "next_step_id", next_step_id)
        object.__setattr__(self, "next_step_summary", next_step_summary)

    @property
    def panel_ready(self) -> bool:
        return True

    @property
    def timeline_ready(self) -> bool:
        return self.status in ("draft", "validated", "deprecated")

    @property
    def filter_ready(self) -> bool:
        return bool(self.tags) and bool(self.project_area)
