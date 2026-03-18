from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class SimulationRequestDefinition:
    """Canonical simulation request definition loaded from contracts."""

    request_id: str
    version: str
    file_path: Path
    payload: dict[str, Any]


@dataclass(slots=True)
class SimulationLoadResult:
    """Result of loading one simulation definition."""

    definition: SimulationRequestDefinition | None
    is_valid: bool
    error: str | None = None
