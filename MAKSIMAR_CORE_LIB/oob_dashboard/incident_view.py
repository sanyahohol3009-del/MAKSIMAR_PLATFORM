from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.incident_view_models import (
    DashboardIncidentView,
    IncidentViewLine,
)
from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_platform_incident_snapshot,
    build_runtime_snapshot,
)


def _resolve_location(incident_name: str) -> str:
    """Resolve probable code location for incident signal."""
    if incident_name == "health_failed_domains":
        return "MAKSIMAR_CORE_LIB/runtime_observability/incident_snapshot.py"
    if incident_name == "runtime_documents":
        return "MAKSIMAR_CORE_LIB/runtime_base"
    if incident_name == "event_records":
        return "MAKSIMAR_CORE_LIB/event_bus"
    if incident_name == "self_check_total_items":
        return "MAKSIMAR_CORE_LIB/platform_integration/self_check.py"
    return "unknown"


def build_dashboard_incident_view() -> DashboardIncidentView:
    """Build dashboard incident view with error localization."""
    runtime_snapshot = build_runtime_snapshot()
    incident_snapshot = build_platform_incident_snapshot(runtime_snapshot)

    lines = [
        IncidentViewLine(
            incident_name=record.incident_name,
            status=record.status,
            probable_location=_resolve_location(record.incident_name),
            detail_value=record.incident_value,
        )
        for record in incident_snapshot.records
    ]

    return DashboardIncidentView(
        overall_status=incident_snapshot.overall_status,
        total_lines=len(lines),
        lines=lines,
    )
