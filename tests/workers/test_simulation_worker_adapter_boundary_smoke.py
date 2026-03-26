from __future__ import annotations

from MAKSIMAR_SERVER.WORKERS.simulation_worker import (
    SimulationEngineRequest,
    build_simulation_worker_runtime,
)


def test_simulation_worker_runtime_builds() -> None:
    """Simulation worker runtime should build successfully."""
    runtime = build_simulation_worker_runtime()

    assert runtime.worker_id == "worker_sim_001"


def test_simulation_worker_runtime_executes_through_adapter() -> None:
    """Simulation worker runtime should execute via adapter boundary."""
    runtime = build_simulation_worker_runtime()

    request = SimulationEngineRequest(
        task_id="task_sim_001",
        scenario_type="control_validation",
        iteration_budget=50,
        input_payload_ref="artifact://simulation/task_sim_001/input",
        requires_gpu=False,
        degraded_allowed=True,
        trace_id="trace_exec_001",
    )

    result = runtime.execute_task(request)

    assert result.task_id == "task_sim_001"
    assert result.backend_kind == "python"
    assert result.status == "completed"
    assert result.output_payload_ref == "artifact://simulation/task_sim_001/result"
