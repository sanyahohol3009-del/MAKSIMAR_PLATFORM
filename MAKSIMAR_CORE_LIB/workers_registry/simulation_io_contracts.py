from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SimulationScenarioType = Literal[
    "control_validation",
    "safety_regression",
    "runtime_pressure_probe",
]


SimulationBackendKind = Literal[
    "python",
    "native",
    "gpu",
    "fallback",
]


@dataclass(frozen=True, slots=True)
class SimulationEngineRequest:
    """Engine-neutral request contract for simulation workloads."""

    task_id: str
    scenario_type: SimulationScenarioType
    iteration_budget: int
    input_payload_ref: str
    requires_gpu: bool
    degraded_allowed: bool
    trace_id: str


@dataclass(frozen=True, slots=True)
class SimulationEngineResult:
    """Engine-neutral result contract for simulation workloads."""

    task_id: str
    backend_kind: SimulationBackendKind
    status: str
    score: float
    output_payload_ref: str
    summary: str
    trace_id: str
