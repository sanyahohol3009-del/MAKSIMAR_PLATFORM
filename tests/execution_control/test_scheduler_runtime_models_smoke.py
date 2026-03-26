from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    SchedulerRuntimeContract,
    SchedulerRuntimeState,
)


def test_scheduler_runtime_models_build() -> None:
    """Scheduler runtime models should build successfully."""
    contract = SchedulerRuntimeContract(
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

    assert contract.total_schedulers == 2
    assert len(contract.schedulers) == 2
    assert contract.schedulers[0].active_node_id == "home_001"
    assert contract.schedulers[-1].degraded_mode_active is True
