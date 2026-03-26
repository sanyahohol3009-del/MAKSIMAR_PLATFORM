from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SimulationExecutionContract:
    """Sandbox boundary contract for simulation execution."""

    execution_id: str
    backend_id: str
    source_definition_id: str
    payload_ref: str
    sandbox_required: bool
    network_access: bool
    write_to_core_allowed: bool
    status: str
