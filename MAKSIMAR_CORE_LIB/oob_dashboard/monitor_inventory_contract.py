from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_registry_contract import (
    build_display_assignment_registry_contract,
)


MonitorRole = Literal[
    "primary_operator_monitor",
    "secondary_diagnostics_monitor",
    "tertiary_expansion_monitor",
]

MonitorState = Literal[
    "monitor_present",
]

ALL_MONITOR_ROLES: tuple[MonitorRole, ...] = (
    "primary_operator_monitor",
    "secondary_diagnostics_monitor",
    "tertiary_expansion_monitor",
)

ALL_MONITOR_STATES: tuple[MonitorState, ...] = (
    "monitor_present",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class MonitorInventoryEntry:
    """Canonical monitor inventory entry."""

    display_target_id: str
    monitor_role: MonitorRole
    monitor_state: MonitorState
    active_assignments: int
    shared_surface: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.monitor_role not in ALL_MONITOR_ROLES:
            raise ValueError(
                f"monitor_role must be one of {ALL_MONITOR_ROLES}, got {self.monitor_role!r}."
            )

        if self.monitor_state not in ALL_MONITOR_STATES:
            raise ValueError(
                f"monitor_state must be one of {ALL_MONITOR_STATES}, got {self.monitor_state!r}."
            )

        if not self.operator_visible:
            raise ValueError("operator_visible must remain true for canonical monitor inventory entries.")

        if self.active_assignments < 1:
            raise ValueError("active_assignments must be at least 1 for canonical monitor inventory entries.")


@dataclass(frozen=True, slots=True)
class MonitorInventoryContract:
    """Canonical monitor inventory contract."""

    contract_id: str
    total_entries: int
    present_entries: int
    shared_surface_entries: int
    operator_visible_entries: int
    entries: tuple[MonitorInventoryEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match the number of entries in the contract.")

        if self.present_entries != sum(
            1 for entry in self.entries if entry.monitor_state == "monitor_present"
        ):
            raise ValueError("present_entries must match monitor_present count.")

        if self.shared_surface_entries != sum(
            1 for entry in self.entries if entry.shared_surface
        ):
            raise ValueError("shared_surface_entries must match shared_surface count.")

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")


def build_monitor_inventory_contract() -> MonitorInventoryContract:
    """Build canonical monitor inventory contract."""
    registry_contract = build_display_assignment_registry_contract()

    role_map = {
        "display_primary_operator": "primary_operator_monitor",
        "display_secondary_diagnostics": "secondary_diagnostics_monitor",
        "display_tertiary_expansion": "tertiary_expansion_monitor",
    }

    assignment_counts: dict[str, int] = {}
    for entry in registry_contract.entries:
        assignment_counts[entry.display_target_id] = (
            assignment_counts.get(entry.display_target_id, 0) + 1
        )

    entries = tuple(
        MonitorInventoryEntry(
            display_target_id=display_target_id,
            monitor_role=role_map[display_target_id],
            monitor_state="monitor_present",
            active_assignments=active_assignments,
            shared_surface=active_assignments > 1,
            operator_visible=True,
            description=f"Canonical monitor inventory entry for {display_target_id}.",
        )
        for display_target_id, active_assignments in assignment_counts.items()
    )

    return MonitorInventoryContract(
        contract_id="monitor_inventory_contract_001",
        total_entries=len(entries),
        present_entries=sum(
            1 for entry in entries if entry.monitor_state == "monitor_present"
        ),
        shared_surface_entries=sum(1 for entry in entries if entry.shared_surface),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
