from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.display_occupancy_contract import (
    DisplayOccupancyEntry,
    build_display_occupancy_contract,
)


def test_display_occupancy_contract_builds() -> None:
    """Display occupancy contract should build successfully."""
    contract = build_display_occupancy_contract()

    assert contract.contract_id == "display_occupancy_contract_001"
    assert contract.total_entries == 3
    assert contract.pinned_entries == 1
    assert contract.replaceable_entries == 2
    assert contract.operator_visible_entries == 3


def test_display_occupancy_contract_contains_expected_entries() -> None:
    """Display occupancy contract should contain expected canonical entries."""
    contract = build_display_occupancy_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    primary_entry = entry_map["display_foundation_primary"]
    secondary_entry = entry_map["display_foundation_secondary"]
    operator_entry = entry_map["display_operator_interaction"]

    assert primary_entry.occupancy_state == "occupied_pinned"
    assert primary_entry.total_assignments == 1
    assert primary_entry.pinned_assignments == 1
    assert primary_entry.replaceable_assignments == 0
    assert primary_entry.occupancy_class == "foundation_primary_display"

    assert secondary_entry.occupancy_state == "occupied_replaceable"
    assert secondary_entry.total_assignments == 2
    assert secondary_entry.replaceable_assignments == 2
    assert secondary_entry.pinned_assignments == 0
    assert secondary_entry.occupancy_class == "foundation_secondary_display"

    assert operator_entry.occupancy_state == "occupied_replaceable"
    assert operator_entry.total_assignments == 1
    assert operator_entry.replaceable_assignments == 1
    assert operator_entry.pinned_assignments == 0
    assert operator_entry.occupancy_class == "operator_interaction_display"


def test_display_occupancy_entry_rejects_bad_total() -> None:
    """Display occupancy entry should reject inconsistent totals."""
    with pytest.raises(ValueError, match="total_assignments must equal"):
        DisplayOccupancyEntry(
            display_target_id="display_foundation_primary",
            occupancy_state="occupied_pinned",
            occupancy_class="foundation_primary_display",
            total_assignments=2,
            replaceable_assignments=0,
            pinned_assignments=1,
            operator_visible=True,
            description="Invalid display occupancy entry.",
        )
