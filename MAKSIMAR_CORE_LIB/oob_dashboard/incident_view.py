from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DashboardIncidentViewLine:
    """Canonical dashboard incident view line."""

    incident_name: str
    status: str
    severity: str
    source_name: str
    probable_location: str
    message: str


@dataclass(frozen=True)
class DashboardIncidentView:
    """Canonical dashboard incident view."""

    view_id: str
    overall_status: str
    total_lines: int
    lines: Tuple[DashboardIncidentViewLine, ...]


def build_dashboard_incident_view() -> DashboardIncidentView:
    """Build canonical dashboard incident view."""
    lines = (
        DashboardIncidentViewLine(
            incident_name="health_failed_domains",
            status="ok",
            severity="info",
            source_name="incident_summary",
            probable_location="MAKSIMAR_CORE_LIB/source_of_truth/health_summary.py",
            message="No failed health domains are active.",
        ),
        DashboardIncidentViewLine(
            incident_name="guard_chain_interrupted",
            status="ok",
            severity="info",
            source_name="incident_guard_chain",
            probable_location="MAKSIMAR_CORE_LIB/oob_dashboard/guard_chain_panel_content_contract.py",
            message="Guard chain is intact.",
        ),
        DashboardIncidentViewLine(
            incident_name="execution_stall_detected",
            status="ok",
            severity="info",
            source_name="incident_execution_flow",
            probable_location="MAKSIMAR_CORE_LIB/oob_dashboard/data_flow_panel_contract.py",
            message="No execution stall detected.",
        ),
        DashboardIncidentViewLine(
            incident_name="incident_localization_ready",
            status="ok",
            severity="info",
            source_name="incident_localization",
            probable_location="MAKSIMAR_CORE_LIB/oob_dashboard/incident_view.py",
            message="Incident localization remains available in read-only mode.",
        ),
    )

    return DashboardIncidentView(
        view_id="dashboard_incident_view_001",
        overall_status="ok",
        total_lines=len(lines),
        lines=lines,
    )
