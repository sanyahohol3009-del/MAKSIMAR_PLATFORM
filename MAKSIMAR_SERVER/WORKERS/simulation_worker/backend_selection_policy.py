from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.feature_gating_contract import (
    build_feature_gating_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.multi_gpu_profile_contract import (
    build_multi_gpu_profile_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.node_runtime_health_contract import (
    build_node_runtime_health_contract,
)
from MAKSIMAR_SERVER.WORKERS.simulation_worker.capability_contract import (
    build_simulation_engine_capability_contract,
)
from MAKSIMAR_SERVER.WORKERS.simulation_worker.io_contracts import (
    SimulationEngineRequest,
)


BackendSelectionStatus = Literal[
    "selected",
    "fallback_selected",
]


@dataclass(frozen=True, slots=True)
class SimulationBackendSelectionDecision:
    """Policy decision for simulation backend selection."""

    task_id: str
    node_id: str
    selected_backend: str
    decision_status: BackendSelectionStatus
    reason: str
    degraded_mode_required: bool


def select_simulation_backend(
    *,
    node_id: str,
    request: SimulationEngineRequest,
) -> SimulationBackendSelectionDecision:
    """Select simulation backend using capability, runtime, and policy data."""
    capability = build_simulation_engine_capability_contract()
    runtime = build_node_runtime_health_contract()
    gpu_profiles = build_multi_gpu_profile_contract()
    feature_gates = build_feature_gating_contract()

    runtime_by_node = {entry.node_id: entry for entry in runtime.nodes}
    gpu_by_node = {entry.node_id: entry for entry in gpu_profiles.nodes}
    gates_by_node_feature = {
        (entry.node_id, entry.feature_id): entry for entry in feature_gates.entries
    }

    node_runtime = runtime_by_node[node_id]
    node_gpu = gpu_by_node[node_id]
    simulation_gate = gates_by_node_feature[(node_id, "simulation_task")]

    requires_fast_path = request.scenario_type == "runtime_pressure_probe"
    multilingual_supported = "Cyrillic" in capability.supported_scripts

    if simulation_gate.availability == "unsupported":
        return SimulationBackendSelectionDecision(
            task_id=request.task_id,
            node_id=node_id,
            selected_backend="fallback",
            decision_status="fallback_selected",
            reason="feature_gate_unsupported",
            degraded_mode_required=True,
        )

    if node_runtime.degraded_active:
        return SimulationBackendSelectionDecision(
            task_id=request.task_id,
            node_id=node_id,
            selected_backend="fallback",
            decision_status="fallback_selected",
            reason="node_degraded_active",
            degraded_mode_required=True,
        )

    if request.requires_gpu and node_gpu.gpu_count == 0:
        return SimulationBackendSelectionDecision(
            task_id=request.task_id,
            node_id=node_id,
            selected_backend="fallback",
            decision_status="fallback_selected",
            reason="gpu_required_but_unavailable",
            degraded_mode_required=True,
        )

    if node_runtime.health_score < 50 or node_runtime.queue_depth > 8:
        return SimulationBackendSelectionDecision(
            task_id=request.task_id,
            node_id=node_id,
            selected_backend="fallback",
            decision_status="fallback_selected",
            reason="runtime_pressure_too_high",
            degraded_mode_required=True,
        )

    if requires_fast_path and node_runtime.cpu_pressure_percent > 85:
        return SimulationBackendSelectionDecision(
            task_id=request.task_id,
            node_id=node_id,
            selected_backend="fallback",
            decision_status="fallback_selected",
            reason="latency_path_under_pressure",
            degraded_mode_required=True,
        )

    if not multilingual_supported:
        return SimulationBackendSelectionDecision(
            task_id=request.task_id,
            node_id=node_id,
            selected_backend="fallback",
            decision_status="fallback_selected",
            reason="script_support_unavailable",
            degraded_mode_required=True,
        )

    return SimulationBackendSelectionDecision(
        task_id=request.task_id,
        node_id=node_id,
        selected_backend="python",
        decision_status="selected",
        reason="python_backend_policy_match",
        degraded_mode_required=False,
    )
