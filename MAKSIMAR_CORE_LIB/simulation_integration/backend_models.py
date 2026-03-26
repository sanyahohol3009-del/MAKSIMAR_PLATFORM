from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SimulationBackendRecord:
    """One simulation backend-oriented record."""

    backend_id: str
    version: str
    source_definition_id: str


@dataclass(frozen=True, slots=True)
class SimulationBackendSummary:
    """Unified summary of simulation backends."""

    total_backends: int
    records: list[SimulationBackendRecord]
