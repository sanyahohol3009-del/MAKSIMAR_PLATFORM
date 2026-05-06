from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class JarvisHistoryReadModel:
    memory_ids: Tuple[str, ...]
    titles: Tuple[str, ...]
    readable_by_jarvis: bool
    context_ready: bool

    def __post_init__(self) -> None:
        if not self.memory_ids:
            raise ValueError("memory_ids must not be empty")
        if not self.titles:
            raise ValueError("titles must not be empty")
        if len(self.memory_ids) != len(self.titles):
            raise ValueError("memory_ids and titles must have equal length")
        if any(not _ensure_non_empty_str(v, "memory_id") for v in self.memory_ids):
            raise ValueError("memory_ids must not contain empty strings")
        if any(not _ensure_non_empty_str(v, "title") for v in self.titles):
            raise ValueError("titles must not contain empty strings")
        if not self.readable_by_jarvis:
            raise ValueError("readable_by_jarvis must be True")
        if not self.context_ready:
            raise ValueError("context_ready must be True")
