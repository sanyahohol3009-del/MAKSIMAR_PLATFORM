from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.display_occupancy_contract import (
    build_display_occupancy_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_runtime_resolver_integration_contract import (
    resolve_fallback_display_target_id,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_target_vocabulary_contract import (
    build_display_target_vocabulary_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_inventory_contract import (
    build_monitor_inventory_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_metadata_models import (
    MonitorMetadataContract,
    MonitorMetadataEntry,
)


def _resolve_metadata_role(display_target_id: str) -> str:
    """Resolve canonical metadata role from display target id."""
    role_map = {
        "display_foundation_primary": "foundation_primary_metadata",
        "display_foundation_secondary": "foundation_secondary_metadata",
        "display_operator_interaction": "operator_interaction_metadata",
    }
    if display_target_id not in role_map:
        raise ValueError(
            f"unsupported display_target_id for metadata role: {display_target_id}"
        )
    return role_map[display_target_id]


def build_monitor_metadata_contract() -> MonitorMetadataContract:
    """Build canonical monitor metadata contract.

    This layer enriches monitor inventory with current canonical display metadata:
    role, zone, fallback target, occupancy class, and assignment count.
    It does not replace inventory, occupancy, assignment, or resolver layers.
    """
    inventory_contract = build_monitor_inventory_contract()
    display_target_contract = build_display_target_vocabulary_contract()
    occupancy_contract = build_display_occupancy_contract()

    display_target_map = {
        entry.display_target_id: entry for entry in display_target_contract.entries
    }
    occupancy_map = {
        entry.display_target_id: entry for entry in occupancy_contract.entries
    }

    entries = tuple(
        MonitorMetadataEntry(
            monitor_id=inventory_entry.monitor_id,
            display_target_id=inventory_entry.display_target_id,
            metadata_role=_resolve_metadata_role(inventory_entry.display_target_id),
            metadata_state="monitor_metadata_ready",
            display_role=display_target_map[inventory_entry.display_target_id].display_role,
            display_zone=display_target_map[inventory_entry.display_target_id].display_zone,
            fallback_display_target_id=resolve_fallback_display_target_id(
                inventory_entry.display_target_id
            ),
            occupancy_class=occupancy_map[
                inventory_entry.display_target_id
            ].occupancy_class,
            assignment_count=occupancy_map[
                inventory_entry.display_target_id
            ].total_assignments,
            supports_foundation_panels=inventory_entry.supports_foundation_panels,
            supports_operator_surfaces=inventory_entry.supports_operator_surfaces,
            multi_monitor_capable=inventory_entry.multi_monitor_capable,
            operator_visible=inventory_entry.operator_visible,
            description=(
                "Canonical monitor metadata entry for "
                f"{inventory_entry.display_target_id}."
            ),
        )
        for inventory_entry in inventory_contract.entries
    )

    return MonitorMetadataContract(
        contract_id="monitor_metadata_contract_001",
        total_entries=len(entries),
        foundation_metadata_entries=sum(
            1
            for entry in entries
            if entry.metadata_role in {
                "foundation_primary_metadata",
                "foundation_secondary_metadata",
            }
        ),
        operator_metadata_entries=sum(
            1
            for entry in entries
            if entry.metadata_role == "operator_interaction_metadata"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
