from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter import (
    build_foundation_live_status_snapshot,
)


FoundationIncidentSeverity = Literal[
    "info",
    "warning",
    "critical",
]

FoundationTruthScope = Literal[
    "runtime",
    "guard",
    "core_guard",
    "kernel_guard",
]

FoundationFailureStage = Literal[
    "runtime_execution",
    "stop_gate_watch",
    "core_guard_enforcement",
    "kernel_watchdog_supervision",
]


@dataclass(frozen=True)
class FoundationIncidentFailureLocalizationEntry:
    """Canonical incident/failure localization entry for foundation dashboards."""

    localization_entry_id: str
    panel_id: str
    truth_scope: FoundationTruthScope
    display_title: str
    failure_stage: FoundationFailureStage
    derived_state: str
    incident_visible: bool
    failure_visible: bool
    severity: FoundationIncidentSeverity
    suspected_source_file: str
    description: str


@dataclass(frozen=True)
class FoundationIncidentFailureLocalizationView:
    """Canonical incident/failure localization view for foundation dashboards."""

    view_id: str
    total_entries: int
    visible_incident_entries: int
    visible_failure_entries: int
    critical_entries: int
    warning_entries: int
    info_entries: int
    entries: tuple[FoundationIncidentFailureLocalizationEntry, ...]


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

_SCOPE_TO_STAGE = {
    "runtime": "runtime_execution",
    "guard": "stop_gate_watch",
    "core_guard": "core_guard_enforcement",
    "kernel_guard": "kernel_watchdog_supervision",
}

_SCOPE_TO_SOURCE_FILE = {
    "runtime": "SUPERVISOR/process_supervisor.py",
    "guard": "CORE_ROOT/stop_gate_watcher.py",
    "core_guard": "CORE_ROOT/core_guard.py",
    "kernel_guard": "CORE_ROOT/kernel_watchdog.py",
}


def _severity_for_state(derived_state: str) -> FoundationIncidentSeverity:
    """Map derived foundation state to incident severity."""
    if derived_state == "BROKEN":
        return "critical"
    if derived_state == "DEGRADED":
        return "warning"
    if derived_state in {"DEAD", "WARMING_UP"}:
        return "warning"
    return "info"


def _incident_visible_for_state(derived_state: str) -> bool:
    """Return whether incident visibility should be enabled for a state."""
    return derived_state in {"DEAD", "DEGRADED", "BROKEN", "WARMING_UP"}


def _failure_visible_for_state(derived_state: str) -> bool:
    """Return whether failure visibility should be enabled for a state."""
    return derived_state in {"DEAD", "DEGRADED", "BROKEN"}


def build_foundation_incident_failure_localization_view() -> (
    FoundationIncidentFailureLocalizationView
):
    """Build canonical incident/failure localization view from live foundation state."""
    snapshot = build_foundation_live_status_snapshot()

    entries = []
    for record in snapshot.records:
        truth_scope = record.truth_scope
        derived_state = record.derived_state

        entries.append(
            FoundationIncidentFailureLocalizationEntry(
                localization_entry_id=f"foundationfailure_{truth_scope}_001",
                panel_id=_SCOPE_TO_PANEL[truth_scope],
                truth_scope=truth_scope,
                display_title=_SCOPE_TO_TITLE[truth_scope],
                failure_stage=_SCOPE_TO_STAGE[truth_scope],
                derived_state=derived_state,
                incident_visible=_incident_visible_for_state(derived_state),
                failure_visible=_failure_visible_for_state(derived_state),
                severity=_severity_for_state(derived_state),
                suspected_source_file=_SCOPE_TO_SOURCE_FILE[truth_scope],
                description=(
                    "Canonical incident/failure localization entry derived from "
                    f"live foundation status for scope={truth_scope}."
                ),
            )
        )

    entry_tuple = tuple(entries)

    return FoundationIncidentFailureLocalizationView(
        view_id="foundation_incident_failure_localization_view_001",
        total_entries=len(entry_tuple),
        visible_incident_entries=sum(
            1 for entry in entry_tuple if entry.incident_visible
        ),
        visible_failure_entries=sum(
            1 for entry in entry_tuple if entry.failure_visible
        ),
        critical_entries=sum(1 for entry in entry_tuple if entry.severity == "critical"),
        warning_entries=sum(1 for entry in entry_tuple if entry.severity == "warning"),
        info_entries=sum(1 for entry in entry_tuple if entry.severity == "info"),
        entries=entry_tuple,
    )
