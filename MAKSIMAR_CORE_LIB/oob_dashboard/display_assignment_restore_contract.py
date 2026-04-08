from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_registry_contract import (
    build_display_assignment_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_inventory_contract import (
    build_monitor_inventory_contract,
)


RestoreDecision = Literal[
    "restore_direct",
    "restore_shared_surface",
]

RestoreState = Literal[
    "restore_ready",
]

ALL_RESTORE_DECISIONS: tuple[RestoreDecision, ...] = (
    "restore_direct",
    "restore_shared_surface",
)

ALL_RESTORE_STATES: tuple[RestoreState, ...] = (
    "restore_ready",
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
    restore_decision: RestoreDecision
    restore_state: RestoreState
    workspace_id: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.assignment_id, "assignment_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.panel_or_surface_id, "panel_or_surface_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.restore_decision not in ALL_RESTORE_DECISIONS:
            raise ValueError(
                f"restore_decision must be one of {ALL_RESTORE_DECISIONS}, got {self.restore_decision!r}."
            )

        if self.restore_state not in ALL_RESTORE_STATES:
            raise ValueError(
                f"restore_state must be one of {ALL_RESTORE_STATES}, got {self.restore_state!r}."
            )

        if not self.operator_visible:
            raise ValueError("operator_visible must remain true for canonical restore entries.")


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
            raise ValueError("total_entries must match the number of entries in the contract.")

        if self.direct_restore_entries != sum(
            1 for entry in self.entries if entry.restore_decision == "restore_direct"
        ):
            raise ValueError("direct_restore_entries must match restore_direct count.")

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
            raise ValueError("operator_visible_entries must match operator_visible count.")


def build_display_assignment_restore_contract() -> DisplayAssignmentRestoreContract:
    """Build canonical display assignment restore contract."""
    registry_contract = build_display_assignment_registry_contract()
    monitor_inventory = build_monitor_inventory_contract()

    shared_surface_by_display = {
        entry.display_target_id: entry.shared_surface for entry in monitor_inventory.entries
    }

    entries = tuple(
        DisplayAssignmentRestoreEntry(
            assignment_id=entry.assignment_id,
            display_target_id=entry.display_target_id,
            panel_or_surface_id=entry.panel_or_surface_id,
            restore_decision=(
                "restore_shared_surface"
                if shared_surface_by_display[entry.display_target_id]
                else "restore_direct"
            ),
            restore_state="restore_ready",
            workspace_id=entry.workspace_id,
            operator_visible=True,
            description=f"Canonical restore entry for {entry.assignment_id}.",
        )
        for entry in registry_contract.entries
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
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
