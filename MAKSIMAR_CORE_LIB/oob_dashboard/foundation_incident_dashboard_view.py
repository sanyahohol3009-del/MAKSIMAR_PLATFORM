from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_history_contract import (
    build_foundation_incident_history_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_snapshot_contract import (
    build_foundation_incident_snapshot_contract,
)


@dataclass(frozen=True)
class FoundationIncidentDashboardViewEntry:
    """Read-only dashboard entry for unified foundation incident visibility."""

    dashboard_entry_id: str
    incident_id: str
    panel_id: str
    source_component: str
    display_title: str
    failing_stage: str
    incident_state: str
    severity: str
    current_incident: bool
    history_visible: bool
    kill_chain_triggered: bool
    archived: bool
    recovered: bool
    read_only: bool
    description: str


@dataclass(frozen=True)
class FoundationIncidentDashboardView:
    """Read-only dashboard view for unified foundation incident visibility."""

    view_id: str
    total_entries: int
    current_incident_entries: int
    history_visible_entries: int
    kill_chain_triggered_entries: int
    archived_entries: int
    recovered_entries: int
    critical_entries: int
    warning_entries: int
    info_entries: int
    entries: tuple[FoundationIncidentDashboardViewEntry, ...]


_SCOPE_TO_PANEL = {
    "runtime": "panel_foundation_runtime_status_001",
    "guard": "panel_foundation_guard_status_001",
    "core_guard": "panel_foundation_core_guard_status_001",
    "kernel_guard": "panel_foundation_kernel_guard_status_001",
}

_SCOPE_TO_TITLE = {
    "runtime": "Runtime Core",
    "guard": "Stop-Gate Watcher",
    "core_guard": "Core Guard",
    "kernel_guard": "Kernel Watchdog",
}


def build_foundation_incident_dashboard_view() -> FoundationIncidentDashboardView:
    """Build unified read-only dashboard view for foundation incidents."""
    snapshot_contract = build_foundation_incident_snapshot_contract()
    history_contract = build_foundation_incident_history_contract()

    history_by_incident_id = {
        entry.incident_id: entry for entry in history_contract.entries
    }

    entries = tuple(
        FoundationIncidentDashboardViewEntry(
            dashboard_entry_id=f"foundation_incident_dashboard_{entry.source_component}_001",
            incident_id=entry.incident_id,
            panel_id=_SCOPE_TO_PANEL[entry.source_component],
            source_component=entry.source_component,
            display_title=_SCOPE_TO_TITLE[entry.source_component],
            failing_stage=entry.failing_stage,
            incident_state=entry.incident_state,
            severity=entry.severity,
            current_incident=entry.current_incident,
            history_visible=history_by_incident_id[entry.incident_id].history_visible,
            kill_chain_triggered=entry.kill_chain_triggered,
            archived=history_by_incident_id[entry.incident_id].archived,
            recovered=history_by_incident_id[entry.incident_id].recovered,
            read_only=True,
            description=(
                "Read-only foundation incident dashboard entry derived from "
                f"incident snapshot/history for scope={entry.source_component}."
            ),
        )
        for entry in snapshot_contract.entries
    )

    return FoundationIncidentDashboardView(
        view_id="foundation_incident_dashboard_view_001",
        total_entries=len(entries),
        current_incident_entries=sum(1 for entry in entries if entry.current_incident),
        history_visible_entries=sum(1 for entry in entries if entry.history_visible),
        kill_chain_triggered_entries=sum(
            1 for entry in entries if entry.kill_chain_triggered
        ),
        archived_entries=sum(1 for entry in entries if entry.archived),
        recovered_entries=sum(1 for entry in entries if entry.recovered),
        critical_entries=sum(1 for entry in entries if entry.severity == "critical"),
        warning_entries=sum(1 for entry in entries if entry.severity == "warning"),
        info_entries=sum(1 for entry in entries if entry.severity == "info"),
        entries=entries,
    )
