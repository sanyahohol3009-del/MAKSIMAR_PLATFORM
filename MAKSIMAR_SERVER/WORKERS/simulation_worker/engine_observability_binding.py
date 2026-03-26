from __future__ import annotations

from MAKSIMAR_SERVER.WORKERS.simulation_worker.backend_selection_policy import (
    select_simulation_backend,
)
from MAKSIMAR_SERVER.WORKERS.simulation_worker.capability_contract import (
    build_simulation_engine_capability_contract,
)
from MAKSIMAR_SERVER.WORKERS.simulation_worker.engine_observability_models import (
    SimulationEngineObservabilityContract,
    SimulationEngineObservabilityRecord,
)
from MAKSIMAR_SERVER.WORKERS.simulation_worker.io_contracts import (
    SimulationEngineRequest,
)
from MAKSIMAR_SERVER.WORKERS.simulation_worker.worker_runtime import (
    build_simulation_worker_runtime,
)


def _measure_latency_ms(request: SimulationEngineRequest, selected_backend: str) -> int:
    """Produce deterministic latency sample for observability binding."""
    if selected_backend == "fallback":
        return 210

    if request.scenario_type == "runtime_pressure_probe":
        return 95

    if request.scenario_type == "safety_regression":
        return 135

    return 120


def build_simulation_engine_observability_contract() -> (
    SimulationEngineObservabilityContract
):
    """Build observability binding for simulation engine executions."""
    capability = build_simulation_engine_capability_contract()
    runtime = build_simulation_worker_runtime()

    requests = (
        SimulationEngineRequest(
            task_id="task_sim_obs_001",
            scenario_type="control_validation",
            iteration_budget=50,
            input_payload_ref="artifact://simulation/task_sim_obs_001/input",
            requires_gpu=False,
            degraded_allowed=True,
            trace_id="trace_obs_001",
        ),
        SimulationEngineRequest(
            task_id="task_sim_obs_002",
            scenario_type="runtime_pressure_probe",
            iteration_budget=25,
            input_payload_ref="artifact://simulation/task_sim_obs_002/input",
            requires_gpu=True,
            degraded_allowed=True,
            trace_id="trace_obs_002",
        ),
    )

    records = []
    node_id = "dev_001"

    for request in requests:
        decision = select_simulation_backend(
            node_id=node_id,
            request=request,
        )

        measured_latency_ms = _measure_latency_ms(
            request=request,
            selected_backend=decision.selected_backend,
        )

        if decision.selected_backend == "python":
            result = runtime.execute_task(request)
            execution_status = result.status
        else:
            execution_status = "fallback_routed"

        backend_mismatch_condition = (
            decision.selected_backend not in capability.compatible_backends
            and decision.selected_backend not in capability.fallback_backends
        )

        unsupported_language_script_fallback = False
        speech_chat_fast_path = request.scenario_type == "runtime_pressure_probe"

        records.append(
            SimulationEngineObservabilityRecord(
                task_id=request.task_id,
                worker_id=runtime.worker_id,
                node_id=node_id,
                selected_backend=decision.selected_backend,
                decision_status=decision.decision_status,
                execution_status=execution_status,
                latency_budget_ms=capability.expected_latency_budget_ms,
                measured_latency_ms=measured_latency_ms,
                fallback_triggered=decision.selected_backend == "fallback",
                backend_mismatch_condition=backend_mismatch_condition,
                unsupported_language_script_fallback=unsupported_language_script_fallback,
                speech_chat_fast_path=speech_chat_fast_path,
                supported_languages_count=len(capability.supported_languages),
                supported_scripts_count=len(capability.supported_scripts),
                trace_id=request.trace_id,
            )
        )

    return SimulationEngineObservabilityContract(
        total_records=len(records),
        records=tuple(records),
    )
