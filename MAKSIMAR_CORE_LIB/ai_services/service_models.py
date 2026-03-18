from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class AIServiceDefinition:
    """Canonical AI service definition loaded from config."""

    service_id: str
    version: str
    file_path: Path
    payload: dict[str, Any]


@dataclass(slots=True)
class AIServiceLoadResult:
    """Result of loading one AI service definition."""

    definition: AIServiceDefinition | None
    is_valid: bool
    error: str | None = None
