from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ActionDefinition:
    """Canonical action definition loaded from contracts."""

    action_id: str
    version: str
    file_path: Path
    payload: dict[str, Any]


@dataclass(slots=True)
class ActionLoadResult:
    """Result of loading one action definition."""

    definition: ActionDefinition | None
    is_valid: bool
    error: str | None = None
