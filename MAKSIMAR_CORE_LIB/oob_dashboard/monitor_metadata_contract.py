from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.display_topology.display_topology_contract import (
    build_display_topology_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_inventory_contract import (
    build_monitor_inventory_contract,
)


MonitorMetadataRole = Literal[
    "primary_operator_monitor",
    "diagnostics_monitor",
    "expansion_surface",
]

MonitorMetadataType = Literal[
    "physical_monitor",
    "logical_surface",
]

MonitorMetadataVisibility = Literal[
    "private",
    "shared",
]

ALL_MONITOR_METADATA_ROLES: tuple[MonitorMetadataRole, ...] = (
    "primary_operator_monitor",
    "diagnostics_monitor",
    "expansion_surface",
)

ALL_MONITOR_METADATA_TYPES: tuple[MonitorMetadataType, ...] = (
    "physical_monitor",
    "logical_surface",
)

ALL_MONITOR_METADATA_VISIBILITY: tuple[MonitorMetadataVisibility, ...] = (
    "private",
    "shared",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class MonitorMetadataEntry:
    """Canonical monitor metadata entry bridging topology truth and inventory."""

    monitor_metadata_id: str
    display_id: str
    display_target_id: str
    monitor_role: MonitorMetadataRole
    monitor_type: MonitorMetadataType
    visibility_mode: MonitorMetadataVisibility
    topology_bound: bool
    inventory_bound: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical monitor metadata entry."""
        _require_non_empty(self.monitor_metadata_id, "monitor_metadata_id")
        _require_non_empty(self.display_id, "display_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.monitor_role not in ALL_MONITOR_METADATA_ROLES:
            raise ValueError(
                "monitor_role must be one of "
                f"{ALL_MONITOR_METADATA_ROLES}, got {self.monitor_role!r}."
            )

        if self.monitor_type not in ALL_MONITOR_METADATA_TYPES:
            raise ValueError(
                "monitor_type must be one of "
                f"{ALL_MONITOR_METADATA_TYPES}, got {self.monitor_type!r}."
            )

        if self.visibility_mode not in ALL_MONITOR_METADATA_VISIBILITY:
            raise ValueError(
                "visibility_mode must be one of "
                f"{ALL_MONITOR_METADATA_VISIBILITY}, "
                f"got {self.visibility_mode!r}."
            )

        if not self.topology_bound:
            raise ValueError(
                "topology_bound must remain true for canonical monitor metadata entries."
            )

        if not self.inventory_bound:
            raise ValueError(
                "inventory_bound must remain true for canonical monitor metadata entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical monitor metadata entries."
            )


@dataclass(frozen=True, slots=True)
class MonitorMetadataContract:
    """Canonical monitor metadata contract."""

    contract_id: str
    total_entries: int
    physical_monitor_entries: int
    logical_surface_entries: int
    topology_bound_entries: int
    inventory_bound_entries: int
    entries: tuple[MonitorMetadataEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical monitor metadata contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.physical_monitor_entries != sum(
            1 for entry in self.entries if entry.monitor_type == "physical_monitor"
        ):
            raise ValueError(
                "physical_monitor_entries must match physical_monitor count."
            )

        if self.logical_surface_entries != sum(
            1 for entry in self.entries if entry.monitor_type == "logical_surface"
        ):
            raise ValueError(
                "logical_surface_entries must match logical_surface count."
            )

        if self.topology_bound_entries != sum(
            1 for entry in self.entries if entry.topology_bound
        ):
            raise ValueError(
                "topology_bound_entries must match topology_bound count."
            )

        if self.inventory_bound_entries != sum(
            1 for entry in self.entries if entry.inventory_bound
        ):
            raise ValueError(
                "inventory_bound_entries must match inventory_bound count."
            )


def build_monitor_metadata_contract() -> MonitorMetadataContract:
    """Build canonical monitor metadata contract."""
    display_topology_contract = build_display_topology_contract()
    monitor_inventory_contract = build_monitor_inventory_contract()

    topology_by_role = {
        entry.display_role: entry for entry in display_topology_contract.entries
    }
    inventory_by_display_target_id = {
        entry.display_target_id: entry for entry in monitor_inventory_contract.entries
    }

    primary_topology_entry = topology_by_role["primary_dashboard_display"]
    diagnostics_topology_entry = topology_by_role["engineering_display"]
    expansion_topology_entry = topology_by_role["mobile_display_proxy"]

    entries = (
        MonitorMetadataEntry(
            monitor_metadata_id="monitor_metadata_001",
            display_id=primary_topology_entry.display_id,
            display_target_id="display_primary_operator",
            monitor_role="primary_operator_monitor",
            monitor_type="physical_monitor",
            visibility_mode="shared",
            topology_bound=True,
            inventory_bound=("display_primary_operator" in inventory_by_display_target_id),
            operator_visible=True,
            description=(
                "Canonical monitor metadata entry for the primary operator monitor."
            ),
        ),
        MonitorMetadataEntry(
            monitor_metadata_id="monitor_metadata_002",
            display_id=diagnostics_topology_entry.display_id,
            display_target_id="display_secondary_diagnostics",
            monitor_role="diagnostics_monitor",
            monitor_type="physical_monitor",
            visibility_mode="shared",
            topology_bound=True,
            inventory_bound=(
                "display_secondary_diagnostics" in inventory_by_display_target_id
            ),
            operator_visible=True,
            description=(
                "Canonical monitor metadata entry for the diagnostics monitor."
            ),
        ),
        MonitorMetadataEntry(
            monitor_metadata_id="monitor_metadata_003",
            display_id=expansion_topology_entry.display_id,
            display_target_id="display_tertiary_expansion",
            monitor_role="expansion_surface",
            monitor_type="logical_surface",
            visibility_mode="private",
            topology_bound=True,
            inventory_bound=("display_tertiary_expansion" in inventory_by_display_target_id),
            operator_visible=True,
            description=(
                "Canonical monitor metadata entry for the tertiary expansion surface."
            ),
        ),
    )

    return MonitorMetadataContract(
        contract_id="monitor_metadata_contract_001",
        total_entries=len(entries),
        physical_monitor_entries=sum(
            1 for entry in entries if entry.monitor_type == "physical_monitor"
        ),
        logical_surface_entries=sum(
            1 for entry in entries if entry.monitor_type == "logical_surface"
        ),
        topology_bound_entries=sum(1 for entry in entries if entry.topology_bound),
        inventory_bound_entries=sum(1 for entry in entries if entry.inventory_bound),
        entries=entries,
    )
