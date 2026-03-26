from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SimulationEngineKind = Literal[
    "simulation_engine",
]

LatencyProfile = Literal[
    "low_latency",
    "balanced",
    "throughput",
]

SupportedWorkload = Literal[
    "control_validation",
    "safety_regression",
    "runtime_pressure_probe",
]

CpuLoadProfile = Literal[
    "low",
    "medium",
    "high",
]

RamProfile = Literal[
    "light",
    "moderate",
    "heavy",
]

GpuClassRequirement = Literal[
    "cpu_only",
    "integrated_gpu",
    "discrete_gpu",
    "accelerator",
]

BackendRuntimeKind = Literal[
    "python",
    "native",
    "gpu",
    "fallback",
]


@dataclass(frozen=True, slots=True)
class SimulationEngineCapabilityContract:
    """Engine-neutral capability contract for simulation engine."""

    engine_id: str
    engine_kind: SimulationEngineKind
    engine_version: str
    contract_version: str

    language_runtime: str

    supported_workloads: tuple[SupportedWorkload, ...]
    latency_profile: LatencyProfile
    expected_latency_budget_ms: int

    requires_gpu: bool
    required_gpu_class: GpuClassRequirement
    requires_native_runtime: bool

    expected_cpu_load: CpuLoadProfile
    expected_ram_profile: RamProfile

    compatible_backends: tuple[BackendRuntimeKind, ...]
    fallback_backends: tuple[BackendRuntimeKind, ...]
    fallback_available: bool

    supported_languages: tuple[str, ...]
    supported_scripts: tuple[str, ...]

    sandbox_required: bool
    network_access_required: bool
    write_to_core_allowed: bool


def build_simulation_engine_capability_contract() -> (
    SimulationEngineCapabilityContract
):
    """Build simulation engine capability contract."""
    return SimulationEngineCapabilityContract(
        engine_id="sim_engine_python_001",
        engine_kind="simulation_engine",
        engine_version="1.0.0",
        contract_version="1.0",
        language_runtime="python",
        supported_workloads=(
            "control_validation",
            "safety_regression",
            "runtime_pressure_probe",
        ),
        latency_profile="balanced",
        expected_latency_budget_ms=150,
        requires_gpu=False,
        required_gpu_class="cpu_only",
        requires_native_runtime=False,
        expected_cpu_load="medium",
        expected_ram_profile="moderate",
        compatible_backends=(
            "python",
            "fallback",
        ),
        fallback_backends=(
            "fallback",
        ),
        fallback_available=True,
        supported_languages=(
            "en",
            "ru",
            "uk",
            "de",
        ),
        supported_scripts=(
            "Latin",
            "Cyrillic",
        ),
        sandbox_required=True,
        network_access_required=False,
        write_to_core_allowed=False,
    )
