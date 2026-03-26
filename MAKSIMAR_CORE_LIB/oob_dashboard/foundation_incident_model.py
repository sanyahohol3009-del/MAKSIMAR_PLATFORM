from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


FoundationIncidentState = Literal[
    "NEW",
    "ACTIVE",
    "CONFIRMED",
    "RECOVERED",
    "ARCHIVED",
]

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
class FoundationIncidentEntry:
    """Canonical incident model entry for foundation dashboard hardening."""

    incident_id: str
    incident_state: FoundationIncidentState
    source_component: FoundationTruthScope
    failing_stage: FoundationFailureStage
    truth_source_trigger: str
    severity: FoundationIncidentSeverity
    reason: str
    kill_chain_triggered: bool
    created_at_wall: float
    created_at_monotonic: float
    recovered_at_monotonic: float | None
    description: str


@dataclass(frozen=True)
class FoundationIncidentModel:
    """Canonical incident model for foundation dashboard hardening."""

    total_entries: int
    new_entries: int
    active_entries: int
    confirmed_entries: int
    recovered_entries: int
    archived_entries: int
    critical_entries: int
    warning_entries: int
    info_entries: int
    entries: tuple[FoundationIncidentEntry, ...]


def build_foundation_incident_model() -> FoundationIncidentModel:
    """Build canonical foundation incident model."""
    entries = (
        FoundationIncidentEntry(
            incident_id="foundationincident_runtime_001",
            incident_state="ACTIVE",
            source_component="runtime",
            failing_stage="runtime_execution",
            truth_source_trigger="heartbeat_truth",
            severity="warning",
            reason="Runtime incident placeholder model entry for dashboard hardening.",
            kill_chain_triggered=False,
            created_at_wall=0.0,
            created_at_monotonic=0.0,
            recovered_at_monotonic=None,
            description="Canonical runtime incident model entry.",
        ),
        FoundationIncidentEntry(
            incident_id="foundationincident_guard_001",
            incident_state="ACTIVE",
            source_component="guard",
            failing_stage="stop_gate_watch",
            truth_source_trigger="heartbeat_truth",
            severity="warning",
            reason="Stop-gate watcher incident placeholder model entry.",
            kill_chain_triggered=False,
            created_at_wall=0.0,
            created_at_monotonic=0.0,
            recovered_at_monotonic=None,
            description="Canonical guard incident model entry.",
        ),
        FoundationIncidentEntry(
            incident_id="foundationincident_core_guard_001",
            incident_state="ACTIVE",
            source_component="core_guard",
            failing_stage="core_guard_enforcement",
            truth_source_trigger="heartbeat_truth",
            severity="warning",
            reason="Core guard incident placeholder model entry.",
            kill_chain_triggered=False,
            created_at_wall=0.0,
            created_at_monotonic=0.0,
            recovered_at_monotonic=None,
            description="Canonical core guard incident model entry.",
        ),
        FoundationIncidentEntry(
            incident_id="foundationincident_kernel_guard_001",
            incident_state="ACTIVE",
            source_component="kernel_guard",
            failing_stage="kernel_watchdog_supervision",
            truth_source_trigger="heartbeat_truth",
            severity="critical",
            reason="Kernel watchdog incident placeholder model entry.",
            kill_chain_triggered=True,
            created_at_wall=0.0,
            created_at_monotonic=0.0,
            recovered_at_monotonic=None,
            description="Canonical kernel guard incident model entry.",
        ),
    )

    return FoundationIncidentModel(
        total_entries=len(entries),
        new_entries=sum(1 for entry in entries if entry.incident_state == "NEW"),
        active_entries=sum(1 for entry in entries if entry.incident_state == "ACTIVE"),
        confirmed_entries=sum(
            1 for entry in entries if entry.incident_state == "CONFIRMED"
        ),
        recovered_entries=sum(
            1 for entry in entries if entry.incident_state == "RECOVERED"
        ),
        archived_entries=sum(
            1 for entry in entries if entry.incident_state == "ARCHIVED"
        ),
        critical_entries=sum(1 for entry in entries if entry.severity == "critical"),
        warning_entries=sum(1 for entry in entries if entry.severity == "warning"),
        info_entries=sum(1 for entry in entries if entry.severity == "info"),
        entries=entries,
    )
