from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class MemoryEntityDefinition:
    """Canonical memory entity definition loaded from contracts."""

    entity_id: str
    version: str
    file_path: Path
    payload: dict[str, Any]


@dataclass(slots=True)
class MemoryLoadResult:
    """Result of loading one memory definition."""

    definition: MemoryEntityDefinition | None
    is_valid: bool
    error: str | None = None
