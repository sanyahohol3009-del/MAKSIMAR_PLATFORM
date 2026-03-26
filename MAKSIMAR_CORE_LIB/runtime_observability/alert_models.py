from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


AlertLevel = Literal[
    "info",
    "warning",
    "critical",
]


@dataclass(frozen=True, slots=True)
class AlertSignal:
    """One classified alert signal."""

    incident_name: str
    incident_value: int
    level: AlertLevel
    status: str


@dataclass(frozen=True, slots=True)
class AlertPolicyResult:
    """Result of alert policy evaluation."""

    overall_level: AlertLevel
    total_signals: int
    critical_signals: int
    warning_signals: int
    info_signals: int
    signals: list[AlertSignal]
