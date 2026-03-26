from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DegradedModeRule:
    """Canonical degraded mode rule."""

    disabled_feature: str
    safety_critical: bool
    remains_active: bool


@dataclass(frozen=True, slots=True)
class DegradedModeContract:
    """Unified degraded mode contract."""

    total_rules: int
    rules: tuple[DegradedModeRule, ...]
