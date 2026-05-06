from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class PanelProjection:
    memory_id: str
    title: str
    status: str
    truth_level: str
    project_area: Tuple[str, ...]
    affected_files: Tuple[str, ...]
    panel_ready: bool

    def __post_init__(self) -> None:
        memory_id = _ensure_non_empty_str(self.memory_id, "memory_id")
        title = _ensure_non_empty_str(self.title, "title")
        status = _ensure_non_empty_str(self.status, "status")
        truth_level = _ensure_non_empty_str(self.truth_level, "truth_level")

        if not self.project_area:
            raise ValueError("project_area must not be empty")
        if not self.affected_files:
            raise ValueError("affected_files must not be empty")
        if not self.panel_ready:
            raise ValueError("panel_ready must be True")

        object.__setattr__(self, "memory_id", memory_id)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "truth_level", truth_level)
