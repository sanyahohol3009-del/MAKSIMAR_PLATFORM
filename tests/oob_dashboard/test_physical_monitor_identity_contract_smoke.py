from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.physical_monitor_identity_contract import (
    PhysicalMonitorIdentityEntry,
    build_physical_monitor_identity_contract,
)


def test_physical_monitor_identity_contract_builds() -> None:
    """Physical monitor identity contract should build successfully."""
    contract = build_physical_monitor_identity_contract()

    assert contract.contract_id == "physical_monitor_identity_contract_001"
    assert contract.total_entries == 3
    assert contract.hotplug_detectable_entries == 3
    assert contract.operator_visible_entries == 3


def test_physical_monitor_identity_contract_contains_expected_entries() -> None:
    """Physical monitor identity contract should contain expected canonical entries."""
    contract = build_physical_monitor_identity_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert (
        entry_map["display_foundation_primary"].identity_class
        == "foundation_primary_physical_monitor"
    )
    assert (
        entry_map["display_foundation_secondary"].identity_class
        == "foundation_secondary_physical_monitor"
    )
    assert (
        entry_map["display_operator_interaction"].identity_class
        == "operator_interaction_physical_monitor"
    )

    assert (
        entry_map["display_foundation_primary"].physical_slot_label
        == "monitor_slot_foundation_primary"
    )
    assert (
        entry_map["display_foundation_secondary"].physical_slot_label
        == "monitor_slot_foundation_secondary"
    )
    assert (
        entry_map["display_operator_interaction"].physical_slot_label
        == "monitor_slot_operator_interaction"
    )


def test_physical_monitor_identity_entry_rejects_non_hotplug_detectable() -> None:
    """Physical monitor identity entry must remain hotplug-detectable."""
    with pytest.raises(
        ValueError,
        match="hotplug_detectable must remain true for canonical physical monitor identity.",
    ):
        PhysicalMonitorIdentityEntry(
            physical_monitor_id="physical_monitor_invalid",
            display_target_id="display_foundation_primary",
            monitor_inventory_id="monitor_inventory_001",
            identity_state="physical_monitor_identity_ready",
            identity_class="foundation_primary_physical_monitor",
            physical_slot_label="monitor_slot_foundation_primary",
            hotplug_detectable=False,
            multi_monitor_capable=True,
            operator_visible=True,
            description="Invalid physical monitor identity entry.",
        )
