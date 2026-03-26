from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control.admission_runtime_models import (
    AdmissionRuntimeContract,
    AdmissionRuntimeState,
)
from MAKSIMAR_CORE_LIB.execution_control.degraded_runtime_models import (
    DegradedRuntimeContract,
    DegradedRuntimeState,
)
from MAKSIMAR_CORE_LIB.execution_control.execution_runtime_shell_models import (
    ExecutionRuntimeShellContract,
)
from MAKSIMAR_CORE_LIB.execution_control.lease_runtime_models import (
    LeaseRuntimeContract,
    LeaseRuntimeState,
)
from MAKSIMAR_CORE_LIB.execution_control.queue_runtime_models import (
    QueueRuntimeContract,
    QueueRuntimeState,
)
from MAKSIMAR_CORE_LIB.execution_control.scheduler_runtime_models import (
    SchedulerRuntimeContract,
    SchedulerRuntimeState,
)


def build_queue_runtime_contract() -> QueueRuntimeContract:
    """Build canonical queue runtime contract."""
    return QueueRuntimeContract(
        total_queues=2,
        queues=(
            QueueRuntimeState(
                queue_name="critical_queue",
                queued_tasks=2,
                running_tasks=1,
                overloaded=False,
            ),
            QueueRuntimeState(
                queue_name="high_queue",
                queued_tasks=5,
                running_tasks=2,
                overloaded=True,
            ),
        ),
    )


def build_lease_runtime_contract() -> LeaseRuntimeContract:
    """Build canonical lease runtime contract."""
    return LeaseRuntimeContract(
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


def build_scheduler_runtime_contract() -> SchedulerRuntimeContract:
    """Build canonical scheduler runtime contract."""
    return SchedulerRuntimeContract(
        total_schedulers=2,
        schedulers=(
            SchedulerRuntimeState(
                scheduler_id="scheduler_001",
                active_node_id="home_001",
                queued_tasks=3,
                degraded_mode_active=False,
            ),
            SchedulerRuntimeState(
                scheduler_id="scheduler_002",
                active_node_id="dev_001",
                queued_tasks=1,
                degraded_mode_active=True,
            ),
        ),
    )


def build_admission_runtime_contract() -> AdmissionRuntimeContract:
    """Build canonical admission runtime contract."""
    return AdmissionRuntimeContract(
        total_requests=2,
        requests=(
            AdmissionRuntimeState(
                request_id="req_001",
                admitted=True,
                denial_reason="",
                policy_checked=True,
            ),
            AdmissionRuntimeState(
                request_id="req_002",
                admitted=False,
                denial_reason="queue_pressure",
                policy_checked=True,
            ),
        ),
    )


def build_degraded_runtime_contract() -> DegradedRuntimeContract:
    """Build canonical degraded runtime contract."""
    return DegradedRuntimeContract(
        total_modes=2,
        modes=(
            DegradedRuntimeState(
                mode_id="degraded_001",
                active=False,
                disabled_feature="voice_duplex",
                reason="normal_operation",
            ),
            DegradedRuntimeState(
                mode_id="degraded_002",
                active=True,
                disabled_feature="background_indexing",
                reason="memory_pressure",
            ),
        ),
    )


def build_execution_runtime_shell_contract() -> ExecutionRuntimeShellContract:
    """Build final shell contract for execution-control runtime layer."""
    queue_runtime = build_queue_runtime_contract()
    lease_runtime = build_lease_runtime_contract()
    scheduler_runtime = build_scheduler_runtime_contract()
    admission_runtime = build_admission_runtime_contract()
    degraded_runtime = build_degraded_runtime_contract()

    return ExecutionRuntimeShellContract(
        shell_id="execution_runtime_shell",
        total_queue_runtime_entries=queue_runtime.total_queues,
        total_lease_runtime_entries=lease_runtime.total_leases,
        total_scheduler_runtime_entries=scheduler_runtime.total_schedulers,
        total_admission_runtime_entries=admission_runtime.total_requests,
        total_degraded_runtime_entries=degraded_runtime.total_modes,
    )
