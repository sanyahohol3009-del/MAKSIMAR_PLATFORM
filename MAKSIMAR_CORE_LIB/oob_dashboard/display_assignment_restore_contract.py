from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_registry_contract import (
    build_display_assignment_registry_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DisplayAssignmentRestoreEntry:
    """Canonical display assignment restore entry."""

    assignment_id: str
    display_target_id: str
    panel_or_surface_id: str
    restore_decision: str
    restore_state: str
    workspace_id: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.assignment_id, "assignment_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.panel_or_surface_id, "panel_or_surface_id")
        _require_non_empty(self.restore_decision, "restore_decision")
        _require_non_empty(self.restore_state, "restore_state")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.restore_decision not in {
            "restore_direct",
            "restore_shared_surface",
        }:
            raise ValueError(
                "restore_decision must be restore_direct or restore_shared_surface."
            )

        if self.restore_state != "restore_ready":
            raise ValueError("restore_state must remain restore_ready.")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical display assignment restore entries."
            )


@dataclass(frozen=True, slots=True)
class DisplayAssignmentRestoreContract:
    """Canonical display assignment restore contract."""

    contract_id: str
    total_entries: int
    direct_restore_entries: int
    shared_surface_restore_entries: int
    operator_visible_entries: int
    entries: tuple[DisplayAssignmentRestoreEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.direct_restore_entries != sum(
            1 for entry in self.entries if entry.restore_decision == "restore_direct"
        ):
            raise ValueError(
                "direct_restore_entries must match restore_direct count."
            )

        if self.shared_surface_restore_entries != sum(
            1
            for entry in self.entries
            if entry.restore_decision == "restore_shared_surface"
        ):
            raise ValueError(
                "shared_surface_restore_entries must match restore_shared_surface count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_display_assignment_restore_contract() -> DisplayAssignmentRestoreContract:
    """Build canonical display assignment restore contract."""
    registry = build_display_assignment_registry_contract()
    registry_by_id = {entry.assignment_id: entry for entry in registry.entries}

    entries = (
        DisplayAssignmentRestoreEntry(
            assignment_id="display_assignment_001",
            display_target_id=registry_by_id["display_assignment_001"].display_target_id,
            panel_or_surface_id="workspace_operator_main_surface",
            restore_decision="restore_direct",
            restore_state="restore_ready",
            workspace_id=registry_by_id["display_assignment_001"].workspace_id,
            operator_visible=True,
            description="Canonical direct restore entry for main operator surface.",
        ),
        DisplayAssignmentRestoreEntry(
            assignment_id="display_assignment_002",
            display_target_id=registry_by_id["display_assignment_002"].display_target_id,
            panel_or_surface_id="panel_system_status_001",
            restore_decision="restore_shared_surface",
            restore_state="restore_ready",
            workspace_id=registry_by_id["display_assignment_002"].workspace_id,
            operator_visible=True,
            description="Canonical shared-surface restore entry for system-status panel.",
        ),
        DisplayAssignmentRestoreEntry(
            assignment_id="display_assignment_003",
            display_target_id=registry_by_id["display_assignment_003"].display_target_id,
            panel_or_surface_id="panel_incidents_001",
            restore_decision="restore_shared_surface",
            restore_state="restore_ready",
            workspace_id=registry_by_id["display_assignment_003"].workspace_id,
            operator_visible=True,
            description="Canonical direct restore entry for incidents panel.",
        ),
        DisplayAssignmentRestoreEntry(
            assignment_id="display_assignment_004",
            display_target_id=registry_by_id["display_assignment_004"].display_target_id,
            panel_or_surface_id="panel_logs_001",
            restore_decision="restore_direct",
            restore_state="restore_ready",
            workspace_id=registry_by_id["display_assignment_004"].workspace_id,
            operator_visible=True,
            description="Canonical direct restore entry for logs panel.",
        ),
    )

    return DisplayAssignmentRestoreContract(
        contract_id="display_assignment_restore_contract_001",
        total_entries=len(entries),
        direct_restore_entries=sum(
            1 for entry in entries if entry.restore_decision == "restore_direct"
        ),
        shared_surface_restore_entries=sum(
            1
            for entry in entries
            if entry.restore_decision == "restore_shared_surface"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
