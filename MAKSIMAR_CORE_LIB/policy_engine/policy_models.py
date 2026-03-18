from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class Policy:
    """Canonical runtime representation of one policy document."""

    name: str
    version: str
    file_path: Path
    payload: dict[str, Any]


@dataclass(slots=True)
class PolicyLoadResult:
    """Result of loading a policy."""

    policy: Policy | None
    is_valid: bool
    error: str | None = None
