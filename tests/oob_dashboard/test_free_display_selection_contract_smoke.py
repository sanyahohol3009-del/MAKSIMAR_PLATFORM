from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.free_display_selection_contract import (
    FreeDisplaySelectionEntry,
    build_free_display_selection_contract,
)


def test_free_display_selection_contract_builds() -> None:
    """Free-display selection contract should build successfully."""
    contract = build_free_display_selection_contract()

    assert contract.contract_id == "free_display_selection_contract_001"
    assert contract.total_entries == 1
    assert contract.no_free_display_entries == 0
    assert contract.replaceable_candidate_entries == 1
    assert contract.operator_visible_entries == 1


def test_free_display_selection_contract_contains_expected_entry() -> None:
    """Free-display selection contract should contain expected canonical entry."""
    contract = build_free_display_selection_contract()
    entry = contract.entries[0]

    assert entry.selection_id == "free_display_selection_001"
    assert entry.requested_role_hint == "operator_auxiliary_surface"
    assert entry.selection_decision == "replaceable_display_candidate_available"
    assert entry.selection_reason == "replaceable_secondary_or_tertiary_available"
    assert entry.candidate_display_target_id == "display_foundation_secondary"
    assert entry.operator_visible is True


def test_free_display_selection_entry_rejects_candidate_on_no_free_decision() -> None:
    """No-free-display decisions must not expose candidate targets."""
    with pytest.raises(ValueError, match="no_free_display_available entries must not expose candidate_display_target_id."):
        FreeDisplaySelectionEntry(
            selection_id="free_display_selection_invalid",
            requested_role_hint="operator_auxiliary_surface",
            selection_decision="no_free_display_available",
            selection_reason="no_replaceable_display_available",
            candidate_display_target_id="display_foundation_secondary",
            operator_visible=True,
            description="Invalid free-display selection entry.",
        )


def test_free_display_selection_entry_requires_reason_alignment() -> None:
    """Selection decision and selection reason must remain aligned."""
    with pytest.raises(ValueError, match="replaceable_display_candidate_available entries must use selection_reason='replaceable_secondary_or_tertiary_available'."):
        FreeDisplaySelectionEntry(
            selection_id="free_display_selection_invalid_reason",
            requested_role_hint="operator_auxiliary_surface",
            selection_decision="replaceable_display_candidate_available",
            selection_reason="no_replaceable_display_available",
            candidate_display_target_id="display_foundation_secondary",
            operator_visible=True,
            description="Invalid free-display selection reason alignment.",
        )
