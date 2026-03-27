from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_dashboard_view import (
    build_foundation_incident_dashboard_view,
)


IncidentsPanelStatus = Literal[
    "incident_visible",
    "no_incident_visible",
]


@dataclass(frozen=True, slots=True)
class IncidentsPanelContentEntry:
    """Canonical content entry for the incidents panel."""

    panel_id: str
    total_incident_entries: int
    active_incident_entries: int
    history_visible_entries: int
    critical_entries: int
    warning_entries: int
    incidents_panel_status: IncidentsPanelStatus
    visible_in_main_dashboard: bool
    visible_in_oob_dashboard: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class IncidentsPanelContentContract:
    """Canonical content contract for the incidents panel."""

    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    entries: tuple[IncidentsPanelContentEntry, ...]


def build_incidents_panel_content_contract() -> IncidentsPanelContentContract:
    """Build canonical content contract for the incidents panel."""
    incident_dashboard_view = build_foundation_incident_dashboard_view()

    entries = (
        IncidentsPanelContentEntry(
            panel_id="panel_incidents_001",
            total_incident_entries=len(incident_dashboard_view.entries),
            active_incident_entries=sum(
                1
                for entry in incident_dashboard_view.entries
                if entry.current_incident
            ),
            history_visible_entries=sum(
                1
                for entry in incident_dashboard_view.entries
                if entry.history_visible
            ),
            critical_entries=sum(
                1
                for entry in incident_dashboard_view.entries
                if entry.severity == "critical"
            ),
            warning_entries=sum(
                1
                for entry in incident_dashboard_view.entries
                if entry.severity == "warning"
            ),
            incidents_panel_status=(
                "incident_visible"
                if any(entry.current_incident for entry in incident_dashboard_view.entries)
                else "no_incident_visible"
            ),
            visible_in_main_dashboard=True,
            visible_in_oob_dashboard=True,
            read_only=True,
            description=(
                "Canonical incidents panel content contract built from "
                "foundation incident dashboard view."
            ),
        ),
    )

    return IncidentsPanelContentContract(
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        main_dashboard_visible_entries=sum(
            1 for entry in entries if entry.visible_in_main_dashboard
        ),
        oob_visible_entries=sum(
            1 for entry in entries if entry.visible_in_oob_dashboard
        ),
        entries=entries,
    )
