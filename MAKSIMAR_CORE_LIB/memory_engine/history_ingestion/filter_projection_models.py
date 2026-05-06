from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class FilterProjection:
    memory_id: str
    status: str
    truth_level: str
    tags: Tuple[str, ...]
    project_area: Tuple[str, ...]
    filter_ready: bool

    def __post_init__(self) -> None:
        memory_id = _ensure_non_empty_str(self.memory_id, "memory_id")
        status = _ensure_non_empty_str(self.status, "status")
        truth_level = _ensure_non_empty_str(self.truth_level, "truth_level")

        if not self.tags:
            raise ValueError("tags must not be empty")
        if not self.project_area:
            raise ValueError("project_area must not be empty")
        if not self.filter_ready:
            raise ValueError("filter_ready must be True")

        object.__setattr__(self, "memory_id", memory_id)
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "truth_level", truth_level)
