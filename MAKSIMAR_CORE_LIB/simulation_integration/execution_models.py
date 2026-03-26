from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SimulationExecutionEnvelope:
    """Execution-level container for simulation request."""

    request_text: str
    backend_id: str
    version: str
    source_definition_id: str

    execution_id: str
    status: str
