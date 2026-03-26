from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionAlert:
    """Canonical execution alert."""

    alert_name: str
    alert_level: str
    triggered: bool


@dataclass(frozen=True, slots=True)
class ExecutionAlertContract:
    """Unified execution alert contract."""

    total_alerts: int
    alerts: tuple[ExecutionAlert, ...]
