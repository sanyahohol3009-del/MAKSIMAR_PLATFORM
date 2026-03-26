from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DegradedRuntimeState:
    """Canonical degraded runtime state entry."""

    mode_id: str
    active: bool
    disabled_feature: str
    reason: str


@dataclass(frozen=True, slots=True)
class DegradedRuntimeContract:
    """Unified degraded runtime state contract."""

    total_modes: int
    modes: tuple[DegradedRuntimeState, ...]
