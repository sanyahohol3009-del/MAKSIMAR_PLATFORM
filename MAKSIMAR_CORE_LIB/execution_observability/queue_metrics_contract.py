from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    build_queue_runtime_contract,
)
from MAKSIMAR_CORE_LIB.execution_observability.queue_metrics_models import (
    QueueMetricEntry,
    QueueMetricsContract,
)


def build_queue_metrics_contract() -> QueueMetricsContract:
    """Build unified deep queue metrics contract."""
    runtime = build_queue_runtime_contract()

    queues = tuple(
        QueueMetricEntry(
            queue_name=queue.queue_name,
            queued_tasks=queue.queued_tasks,
            running_tasks=queue.running_tasks,
            overloaded=queue.overloaded,
        )
        for queue in runtime.queues
    )

    return QueueMetricsContract(
        total_queues=len(queues),
        queues=queues,
    )
