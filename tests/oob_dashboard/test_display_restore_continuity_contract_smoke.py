from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.display_restore_continuity_contract import (
    DisplayRestoreContinuityEntry,
    build_display_restore_continuity_contract,
)


def test_display_restore_continuity_contract_builds() -> None:
    """Display restore continuity contract should build successfully."""
    contract = build_display_restore_continuity_contract()

    assert contract.contract_id == "display_restore_continuity_contract_001"
    assert contract.total_entries == 4
    assert contract.direct_restore_entries == 2
    assert contract.shared_surface_restore_entries == 2
    assert contract.operator_visible_entries == 4


def test_display_restore_continuity_contract_contains_expected_entries() -> None:
    """Display restore continuity contract should contain expected canonical entries."""
    contract = build_display_restore_continuity_contract()
    entry_map = {entry.assignment_id: entry for entry in contract.entries}

    assert entry_map["display_assignment_001"].restore_continuity_class == "direct_restore_continuity"
    assert entry_map["display_assignment_002"].restore_continuity_class == "shared_surface_restore_continuity"
    assert entry_map["display_assignment_003"].restore_continuity_class == "shared_surface_restore_continuity"
    assert entry_map["display_assignment_004"].restore_continuity_class == "direct_restore_continuity"


def test_display_restore_continuity_entry_rejects_blank_id() -> None:
    """Display restore continuity entry should reject blank ids."""
    with pytest.raises(ValueError, match="continuity_id must be a non-empty string."):
        DisplayRestoreContinuityEntry(
            continuity_id="",
            assignment_id="display_assignment_001",
            display_target_id="display_primary_operator",
            restore_continuity_state="restore_continuity_preserved",
            restore_continuity_class="direct_restore_continuity",
            workspace_id="workspace_operator_main",
            operator_visible=True,
            description="Invalid restore continuity entry.",
        )
