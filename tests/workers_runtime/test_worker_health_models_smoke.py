from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_runtime import (
    WorkerHealthContract,
    WorkerHealthEntry,
)


def test_worker_health_models_build() -> None:
    """Worker health models should build successfully."""
    contract = WorkerHealthContract(
        total_workers=3,
        workers=(
            WorkerHealthEntry(
                worker_id="worker_ai_001",
                status="ok",
                active_tasks=1,
                heartbeat_ok=True,
            ),
            WorkerHealthEntry(
                worker_id="worker_sim_001",
                status="ok",
                active_tasks=1,
                heartbeat_ok=True,
            ),
            WorkerHealthEntry(
                worker_id="worker_voice_001",
                status="warning",
                active_tasks=2,
                heartbeat_ok=True,
            ),
        ),
    )

    assert contract.total_workers == 3
    assert len(contract.workers) == 3
    assert contract.workers[0].worker_id == "worker_ai_001"
    assert contract.workers[-1].status == "warning"
