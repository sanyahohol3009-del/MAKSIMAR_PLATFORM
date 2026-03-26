from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    LeaseRuntimeContract,
    LeaseRuntimeState,
)


def test_lease_runtime_models_build() -> None:
    """Lease runtime models should build successfully."""
    contract = LeaseRuntimeContract(
        total_leases=2,
        leases=(
            LeaseRuntimeState(
                lease_id="lease_001",
                owner_task_id="task_env_001",
                owner_worker_id="worker_ai_001",
                active=True,
            ),
            LeaseRuntimeState(
                lease_id="lease_002",
                owner_task_id="task_env_002",
                owner_worker_id="worker_sim_001",
                active=False,
            ),
        ),
    )

    assert contract.total_leases == 2
    assert len(contract.leases) == 2
    assert contract.leases[0].owner_worker_id == "worker_ai_001"
    assert contract.leases[-1].active is False
