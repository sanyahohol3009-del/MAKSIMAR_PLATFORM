from __future__ import annotations

from MAKSIMAR_SERVER.WORKERS.simulation_worker import (
    SimulationEngineRequest,
    select_simulation_backend,
)


def test_simulation_backend_selection_policy_builds() -> None:
    """Backend selection policy should return a decision."""
    request = SimulationEngineRequest(
        task_id="task_sim_001",
        scenario_type="control_validation",
        iteration_budget=50,
        input_payload_ref="artifact://simulation/task_sim_001/input",
        requires_gpu=False,
        degraded_allowed=True,
        trace_id="trace_exec_001",
    )

    decision = select_simulation_backend(
        node_id="dev_001",
        request=request,
    )

    assert decision.task_id == "task_sim_001"
    assert decision.node_id == "dev_001"
    assert decision.selected_backend in ("python", "fallback")


def test_simulation_backend_selection_policy_uses_fallback_when_gpu_required() -> None:
    """Backend selection policy should fallback when GPU is required but unavailable."""
    request = SimulationEngineRequest(
        task_id="task_sim_002",
        scenario_type="runtime_pressure_probe",
        iteration_budget=25,
        input_payload_ref="artifact://simulation/task_sim_002/input",
        requires_gpu=True,
        degraded_allowed=True,
        trace_id="trace_exec_002",
    )

    decision = select_simulation_backend(
        node_id="dev_001",
        request=request,
    )

    assert decision.selected_backend == "fallback"
    assert decision.decision_status == "fallback_selected"
    assert decision.degraded_mode_required is True
