from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_model import (
    build_foundation_incident_model,
)


@dataclass(frozen=True)
class FoundationIncidentSnapshotEntry:
    """Canonical incident snapshot entry for foundation dashboard hardening."""

    snapshot_entry_id: str
    incident_id: str
    source_component: str
    failing_stage: str
    severity: str
    incident_state: str
    kill_chain_triggered: bool
    snapshot_available: bool
    current_incident: bool
    description: str


@dataclass(frozen=True)
class FoundationIncidentSnapshotContract:
    """Canonical incident snapshot contract for foundation dashboard hardening."""

    total_entries: int
    snapshot_available_entries: int
    current_incident_entries: int
    kill_chain_triggered_entries: int
    critical_entries: int
    warning_entries: int
    info_entries: int
    entries: tuple[FoundationIncidentSnapshotEntry, ...]


def build_foundation_incident_snapshot_contract() -> (
    FoundationIncidentSnapshotContract
):
    """Build canonical incident snapshot contract from foundation incident model."""
    model = build_foundation_incident_model()

    entries = tuple(
        FoundationIncidentSnapshotEntry(
            snapshot_entry_id=f"foundation_snapshot_{entry.source_component}_001",
            incident_id=entry.incident_id,
            source_component=entry.source_component,
            failing_stage=entry.failing_stage,
            severity=entry.severity,
            incident_state=entry.incident_state,
            kill_chain_triggered=entry.kill_chain_triggered,
            snapshot_available=True,
            current_incident=entry.incident_state in {"NEW", "ACTIVE", "CONFIRMED"},
            description=(
                "Canonical incident snapshot entry derived from foundation "
                f"incident model for scope={entry.source_component}."
            ),
        )
        for entry in model.entries
    )

    return FoundationIncidentSnapshotContract(
        total_entries=len(entries),
        snapshot_available_entries=sum(
            1 for entry in entries if entry.snapshot_available
        ),
        current_incident_entries=sum(1 for entry in entries if entry.current_incident),
        kill_chain_triggered_entries=sum(
            1 for entry in entries if entry.kill_chain_triggered
        ),
        critical_entries=sum(1 for entry in entries if entry.severity == "critical"),
        warning_entries=sum(1 for entry in entries if entry.severity == "warning"),
        info_entries=sum(1 for entry in entries if entry.severity == "info"),
        entries=entries,
    )
