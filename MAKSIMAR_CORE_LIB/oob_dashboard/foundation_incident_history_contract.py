from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_model import (
    build_foundation_incident_model,
)


@dataclass(frozen=True)
class FoundationIncidentHistoryEntry:
    """Canonical incident history entry for foundation dashboard hardening."""

    history_entry_id: str
    incident_id: str
    source_component: str
    failing_stage: str
    incident_state: str
    severity: str
    archived: bool
    recovered: bool
    history_visible: bool
    description: str


@dataclass(frozen=True)
class FoundationIncidentHistoryContract:
    """Canonical incident history contract for foundation dashboard hardening."""

    total_entries: int
    history_visible_entries: int
    archived_entries: int
    recovered_entries: int
    critical_entries: int
    warning_entries: int
    info_entries: int
    entries: tuple[FoundationIncidentHistoryEntry, ...]


def build_foundation_incident_history_contract() -> (
    FoundationIncidentHistoryContract
):
    """Build canonical incident history contract from foundation incident model."""
    model = build_foundation_incident_model()

    entries = tuple(
        FoundationIncidentHistoryEntry(
            history_entry_id=f"foundation_history_{entry.source_component}_001",
            incident_id=entry.incident_id,
            source_component=entry.source_component,
            failing_stage=entry.failing_stage,
            incident_state=entry.incident_state,
            severity=entry.severity,
            archived=entry.incident_state == "ARCHIVED",
            recovered=entry.incident_state == "RECOVERED",
            history_visible=True,
            description=(
                "Canonical incident history entry derived from foundation incident "
                f"model for scope={entry.source_component}."
            ),
        )
        for entry in model.entries
    )

    return FoundationIncidentHistoryContract(
        total_entries=len(entries),
        history_visible_entries=sum(1 for entry in entries if entry.history_visible),
        archived_entries=sum(1 for entry in entries if entry.archived),
        recovered_entries=sum(1 for entry in entries if entry.recovered),
        critical_entries=sum(1 for entry in entries if entry.severity == "critical"),
        warning_entries=sum(1 for entry in entries if entry.severity == "warning"),
        info_entries=sum(1 for entry in entries if entry.severity == "info"),
        entries=entries,
    )
