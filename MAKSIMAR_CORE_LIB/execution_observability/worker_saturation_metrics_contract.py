from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability.worker_saturation_metrics_models import (
    WorkerSaturationMetricEntry,
    WorkerSaturationMetricsContract,
)
from MAKSIMAR_CORE_LIB.workers_runtime import (
    build_worker_load_contract,
)


def build_worker_saturation_metrics_contract() -> WorkerSaturationMetricsContract:
    """Build unified worker saturation metrics contract."""
    runtime = build_worker_load_contract()

    workers = tuple(
        WorkerSaturationMetricEntry(
            worker_id=worker.worker_id,
            active_tasks=worker.active_tasks,
            max_concurrency=worker.max_concurrency,
            saturation_level=worker.saturation_level,
        )
        for worker in runtime.workers
    )

    return WorkerSaturationMetricsContract(
        total_workers=len(workers),
        workers=workers,
    )
