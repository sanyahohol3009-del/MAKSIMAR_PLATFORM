from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    ExecutionState,
    ExecutionStateContract,
)


def test_execution_state_models_build() -> None:
    state = ExecutionState(
        total_tasks=10,
        queued_tasks=4,
        running_tasks=6,
        node_health="ok",
        degraded_mode_active=False,
    )

    contract = ExecutionStateContract(state=state)

    assert contract.state.total_tasks == 10
    assert contract.state.node_health == "ok"
