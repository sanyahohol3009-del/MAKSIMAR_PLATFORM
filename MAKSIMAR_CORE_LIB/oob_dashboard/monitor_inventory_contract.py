from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_inventory_models import (
    MonitorInventoryContract,
    MonitorInventoryEntry,
)


def build_monitor_inventory_contract() -> MonitorInventoryContract:
    """Build canonical monitor inventory contract.

    This layer is inventory-only.
    It does not replace occupancy, assignment, or restore semantics.
    It formalizes the currently supported display targets as inventory-visible
    monitor surfaces for multi-monitor operation.
    """
    entries = (
        MonitorInventoryEntry(
            monitor_id="monitor_inventory_001",
            display_target_id="display_foundation_primary",
            monitor_role="foundation_primary_monitor",
            inventory_state="monitor_present",
            supports_foundation_panels=True,
            supports_operator_surfaces=False,
            multi_monitor_capable=True,
            operator_visible=True,
            description=(
                "Canonical foundation primary monitor inventory entry for "
                "the primary foundation display target."
            ),
        ),
        MonitorInventoryEntry(
            monitor_id="monitor_inventory_002",
            display_target_id="display_foundation_secondary",
            monitor_role="foundation_secondary_monitor",
            inventory_state="monitor_present",
            supports_foundation_panels=True,
            supports_operator_surfaces=False,
            multi_monitor_capable=True,
            operator_visible=True,
            description=(
                "Canonical foundation secondary monitor inventory entry for "
                "the observability/secondary display target."
            ),
        ),
        MonitorInventoryEntry(
            monitor_id="monitor_inventory_003",
            display_target_id="display_operator_interaction",
            monitor_role="operator_interaction_monitor",
            inventory_state="monitor_present",
            supports_foundation_panels=False,
            supports_operator_surfaces=True,
            multi_monitor_capable=True,
            operator_visible=True,
            description=(
                "Canonical operator interaction monitor inventory entry for "
                "the operator interaction display target."
            ),
        ),
    )

    return MonitorInventoryContract(
        contract_id="monitor_inventory_contract_001",
        total_entries=len(entries),
        foundation_monitor_entries=sum(
            1
            for entry in entries
            if entry.monitor_role in {
                "foundation_primary_monitor",
                "foundation_secondary_monitor",
            }
        ),
        operator_monitor_entries=sum(
            1
            for entry in entries
            if entry.monitor_role == "operator_interaction_monitor"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
