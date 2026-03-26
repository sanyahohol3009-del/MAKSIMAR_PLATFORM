from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    ExecutionLease,
    ExecutionLeaseContract,
)


def test_execution_lease_models_build() -> None:
    lease = ExecutionLease(
        lease_id="lease_001",
        owner_task_id="task_env_001",
        resource_type="simulation_engine",
        active=True,
    )

    contract = ExecutionLeaseContract(
        total_leases=1,
        leases=(lease,),
    )

    assert contract.total_leases == 1
    assert contract.leases[0].lease_id == "lease_001"
