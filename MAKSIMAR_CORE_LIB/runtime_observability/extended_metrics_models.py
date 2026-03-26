from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExtendedRuntimeMetric:
    """One extended runtime metric for observability expansion."""

    metric_name: str
    metric_value: int
    metric_unit: str


@dataclass(frozen=True, slots=True)
class ExtendedRuntimeMetricsContract:
    """Unified extended runtime metrics contract."""

    total_metrics: int
    metrics: tuple[ExtendedRuntimeMetric, ...]
