from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionMetric:
    """Canonical execution observability metric."""

    metric_name: str
    metric_value: int
    metric_unit: str


@dataclass(frozen=True, slots=True)
class ExecutionMetricsContract:
    """Unified execution observability metrics contract."""

    total_metrics: int
    metrics: tuple[ExecutionMetric, ...]
