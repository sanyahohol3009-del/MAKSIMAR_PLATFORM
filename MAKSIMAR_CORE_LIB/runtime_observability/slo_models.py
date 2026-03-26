from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


AlertLevel = Literal[
    "info",
    "warning",
    "critical",
]


@dataclass(frozen=True, slots=True)
class SLOIndicator:
    """One SLO / alert semantics indicator."""

    indicator_name: str
    alert_level: AlertLevel
    service_impact: str


@dataclass(frozen=True, slots=True)
class SLOAlertSemanticsContract:
    """Unified SLO / alert semantics contract."""

    total_indicators: int
    indicators: tuple[SLOIndicator, ...]
