from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


EngineExecutionStatus = Literal[
    "completed",
    "fallback_routed",
    "failed",
]


@dataclass(frozen=True, slots=True)
class SimulationEngineObservabilityRecord:
    """Read-only observability record for a simulation engine execution path."""

    task_id: str
    worker_id: str
    node_id: str
    selected_backend: str
    decision_status: str
    execution_status: EngineExecutionStatus
    latency_budget_ms: int
    measured_latency_ms: int
    fallback_triggered: bool
    backend_mismatch_condition: bool
    unsupported_language_script_fallback: bool
    speech_chat_fast_path: bool
    supported_languages_count: int
    supported_scripts_count: int
    trace_id: str


@dataclass(frozen=True, slots=True)
class SimulationEngineObservabilityContract:
    """Unified observability binding contract for simulation engine executions."""

    total_records: int
    records: tuple[SimulationEngineObservabilityRecord, ...]
