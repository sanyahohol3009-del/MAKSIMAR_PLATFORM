from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionIncident:
    """Canonical execution observability incident."""

    incident_name: str
    severity: str
    active: bool


@dataclass(frozen=True, slots=True)
class ExecutionIncidentContract:
    """Unified execution incident contract."""

    total_incidents: int
    incidents: tuple[ExecutionIncident, ...]
