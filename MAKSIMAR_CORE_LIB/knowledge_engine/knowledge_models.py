from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class KnowledgeObjectDefinition:
    """Canonical knowledge object definition loaded from contracts."""

    object_id: str
    version: str
    file_path: Path
    payload: dict[str, Any]


@dataclass(slots=True)
class KnowledgeLoadResult:
    """Result of loading one knowledge definition."""

    definition: KnowledgeObjectDefinition | None
    is_valid: bool
    error: str | None = None
