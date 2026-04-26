from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_inventory_contract import (
    build_monitor_inventory_contract,
)


PhysicalMonitorIdentityState = Literal[
    "physical_monitor_identity_ready",
]

PhysicalMonitorIdentityClass = Literal[
    "foundation_primary_physical_monitor",
    "foundation_secondary_physical_monitor",
    "operator_interaction_physical_monitor",
]

ALL_PHYSICAL_MONITOR_IDENTITY_STATES: tuple[PhysicalMonitorIdentityState, ...] = (
    "physical_monitor_identity_ready",
)

ALL_PHYSICAL_MONITOR_IDENTITY_CLASSES: tuple[PhysicalMonitorIdentityClass, ...] = (
    "foundation_primary_physical_monitor",
    "foundation_secondary_physical_monitor",
    "operator_interaction_physical_monitor",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class PhysicalMonitorIdentityEntry:
    """Canonical physical monitor identity entry."""

    physical_monitor_id: str
    display_target_id: str
    monitor_inventory_id: str
    identity_state: PhysicalMonitorIdentityState
    identity_class: PhysicalMonitorIdentityClass
    physical_slot_label: str
    hotplug_detectable: bool
    multi_monitor_capable: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.physical_monitor_id, "physical_monitor_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.monitor_inventory_id, "monitor_inventory_id")
        _require_non_empty(self.physical_slot_label, "physical_slot_label")
        _require_non_empty(self.description, "description")

        if self.identity_state not in ALL_PHYSICAL_MONITOR_IDENTITY_STATES:
            raise ValueError(
                "identity_state must be one of "
                f"{ALL_PHYSICAL_MONITOR_IDENTITY_STATES}, got {self.identity_state!r}."
            )

        if self.identity_class not in ALL_PHYSICAL_MONITOR_IDENTITY_CLASSES:
            raise ValueError(
                "identity_class must be one of "
                f"{ALL_PHYSICAL_MONITOR_IDENTITY_CLASSES}, got {self.identity_class!r}."
            )

        if not self.hotplug_detectable:
            raise ValueError(
                "hotplug_detectable must remain true for canonical physical monitor identity."
            )

        if not self.multi_monitor_capable:
            raise ValueError(
                "multi_monitor_capable must remain true for canonical physical monitor identity."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical physical monitor identity."
            )


@dataclass(frozen=True, slots=True)
class PhysicalMonitorIdentityContract:
    """Canonical physical monitor identity contract."""

    contract_id: str
    total_entries: int
    hotplug_detectable_entries: int
    operator_visible_entries: int
    entries: tuple[PhysicalMonitorIdentityEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.hotplug_detectable_entries != sum(
            1 for entry in self.entries if entry.hotplug_detectable
        ):
            raise ValueError(
                "hotplug_detectable_entries must match hotplug_detectable count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_physical_monitor_identity_contract() -> PhysicalMonitorIdentityContract:
    """Build canonical physical monitor identity contract."""
    inventory_contract = build_monitor_inventory_contract()
    inventory_by_display = {
        entry.display_target_id: entry for entry in inventory_contract.entries
    }

    class_map: dict[str, PhysicalMonitorIdentityClass] = {
        "display_foundation_primary": "foundation_primary_physical_monitor",
        "display_foundation_secondary": "foundation_secondary_physical_monitor",
        "display_operator_interaction": "operator_interaction_physical_monitor",
    }

    slot_map = {
        "display_foundation_primary": "monitor_slot_foundation_primary",
        "display_foundation_secondary": "monitor_slot_foundation_secondary",
        "display_operator_interaction": "monitor_slot_operator_interaction",
    }

    ordered_display_targets = (
        "display_foundation_primary",
        "display_foundation_secondary",
        "display_operator_interaction",
    )

    entries = tuple(
        PhysicalMonitorIdentityEntry(
            physical_monitor_id=f"physical_monitor_{index:03d}",
            display_target_id=display_target_id,
            monitor_inventory_id=inventory_by_display[display_target_id].monitor_id,
            identity_state="physical_monitor_identity_ready",
            identity_class=class_map[display_target_id],
            physical_slot_label=slot_map[display_target_id],
            hotplug_detectable=True,
            multi_monitor_capable=inventory_by_display[
                display_target_id
            ].multi_monitor_capable,
            operator_visible=inventory_by_display[display_target_id].operator_visible,
            description=(
                f"Canonical physical monitor identity entry for {display_target_id}."
            ),
        )
        for index, display_target_id in enumerate(ordered_display_targets, start=1)
    )

    return PhysicalMonitorIdentityContract(
        contract_id="physical_monitor_identity_contract_001",
        total_entries=len(entries),
        hotplug_detectable_entries=sum(
            1 for entry in entries if entry.hotplug_detectable
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
