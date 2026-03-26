from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PressureLevel = Literal[
    "low",
    "medium",
    "high",
]


@dataclass(frozen=True, slots=True)
class PressureMetricEntry:
    """Canonical pressure metric entry."""

    metric_name: str
    pressure_level: PressureLevel
    trigger_active: bool


@dataclass(frozen=True, slots=True)
class PressureMetricsContract:
    """Unified pressure metrics contract."""

    total_metrics: int
    metrics: tuple[PressureMetricEntry, ...]
