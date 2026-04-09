from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_metadata_contract import (
    MonitorMetadataEntry,
    build_monitor_metadata_contract,
)


def test_monitor_metadata_contract_builds() -> None:
    contract = build_monitor_metadata_contract()

    assert contract.contract_id == "monitor_metadata_contract_001"
    assert contract.total_entries == 3
    assert contract.physical_monitor_entries == 2
    assert contract.logical_surface_entries == 1
    assert contract.topology_bound_entries == 3
    assert contract.inventory_bound_entries == 3


def test_monitor_metadata_contract_contains_expected_primary_entry() -> None:
    contract = build_monitor_metadata_contract()
    entry = contract.entries[0]

    assert entry.monitor_metadata_id == "monitor_metadata_001"
    assert entry.display_id == "display_primary_dashboard_001"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.monitor_role == "primary_operator_monitor"
    assert entry.monitor_type == "physical_monitor"
    assert entry.visibility_mode == "shared"
    assert entry.topology_bound is True
    assert entry.inventory_bound is True
    assert entry.operator_visible is True


def test_monitor_metadata_entry_rejects_invalid_role() -> None:
    with pytest.raises(ValueError, match="monitor_role must be one of"):
        MonitorMetadataEntry(
            monitor_metadata_id="invalid_monitor_metadata",
            display_id="display_primary_dashboard_001",
            display_target_id="display_primary_operator",
            monitor_role="invalid_role",  # type: ignore[arg-type]
            monitor_type="physical_monitor",
            visibility_mode="shared",
            topology_bound=True,
            inventory_bound=True,
            operator_visible=True,
            description="Invalid monitor metadata entry.",
        )


def test_monitor_metadata_entry_rejects_non_topology_bound() -> None:
    with pytest.raises(ValueError, match="topology_bound must remain true"):
        MonitorMetadataEntry(
            monitor_metadata_id="invalid_monitor_metadata",
            display_id="display_primary_dashboard_001",
            display_target_id="display_primary_operator",
            monitor_role="primary_operator_monitor",
            monitor_type="physical_monitor",
            visibility_mode="shared",
            topology_bound=False,
            inventory_bound=True,
            operator_visible=True,
            description="Invalid monitor metadata entry.",
        )


def test_monitor_metadata_entry_rejects_non_inventory_bound() -> None:
    with pytest.raises(ValueError, match="inventory_bound must remain true"):
        MonitorMetadataEntry(
            monitor_metadata_id="invalid_monitor_metadata",
            display_id="display_primary_dashboard_001",
            display_target_id="display_primary_operator",
            monitor_role="primary_operator_monitor",
            monitor_type="physical_monitor",
            visibility_mode="shared",
            topology_bound=True,
            inventory_bound=False,
            operator_visible=True,
            description="Invalid monitor metadata entry.",
        )
