from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    ExecutionMetric,
    ExecutionMetricsContract,
)


def test_execution_metrics_models_build() -> None:
    """Execution observability metric models should build successfully."""
    contract = ExecutionMetricsContract(
        total_metrics=3,
        metrics=(
            ExecutionMetric(
                metric_name="queue_depth",
                metric_value=4,
                metric_unit="tasks",
            ),
            ExecutionMetric(
                metric_name="lease_count",
                metric_value=1,
                metric_unit="leases",
            ),
            ExecutionMetric(
                metric_name="running_tasks",
                metric_value=6,
                metric_unit="tasks",
            ),
        ),
    )

    assert contract.total_metrics == 3
    assert len(contract.metrics) == 3
    assert contract.metrics[0].metric_name == "queue_depth"
    assert contract.metrics[-1].metric_name == "running_tasks"
