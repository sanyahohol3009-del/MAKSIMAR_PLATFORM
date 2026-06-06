from __future__ import annotations

import MAKSIMAR_SERVER.WORKERS.simulation_worker.backend_selection_policy as backend_policy
from MAKSIMAR_CORE_LIB.node_roles.multi_gpu_profile_models import (
    MultiGpuProfile,
    MultiGpuProfileContract,
)
from MAKSIMAR_SERVER.WORKERS.simulation_worker import (
    SimulationEngineRequest,
    select_simulation_backend,
)


def _build_no_gpu_profile_contract() -> MultiGpuProfileContract:
    nodes = tuple(
        MultiGpuProfile(node_id=node_id, gpu_count=0, accelerators=())
        for node_id in ("mobile_001", "dev_001", "home_001")
    )
    return MultiGpuProfileContract(total_nodes=len(nodes), nodes=nodes)


def _gpu_required_request(task_id: str) -> SimulationEngineRequest:
    return SimulationEngineRequest(
        task_id=task_id,
        scenario_type="runtime_pressure_probe",
        iteration_budget=25,
        input_payload_ref=f"artifact://simulation/{task_id}/input",
        requires_gpu=True,
        degraded_allowed=True,
        trace_id=f"trace_{task_id}",
    )


def test_simulation_backend_selection_policy_builds() -> None:
    request = SimulationEngineRequest(
        task_id="task_sim_001",
        scenario_type="control_validation",
        iteration_budget=50,
        input_payload_ref="artifact://simulation/task_sim_001/input",
        requires_gpu=False,
        degraded_allowed=True,
        trace_id="trace_exec_001",
    )

    decision = select_simulation_backend(node_id="dev_001", request=request)

    assert decision.task_id == "task_sim_001"
    assert decision.node_id == "dev_001"
    assert decision.selected_backend in ("python", "fallback")


def test_simulation_backend_selection_policy_gpu_required_matches_current_hardware() -> None:
    decision = select_simulation_backend(
        node_id="dev_001",
        request=_gpu_required_request("task_sim_real_gpu_path"),
    )

    assert decision.task_id == "task_sim_real_gpu_path"
    assert decision.node_id == "dev_001"
    assert decision.selected_backend in ("python", "fallback")

    if decision.selected_backend == "python":
        assert decision.decision_status == "selected"
        assert decision.degraded_mode_required is False
        assert decision.reason == "python_backend_policy_match"
    else:
        assert decision.decision_status == "fallback_selected"
        assert decision.degraded_mode_required is True
        assert decision.reason in {
            "feature_gate_unsupported",
            "node_degraded_active",
            "gpu_required_but_unavailable",
            "runtime_pressure_too_high",
            "latency_path_under_pressure",
            "script_support_unavailable",
        }


def test_simulation_backend_selection_policy_uses_fallback_when_gpu_unavailable_simulated(monkeypatch) -> None:
    monkeypatch.setattr(
        backend_policy,
        "build_multi_gpu_profile_contract",
        _build_no_gpu_profile_contract,
    )

    decision = select_simulation_backend(
        node_id="dev_001",
        request=_gpu_required_request("task_sim_no_gpu_simulated"),
    )

    assert decision.selected_backend == "fallback"
    assert decision.decision_status == "fallback_selected"
    assert decision.reason == "gpu_required_but_unavailable"
    assert decision.degraded_mode_required is True
