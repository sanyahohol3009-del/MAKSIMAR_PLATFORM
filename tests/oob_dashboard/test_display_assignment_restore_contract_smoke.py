from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_restore_contract import (
    DisplayAssignmentRestoreEntry,
    build_display_assignment_restore_contract,
)


def test_display_assignment_restore_contract_builds() -> None:
    """Display assignment restore contract should build successfully."""
    contract = build_display_assignment_restore_contract()

    assert contract.contract_id == "display_assignment_restore_contract_001"
    assert contract.total_entries == 4
    assert contract.direct_restore_entries == 2
    assert contract.shared_surface_restore_entries == 2
    assert contract.operator_visible_entries == 4


def test_display_assignment_restore_contract_contains_expected_entries() -> None:
    """Display assignment restore contract should contain expected canonical entries."""
    contract = build_display_assignment_restore_contract()
    entry_map = {entry.assignment_id: entry for entry in contract.entries}

    assert entry_map["display_assignment_001"].restore_decision == "restore_direct"
    assert entry_map["display_assignment_001"].display_target_id == "display_foundation_primary"

    assert entry_map["display_assignment_002"].restore_decision == "restore_shared_surface"
    assert entry_map["display_assignment_003"].restore_decision == "restore_shared_surface"
    assert entry_map["display_assignment_004"].restore_decision == "restore_direct"


def test_display_assignment_restore_entry_rejects_blank_assignment_id() -> None:
    """Display assignment restore entry should reject blank ids."""
    with pytest.raises(ValueError, match="assignment_id must be a non-empty string."):
        DisplayAssignmentRestoreEntry(
            assignment_id="",
            display_target_id="display_foundation_primary",
            panel_or_surface_id="main_operator_interaction_surface_001",
            restore_decision="restore_direct",
            restore_state="restore_ready",
            workspace_id="workspace_operator_main",
            operator_visible=True,
            description="Invalid restore entry.",
        )
