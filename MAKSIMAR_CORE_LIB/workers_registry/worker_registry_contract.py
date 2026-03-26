from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_registry.worker_models import (
    WorkerEntry,
    WorkerRegistryContract,
)


def build_worker_registry_contract() -> WorkerRegistryContract:
    """Build unified canonical worker registry contract."""

    workers = (
        WorkerEntry(
            worker_id="worker_ai_001",
            worker_type="ai_worker",
            target_node="home_001",
            active=True,
        ),
        WorkerEntry(
            worker_id="worker_sim_001",
            worker_type="simulation_worker",
            target_node="home_001",
            active=True,
        ),
        WorkerEntry(
            worker_id="worker_voice_001",
            worker_type="voice_worker",
            target_node="dev_001",
            active=True,
        ),
    )

    return WorkerRegistryContract(
        total_workers=len(workers),
        workers=workers,
    )
