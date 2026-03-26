from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.runtime_observability.metrics_models import (
    RuntimeMetric,
    RuntimeSnapshot,
)


@dataclass(frozen=True, slots=True)
class ObservabilitySummaryLine:
    """One readable observability summary line."""

    metric_name: str
    metric_value: int
    status: str


@dataclass(frozen=True, slots=True)
class RuntimeObservabilitySummary:
    """Unified runtime observability summary."""

    overall_status: str
    total_metrics: int
    failed_metrics: int
    lines: list[ObservabilitySummaryLine]


def build_runtime_observability_summary(
    snapshot: RuntimeSnapshot,
    metrics: list[RuntimeMetric],
) -> RuntimeObservabilitySummary:
    """Build unified runtime observability summary."""
    lines = [
        ObservabilitySummaryLine(
            metric_name=metric.metric_name,
            metric_value=metric.metric_value,
            status=metric.status,
        )
        for metric in metrics
    ]

    failed_metrics = sum(1 for metric in metrics if metric.status != "ok")
    overall_status = "ok" if failed_metrics == 0 else "failed"

    return RuntimeObservabilitySummary(
        overall_status=overall_status,
        total_metrics=len(metrics),
        failed_metrics=failed_metrics,
        lines=lines,
    )
