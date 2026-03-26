from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability.metrics_contract import (
    build_execution_metrics_contract,
)
from MAKSIMAR_CORE_LIB.execution_observability.summary_models import (
    ExecutionSummary,
    ExecutionSummaryLine,
)


def build_execution_summary() -> ExecutionSummary:
    """Build execution observability summary."""
    metrics = build_execution_metrics_contract()

    lines = tuple(
        ExecutionSummaryLine(
            metric_name=m.metric_name,
            value=m.metric_value,
            status="ok" if m.metric_value >= 0 else "error",
        )
        for m in metrics.metrics
    )

    overall_status = "ok"

    return ExecutionSummary(
        overall_status=overall_status,
        total_lines=len(lines),
        lines=lines,
    )
