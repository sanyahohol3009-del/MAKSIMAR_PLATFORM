from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_registry import (
    WorkerEntry,
    WorkerRegistryContract,
)


def test_worker_models_build() -> None:
    """Worker registry models should build successfully."""
    contract = WorkerRegistryContract(
        total_workers=3,
        workers=(
            WorkerEntry(
                worker_id="worker_ai_001",
                worker_type="ai_worker",
                target_node="home_node",
                active=True,
            ),
            WorkerEntry(
                worker_id="worker_sim_001",
                worker_type="simulation_worker",
                target_node="home_node",
                active=True,
            ),
            WorkerEntry(
                worker_id="worker_voice_001",
                worker_type="voice_worker",
                target_node="dev_node",
                active=True,
            ),
        ),
    )

    assert contract.total_workers == 3
    assert len(contract.workers) == 3
    assert contract.workers[0].worker_type == "ai_worker"
    assert contract.workers[-1].worker_type == "voice_worker"
