from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control.admission_contract import (
    build_admission_contract,
)
from MAKSIMAR_CORE_LIB.execution_control.lease_models import (
    ExecutionLeaseContract,
    ExecutionLease,
)
from MAKSIMAR_CORE_LIB.execution_control.queue_models import (
    ExecutionQueueContract,
    ExecutionQueueState,
)
from MAKSIMAR_CORE_LIB.execution_control.router_contract import (
    build_execution_router_contract,
)
from MAKSIMAR_CORE_LIB.execution_control.scheduler_models import (
    SchedulerContract,
    SchedulerState,
)
from MAKSIMAR_CORE_LIB.execution_control.shell_models import (
    ExecutionControlShellContract,
)
from MAKSIMAR_CORE_LIB.execution_control.state_models import (
    ExecutionState,
    ExecutionStateContract,
)


def build_execution_state_contract() -> ExecutionStateContract:
    """Build canonical execution state contract."""
    return ExecutionStateContract(
        state=ExecutionState(
            total_tasks=10,
            queued_tasks=4,
            running_tasks=6,
            node_health="ok",
            degraded_mode_active=False,
        )
    )


def build_execution_queue_contract() -> ExecutionQueueContract:
    """Build canonical execution queue contract."""
    return ExecutionQueueContract(
        total_queues=1,
        queues=(
            ExecutionQueueState(
                queue_name="critical_queue",
                queued_tasks=4,
                max_tasks=32,
                overloaded=False,
            ),
        ),
    )


def build_execution_lease_contract() -> ExecutionLeaseContract:
    """Build canonical execution lease contract."""
    return ExecutionLeaseContract(
        total_leases=1,
        leases=(
            ExecutionLease(
                lease_id="lease_001",
                owner_task_id="task_env_001",
                resource_type="simulation_engine",
                active=True,
            ),
        ),
    )


def build_scheduler_contract() -> SchedulerContract:
    """Build canonical scheduler contract."""
    return SchedulerContract(
        total_schedulers=1,
        schedulers=(
            SchedulerState(
                scheduler_id="scheduler_001",
                active_node="home_node",
                running_tasks=3,
                degraded_mode_active=False,
            ),
        ),
    )


def build_execution_control_shell_contract() -> ExecutionControlShellContract:
    """Build final execution control shell contract."""
    state_contract = build_execution_state_contract()
    queue_contract = build_execution_queue_contract()
    lease_contract = build_execution_lease_contract()
    scheduler_contract = build_scheduler_contract()
    admission_contract = build_admission_contract()
    router_contract = build_execution_router_contract()

    return ExecutionControlShellContract(
        shell_id="execution_control_shell",
        total_tasks=state_contract.state.total_tasks,
        total_queues=queue_contract.total_queues,
        total_leases=lease_contract.total_leases,
        total_schedulers=scheduler_contract.total_schedulers,
        total_admission_decisions=admission_contract.total_decisions,
        total_routes=router_contract.total_routes,
        degraded_mode_active=state_contract.state.degraded_mode_active,
    )
