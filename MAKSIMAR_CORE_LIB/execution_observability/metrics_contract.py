from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    build_execution_control_shell_contract,
)
from MAKSIMAR_CORE_LIB.execution_observability.metrics_models import (
    ExecutionMetric,
    ExecutionMetricsContract,
)


def build_execution_metrics_contract() -> ExecutionMetricsContract:
    """Build unified execution observability metrics contract."""
    shell = build_execution_control_shell_contract()

    metrics = (
        ExecutionMetric(
            metric_name="queue_depth",
            metric_value=shell.total_queues,
            metric_unit="queues",
        ),
        ExecutionMetric(
            metric_name="lease_count",
            metric_value=shell.total_leases,
            metric_unit="leases",
        ),
        ExecutionMetric(
            metric_name="running_tasks",
            metric_value=shell.total_tasks,
            metric_unit="tasks",
        ),
        ExecutionMetric(
            metric_name="admission_decisions",
            metric_value=shell.total_admission_decisions,
            metric_unit="decisions",
        ),
        ExecutionMetric(
            metric_name="execution_routes",
            metric_value=shell.total_routes,
            metric_unit="routes",
        ),
    )

    return ExecutionMetricsContract(
        total_metrics=len(metrics),
        metrics=metrics,
    )
