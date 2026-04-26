from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


MonitorInventoryRole = Literal[
    "foundation_primary_monitor",
    "foundation_secondary_monitor",
    "operator_interaction_monitor",
]

MonitorInventoryState = Literal[
    "monitor_present",
]

ALL_MONITOR_INVENTORY_ROLES: tuple[MonitorInventoryRole, ...] = (
    "foundation_primary_monitor",
    "foundation_secondary_monitor",
    "operator_interaction_monitor",
)

ALL_MONITOR_INVENTORY_STATES: tuple[MonitorInventoryState, ...] = (
    "monitor_present",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class MonitorInventoryEntry:
    """Canonical monitor inventory entry."""

    monitor_id: str
    display_target_id: str
    monitor_role: MonitorInventoryRole
    inventory_state: MonitorInventoryState
    supports_foundation_panels: bool
    supports_operator_surfaces: bool
    multi_monitor_capable: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.monitor_id, "monitor_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.monitor_role not in ALL_MONITOR_INVENTORY_ROLES:
            raise ValueError(
                "monitor_role must be one of "
                f"{ALL_MONITOR_INVENTORY_ROLES}, got {self.monitor_role!r}."
            )

        if self.inventory_state not in ALL_MONITOR_INVENTORY_STATES:
            raise ValueError(
                "inventory_state must be one of "
                f"{ALL_MONITOR_INVENTORY_STATES}, got {self.inventory_state!r}."
            )

        if not self.multi_monitor_capable:
            raise ValueError(
                "multi_monitor_capable must remain true for canonical monitor inventory."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical monitor inventory."
            )

        if (
            self.monitor_role == "operator_interaction_monitor"
            and not self.supports_operator_surfaces
        ):
            raise ValueError(
                "operator_interaction_monitor must support operator surfaces."
            )

        if (
            self.monitor_role != "operator_interaction_monitor"
            and not self.supports_foundation_panels
        ):
            raise ValueError(
                "foundation monitor roles must support foundation panels."
            )


@dataclass(frozen=True, slots=True)
class MonitorInventoryContract:
    """Canonical monitor inventory contract."""

    contract_id: str
    total_entries: int
    foundation_monitor_entries: int
    operator_monitor_entries: int
    operator_visible_entries: int
    entries: tuple[MonitorInventoryEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.foundation_monitor_entries != sum(
            1
            for entry in self.entries
            if entry.monitor_role in {
                "foundation_primary_monitor",
                "foundation_secondary_monitor",
            }
        ):
            raise ValueError(
                "foundation_monitor_entries must match foundation monitor count."
            )

        if self.operator_monitor_entries != sum(
            1
            for entry in self.entries
            if entry.monitor_role == "operator_interaction_monitor"
        ):
            raise ValueError(
                "operator_monitor_entries must match operator monitor count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
