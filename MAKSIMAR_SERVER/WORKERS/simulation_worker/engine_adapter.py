from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from MAKSIMAR_SERVER.WORKERS.simulation_worker.io_contracts import (
    SimulationEngineRequest,
    SimulationEngineResult,
)


class SimulationEngine(Protocol):
    """Protocol for swappable simulation engines."""

    def run(self, request: SimulationEngineRequest) -> SimulationEngineResult:
        """Execute a simulation request and return engine-neutral result."""


@dataclass(frozen=True, slots=True)
class SimulationEngineAdapter:
    """Adapter boundary between worker runtime and compute engine."""

    engine: SimulationEngine

    def execute(self, request: SimulationEngineRequest) -> SimulationEngineResult:
        """Forward request to engine through stable adapter boundary."""
        return self.engine.run(request)
