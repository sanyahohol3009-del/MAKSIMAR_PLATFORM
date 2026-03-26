from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability.deep_observability_shell_models import (
    DeepExecutionObservabilityShellContract,
)
from MAKSIMAR_CORE_LIB.execution_observability.lease_metrics_contract import (
    build_lease_metrics_contract,
)
from MAKSIMAR_CORE_LIB.execution_observability.pressure_metrics_contract import (
    build_pressure_metrics_contract,
)
from MAKSIMAR_CORE_LIB.execution_observability.queue_metrics_contract import (
    build_queue_metrics_contract,
)
from MAKSIMAR_CORE_LIB.execution_observability.worker_saturation_metrics_contract import (
    build_worker_saturation_metrics_contract,
)


def build_deep_execution_observability_shell_contract() -> (
    DeepExecutionObservabilityShellContract
):
    """Build final shell contract for deep execution observability layer."""
    queue_metrics = build_queue_metrics_contract()
    lease_metrics = build_lease_metrics_contract()
    pressure_metrics = build_pressure_metrics_contract()
    worker_saturation_metrics = build_worker_saturation_metrics_contract()

    return DeepExecutionObservabilityShellContract(
        shell_id="execution_observability_deep_shell",
        total_queue_metrics=queue_metrics.total_queues,
        total_lease_metrics=lease_metrics.total_leases,
        total_pressure_metrics=pressure_metrics.total_metrics,
        total_worker_saturation_metrics=worker_saturation_metrics.total_workers,
    )
