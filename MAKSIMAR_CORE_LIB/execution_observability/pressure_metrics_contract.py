from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability.pressure_metrics_models import (
    PressureMetricEntry,
    PressureMetricsContract,
)
from MAKSIMAR_CORE_LIB.execution_observability.queue_metrics_contract import (
    build_queue_metrics_contract,
)


def build_pressure_metrics_contract() -> PressureMetricsContract:
    """Build unified pressure metrics contract."""
    queue_metrics = build_queue_metrics_contract()

    has_overloaded_queue = any(queue.overloaded for queue in queue_metrics.queues)

    metrics = (
        PressureMetricEntry(
            metric_name="queue_pressure",
            pressure_level="high" if has_overloaded_queue else "low",
            trigger_active=has_overloaded_queue,
        ),
        PressureMetricEntry(
            metric_name="execution_pressure",
            pressure_level="medium",
            trigger_active=False,
        ),
        PressureMetricEntry(
            metric_name="worker_pressure",
            pressure_level="medium",
            trigger_active=False,
        ),
    )

    return PressureMetricsContract(
        total_metrics=len(metrics),
        metrics=metrics,
    )
