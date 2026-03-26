from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SimulationEvaluationHandoff:
    """Canonical handoff from simulation layer to evaluation layer."""

    simulation_execution_id: str
    simulation_backend_id: str
    simulation_payload_ref: str
    evaluation_execution_id: str
    evaluation_id: str
    handoff_status: str
