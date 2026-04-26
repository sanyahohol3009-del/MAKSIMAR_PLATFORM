from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.display_resolver_decision_contract import (
    DisplayResolverDecisionEntry,
    build_display_resolver_decision_contract,
)


def test_display_resolver_decision_contract_builds() -> None:
    """Display resolver decision contract should build successfully."""
    contract = build_display_resolver_decision_contract()

    assert contract.contract_id == "display_resolver_decision_contract_001"
    assert contract.total_entries == 2
    assert contract.pinned_resolution_entries == 1
    assert contract.replaceable_resolution_entries == 1
    assert contract.operator_visible_entries == 2


def test_display_resolver_decision_contract_contains_expected_entries() -> None:
    """Display resolver decision contract should contain expected canonical entries."""
    contract = build_display_resolver_decision_contract()
    entry_map = {entry.resolver_decision_id: entry for entry in contract.entries}

    pinned_entry = entry_map["display_resolver_decision_001"]
    replaceable_entry = entry_map["display_resolver_decision_002"]

    assert pinned_entry.display_target_id == "display_foundation_primary"
    assert pinned_entry.resolver_decision_class == "pinned_display_resolution"
    assert pinned_entry.routed_candidate_display_target_id is None

    assert replaceable_entry.display_target_id == "display_foundation_secondary"
    assert replaceable_entry.resolver_decision_class == "replaceable_display_resolution"
    assert replaceable_entry.routed_candidate_display_target_id == "display_foundation_secondary"


def test_display_resolver_decision_entry_rejects_missing_candidate() -> None:
    """Replaceable resolver decisions must expose routed candidate display ids."""
    with pytest.raises(
        ValueError,
        match="replaceable_display_resolution entries must expose routed_candidate_display_target_id.",
    ):
        DisplayResolverDecisionEntry(
            resolver_decision_id="display_resolver_decision_invalid",
            display_target_id="display_foundation_secondary",
            resolver_decision_state="resolver_decision_ready",
            resolver_decision_class="replaceable_display_resolution",
            selected_assignment_id="display_assignment_002",
            continuity_id="display_restore_continuity_002",
            routed_candidate_display_target_id=None,
            operator_visible=True,
            description="Invalid resolver decision entry.",
        )
