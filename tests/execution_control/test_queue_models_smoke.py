from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    ExecutionQueueContract,
    ExecutionQueueState,
)


def test_execution_queue_models_build() -> None:
    queue = ExecutionQueueState(
        queue_name="critical_queue",
        queued_tasks=4,
        max_tasks=32,
        overloaded=False,
    )

    contract = ExecutionQueueContract(
        total_queues=1,
        queues=(queue,),
    )

    assert contract.total_queues == 1
    assert contract.queues[0].queue_name == "critical_queue"
