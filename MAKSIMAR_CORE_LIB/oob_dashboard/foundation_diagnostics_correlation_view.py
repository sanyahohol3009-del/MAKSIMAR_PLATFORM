from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_failure_localization_view import (
    build_foundation_incident_failure_localization_view,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter import (
    build_foundation_live_status_snapshot,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_stalled_stage_command_flow_view import (
    build_foundation_stalled_stage_command_flow_view,
)


@dataclass(frozen=True)
class FoundationDiagnosticsCorrelationEntry:
    """Canonical correlated diagnostics entry for foundation dashboards."""

    correlation_entry_id: str
    panel_id: str
    truth_scope: str
    display_title: str
    derived_state: str
    flow_state: str
    severity: str
    failure_stage: str
    incident_visible: bool
    failure_visible: bool
    stalled_stage_visible: bool
    suspected_source_file: str
    description: str


@dataclass(frozen=True)
class FoundationDiagnosticsCorrelationView:
    """Canonical correlated diagnostics view for foundation dashboards."""

    view_id: str
    total_entries: int
    alive_entries: int
    degraded_entries: int
    dead_entries: int
    broken_entries: int
    flowing_entries: int
    stalled_entries: int
    incident_visible_entries: int
    failure_visible_entries: int
    entries: tuple[FoundationDiagnosticsCorrelationEntry, ...]


def build_foundation_diagnostics_correlation_view() -> (
    FoundationDiagnosticsCorrelationView
):
    """Build canonical correlated diagnostics view for foundation dashboards."""
    live_snapshot = build_foundation_live_status_snapshot()
    incident_view = build_foundation_incident_failure_localization_view()
    flow_view = build_foundation_stalled_stage_command_flow_view()

    incident_by_scope = {entry.truth_scope: entry for entry in incident_view.entries}
    flow_by_scope = {entry.truth_scope: entry for entry in flow_view.entries}

    entries = []
    for live_record in live_snapshot.records:
        truth_scope = live_record.truth_scope
        incident_entry = incident_by_scope[truth_scope]
        flow_entry = flow_by_scope[truth_scope]

        panel_id = incident_entry.panel_id

        entries.append(
            FoundationDiagnosticsCorrelationEntry(
                correlation_entry_id=f"foundationdiagnostics_{truth_scope}_001",
                panel_id=panel_id,
                truth_scope=truth_scope,
                display_title=incident_entry.display_title,
                derived_state=live_record.derived_state,
                flow_state=flow_entry.flow_state,
                severity=incident_entry.severity,
                failure_stage=incident_entry.failure_stage,
                incident_visible=incident_entry.incident_visible,
                failure_visible=incident_entry.failure_visible,
                stalled_stage_visible=flow_entry.stalled_stage_visible,
                suspected_source_file=incident_entry.suspected_source_file,
                description=(
                    "Canonical correlated diagnostics entry derived from live "
                    f"state, flow, and failure localization for scope={truth_scope}."
                ),
            )
        )

    entry_tuple = tuple(entries)

    return FoundationDiagnosticsCorrelationView(
        view_id="foundation_diagnostics_correlation_view_001",
        total_entries=len(entry_tuple),
        alive_entries=sum(1 for entry in entry_tuple if entry.derived_state == "ALIVE"),
        degraded_entries=sum(
            1 for entry in entry_tuple if entry.derived_state == "DEGRADED"
        ),
        dead_entries=sum(1 for entry in entry_tuple if entry.derived_state == "DEAD"),
        broken_entries=sum(1 for entry in entry_tuple if entry.derived_state == "BROKEN"),
        flowing_entries=sum(1 for entry in entry_tuple if entry.flow_state == "FLOWING"),
        stalled_entries=sum(1 for entry in entry_tuple if entry.flow_state == "STALLED"),
        incident_visible_entries=sum(
            1 for entry in entry_tuple if entry.incident_visible
        ),
        failure_visible_entries=sum(
            1 for entry in entry_tuple if entry.failure_visible
        ),
        entries=entry_tuple,
    )
