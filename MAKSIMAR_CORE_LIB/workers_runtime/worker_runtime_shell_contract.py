from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_runtime.worker_health_models import (
    WorkerHealthContract,
    WorkerHealthEntry,
)
from MAKSIMAR_CORE_LIB.workers_runtime.worker_load_contract import (
    build_worker_load_contract,
)
from MAKSIMAR_CORE_LIB.workers_runtime.worker_runtime_shell_models import (
    WorkerRuntimeShellContract,
)


def build_worker_health_contract() -> WorkerHealthContract:
    """Build canonical worker health contract."""
    return WorkerHealthContract(
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


def build_worker_runtime_shell_contract() -> WorkerRuntimeShellContract:
    """Build final shell contract for workers runtime / health layer."""
    health = build_worker_health_contract()
    load = build_worker_load_contract()

    return WorkerRuntimeShellContract(
        shell_id="worker_runtime_shell",
        total_health_entries=health.total_workers,
        total_load_entries=load.total_workers,
    )
