from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class VoicePolicyDefinition:
    """Canonical voice policy definition loaded from config."""

    policy_id: str
    version: str
    file_path: Path
    payload: dict[str, Any]


@dataclass(slots=True)
class VoiceLoadResult:
    """Result of loading one voice policy definition."""

    definition: VoicePolicyDefinition | None
    is_valid: bool
    error: str | None = None
