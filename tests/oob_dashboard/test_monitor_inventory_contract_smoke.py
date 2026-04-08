from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_inventory_contract import (
    MonitorInventoryEntry,
    build_monitor_inventory_contract,
)


def test_monitor_inventory_contract_builds() -> None:
    """Monitor inventory contract should build successfully."""
    contract = build_monitor_inventory_contract()

    assert contract.contract_id == "monitor_inventory_contract_001"
    assert contract.total_entries == 3
    assert contract.present_entries == 3
    assert contract.shared_surface_entries == 1
    assert contract.operator_visible_entries == 3


def test_monitor_inventory_contract_contains_expected_entries() -> None:
    """Monitor inventory contract should contain expected canonical entries."""
    contract = build_monitor_inventory_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert entry_map["display_primary_operator"].monitor_role == "primary_operator_monitor"
    assert entry_map["display_primary_operator"].active_assignments == 1
    assert entry_map["display_primary_operator"].shared_surface is False

    assert entry_map["display_secondary_diagnostics"].monitor_role == "secondary_diagnostics_monitor"
    assert entry_map["display_secondary_diagnostics"].active_assignments == 2
    assert entry_map["display_secondary_diagnostics"].shared_surface is True

    assert entry_map["display_tertiary_expansion"].monitor_role == "tertiary_expansion_monitor"
    assert entry_map["display_tertiary_expansion"].active_assignments == 1
    assert entry_map["display_tertiary_expansion"].shared_surface is False


def test_monitor_inventory_entry_rejects_zero_assignments() -> None:
    """Monitor inventory entry should reject zero assignments."""
    with pytest.raises(ValueError, match="active_assignments must be at least 1"):
        MonitorInventoryEntry(
            display_target_id="display_primary_operator",
            monitor_role="primary_operator_monitor",
            monitor_state="monitor_present",
            active_assignments=0,
            shared_surface=False,
            operator_visible=True,
            description="Invalid monitor inventory entry.",
        )
