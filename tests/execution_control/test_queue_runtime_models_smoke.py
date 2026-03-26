from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    QueueRuntimeContract,
    QueueRuntimeState,
)


def test_queue_runtime_models_build() -> None:
    """Queue runtime models should build successfully."""
    contract = QueueRuntimeContract(
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

    assert contract.total_queues == 2
    assert len(contract.queues) == 2
    assert contract.queues[0].queue_name == "critical_queue"
    assert contract.queues[-1].overloaded is True
