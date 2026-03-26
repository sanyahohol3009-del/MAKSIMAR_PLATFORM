from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    SchedulerContract,
    SchedulerState,
)


def test_scheduler_models_build() -> None:
    scheduler = SchedulerState(
        scheduler_id="scheduler_001",
        active_node="home_node",
        running_tasks=3,
        degraded_mode_active=False,
    )

    contract = SchedulerContract(
        total_schedulers=1,
        schedulers=(scheduler,),
    )

    assert contract.total_schedulers == 1
    assert contract.schedulers[0].active_node == "home_node"
