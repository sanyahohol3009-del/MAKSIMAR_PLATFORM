from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability.extended_metrics_contract import (
    build_extended_runtime_metrics_contract,
)
from MAKSIMAR_CORE_LIB.runtime_observability.extended_summary_models import (
    ExtendedObservabilitySummary,
    ExtendedSummaryLine,
)


def build_extended_observability_summary() -> ExtendedObservabilitySummary:
    """Build unified extended observability summary."""
    metrics_contract = build_extended_runtime_metrics_contract()

    lines = tuple(
        ExtendedSummaryLine(
            metric_name=metric.metric_name,
            metric_value=metric.metric_value,
            metric_unit=metric.metric_unit,
        )
        for metric in metrics_contract.metrics
    )

    overall_status = "ok"
    if any(line.metric_name == "failed_domains" and line.metric_value > 0 for line in lines):
        overall_status = "warning"

    return ExtendedObservabilitySummary(
        overall_status=overall_status,
        total_lines=len(lines),
        lines=lines,
    )
