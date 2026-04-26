from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.display_continuity_snapshot_contract import (
    DisplayContinuitySnapshotEntry,
    build_display_continuity_snapshot_contract,
)


def test_display_continuity_snapshot_contract_builds() -> None:
    """Display continuity snapshot contract should build successfully."""
    contract = build_display_continuity_snapshot_contract()

    assert contract.contract_id == "display_continuity_snapshot_contract_001"
    assert contract.total_entries == 3
    assert contract.shared_surface_entries == 1
    assert contract.operator_visible_entries == 3


def test_display_continuity_snapshot_contract_contains_expected_entries() -> None:
    """Display continuity snapshot contract should contain expected canonical entries."""
    contract = build_display_continuity_snapshot_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert entry_map["display_foundation_primary"].snapshot_class == "foundation_primary_snapshot"
    assert entry_map["display_foundation_primary"].shared_surface is False
    assert entry_map["display_foundation_primary"].selected_assignment_present is True

    assert entry_map["display_foundation_secondary"].snapshot_class == "foundation_secondary_snapshot"
    assert entry_map["display_foundation_secondary"].shared_surface is True
    assert entry_map["display_foundation_secondary"].selected_assignment_present is True

    assert entry_map["display_operator_interaction"].snapshot_class == "operator_interaction_snapshot"
    assert entry_map["display_operator_interaction"].shared_surface is False
    assert entry_map["display_operator_interaction"].selected_assignment_present is True


def test_display_continuity_snapshot_entry_rejects_missing_selected_assignment() -> None:
    """Continuity snapshots must expose selected assignment presence."""
    with pytest.raises(ValueError, match="selected_assignment_present must remain true"):
        DisplayContinuitySnapshotEntry(
            snapshot_id="display_continuity_snapshot_invalid",
            display_target_id="display_foundation_primary",
            snapshot_state="snapshot_ready",
            snapshot_class="foundation_primary_snapshot",
            active_assignments=1,
            selected_assignment_present=False,
            shared_surface=False,
            operator_visible=True,
            description="Invalid continuity snapshot entry.",
        )
