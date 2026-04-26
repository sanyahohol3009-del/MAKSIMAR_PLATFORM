from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_close_or_replace_decision_contract import (
    OperatorCloseOrReplaceDecisionEntry,
    build_operator_close_or_replace_decision_contract,
)


def test_operator_close_or_replace_decision_contract_builds() -> None:
    """Operator close-or-replace decision contract should build successfully."""
    contract = build_operator_close_or_replace_decision_contract()

    assert contract.contract_id == "operator_close_or_replace_decision_contract_001"
    assert contract.total_entries == 2
    assert contract.retain_entries == 1
    assert contract.replace_entries == 1
    assert contract.operator_visible_entries == 2


def test_operator_close_or_replace_decision_contract_contains_expected_entries() -> None:
    """Operator close-or-replace decision contract should contain expected canonical entries."""
    contract = build_operator_close_or_replace_decision_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert (
        entry_map["display_foundation_primary"].decision_class
        == "retain_primary_surface_decision"
    )
    assert (
        entry_map["display_foundation_primary"].decision_action
        == "retain_current_surface"
    )
    assert (
        entry_map["display_foundation_primary"].candidate_display_target_id is None
    )

    assert (
        entry_map["display_foundation_secondary"].decision_class
        == "replace_secondary_surface_decision"
    )
    assert (
        entry_map["display_foundation_secondary"].decision_action
        == "replace_with_candidate_surface"
    )
    assert (
        entry_map["display_foundation_secondary"].candidate_display_target_id
        == "display_foundation_secondary"
    )


def test_operator_close_or_replace_decision_entry_rejects_missing_candidate_for_replace() -> None:
    """Replace decisions must expose a candidate display target id."""
    with pytest.raises(
        ValueError,
        match="replace_with_candidate_surface entries must expose candidate_display_target_id.",
    ):
        OperatorCloseOrReplaceDecisionEntry(
            decision_id="operator_close_or_replace_decision_invalid",
            display_target_id="display_foundation_secondary",
            logical_target_id="logical_display_target_002",
            decision_state="operator_decision_ready",
            decision_class="replace_secondary_surface_decision",
            decision_action="replace_with_candidate_surface",
            candidate_display_target_id=None,
            operator_visible=True,
            description="Invalid replace decision entry.",
        )
