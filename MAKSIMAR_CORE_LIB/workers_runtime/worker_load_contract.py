from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_runtime.worker_load_models import (
    WorkerLoadContract,
    WorkerLoadEntry,
)


def build_worker_load_contract() -> WorkerLoadContract:
    """Build unified worker load / saturation contract."""

    workers = (
        WorkerLoadEntry(
            worker_id="worker_ai_001",
            active_tasks=1,
            max_concurrency=2,
            saturation_level="medium",
        ),
        WorkerLoadEntry(
            worker_id="worker_sim_001",
            active_tasks=1,
            max_concurrency=1,
            saturation_level="high",
        ),
        WorkerLoadEntry(
            worker_id="worker_voice_001",
            active_tasks=2,
            max_concurrency=4,
            saturation_level="medium",
        ),
    )

    return WorkerLoadContract(
        total_workers=len(workers),
        workers=workers,
    )
