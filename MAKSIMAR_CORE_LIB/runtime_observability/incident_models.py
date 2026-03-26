from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlatformIncidentRecord:
    """One platform incident-oriented signal."""

    incident_name: str
    incident_value: int
    status: str


@dataclass(frozen=True, slots=True)
class PlatformIncidentSnapshot:
    """Unified incident snapshot for platform observability."""

    overall_status: str
    total_incident_signals: int
    failed_signals: int
    records: list[PlatformIncidentRecord]
