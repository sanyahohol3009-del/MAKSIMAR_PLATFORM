from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.display_conflict_resolution_contract import (
    DisplayConflictResolutionEntry,
    build_display_conflict_resolution_contract,
)


def test_display_conflict_resolution_contract_builds() -> None:
    """Display conflict-resolution contract should build successfully."""
    contract = build_display_conflict_resolution_contract()

    assert contract.contract_id == "display_conflict_resolution_contract_001"
    assert contract.total_entries == 2
    assert contract.pinned_conflict_entries == 1
    assert contract.replaceable_conflict_entries == 1
    assert contract.operator_visible_entries == 2


def test_display_conflict_resolution_contract_contains_expected_entries() -> None:
    """Display conflict-resolution contract should contain expected canonical entries."""
    contract = build_display_conflict_resolution_contract()
    entry_map = {entry.conflict_id: entry for entry in contract.entries}

    primary_entry = entry_map["display_conflict_001"]
    secondary_entry = entry_map["display_conflict_002"]

    assert primary_entry.display_target_id == "display_primary_operator"
    assert primary_entry.conflict_decision == "retain_pinned_surface"
    assert primary_entry.conflict_class == "pinned_primary_conflict"
    assert primary_entry.candidate_display_target_id is None

    assert secondary_entry.display_target_id == "display_secondary_diagnostics"
    assert secondary_entry.conflict_decision == "replace_replaceable_surface"
    assert secondary_entry.conflict_class == "replaceable_secondary_conflict"
    assert secondary_entry.candidate_display_target_id == "display_secondary_diagnostics"


def test_display_conflict_resolution_entry_rejects_missing_candidate_for_replaceable_conflict() -> None:
    """Replaceable conflict entries must expose candidate display ids."""
    with pytest.raises(ValueError, match="replace_replaceable_surface entries must expose candidate_display_target_id."):
        DisplayConflictResolutionEntry(
            conflict_id="display_conflict_invalid",
            display_target_id="display_secondary_diagnostics",
            conflict_decision="replace_replaceable_surface",
            conflict_class="replaceable_secondary_conflict",
            incumbent_assignment_id="display_assignment_002",
            candidate_display_target_id=None,
            operator_visible=True,
            description="Invalid replaceable conflict entry.",
        )
