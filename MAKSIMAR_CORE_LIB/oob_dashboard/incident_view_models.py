from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IncidentViewLine:
    """One incident-oriented line for dashboard view."""

    incident_name: str
    status: str
    probable_location: str
    detail_value: int


@dataclass(frozen=True, slots=True)
class DashboardIncidentView:
    """Unified incident view with error localization for dashboard."""

    overall_status: str
    total_lines: int
    lines: list[IncidentViewLine]
