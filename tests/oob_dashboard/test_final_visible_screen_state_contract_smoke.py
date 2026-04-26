from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.final_visible_screen_state_contract import (
    FinalVisibleScreenStateContract,
    FinalVisibleScreenStateEntry,
    build_final_visible_screen_state_contract,
)


def test_final_visible_screen_state_contract_builds() -> None:
    """Final visible screen state contract should build successfully."""
    contract = build_final_visible_screen_state_contract()

    assert contract.contract_id == "final_visible_screen_state_contract_001"
    assert contract.total_entries == 4
    assert contract.ready_entries == 4
    assert contract.operator_visible_entries == 4
    assert contract.truth_bound_entries == 4


def test_final_visible_screen_state_contract_contains_expected_entries() -> None:
    """Final visible screen state contract should contain expected canonical entries."""
    contract = build_final_visible_screen_state_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert (
        entry_map["display_foundation_primary"].final_visible_screen_state_class
        == "foundation_primary_final_screen_state"
    )
    assert (
        entry_map["display_foundation_secondary"].final_visible_screen_state_class
        == "foundation_secondary_final_screen_state"
    )
    assert (
        entry_map["display_operator_interaction"].final_visible_screen_state_class
        == "interaction_final_screen_state"
    )

    assert entry_map["display_foundation_primary"].presentation_bundle_ready is True
    assert entry_map["display_foundation_primary"].rollback_readiness_ready is True


def test_final_visible_screen_state_entry_rejects_non_truth_bound() -> None:
    """Final visible screen state entry must remain truth-bound."""
    with pytest.raises(
        ValueError,
        match="truth_bound must remain true for canonical final visible screen state.",
    ):
        FinalVisibleScreenStateEntry(
            final_visible_screen_state_id="final_visible_screen_state_invalid",
            display_target_id="display_foundation_primary",
            workspace_id="workspace_foundation_monitoring",
            final_visible_screen_state="final_visible_screen_state_ready",
            final_visible_screen_state_class="foundation_primary_final_screen_state",
            presentation_bundle_ready=True,
            rollback_readiness_ready=True,
            operator_visible=True,
            truth_bound=False,
            description="Invalid final visible screen state entry.",
        )


def test_final_visible_screen_state_manual_contract_builds() -> None:
    """Final visible screen state manual contract should build successfully."""
    entries = (
        FinalVisibleScreenStateEntry(
            final_visible_screen_state_id="final_visible_screen_state_001",
            display_target_id="display_foundation_primary",
            workspace_id="workspace_foundation_monitoring",
            final_visible_screen_state="final_visible_screen_state_ready",
            final_visible_screen_state_class="foundation_primary_final_screen_state",
            presentation_bundle_ready=True,
            rollback_readiness_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical final visible screen state entry.",
        ),
    )

    contract = FinalVisibleScreenStateContract(
        contract_id="final_visible_screen_state_contract_001",
        total_entries=1,
        ready_entries=1,
        operator_visible_entries=1,
        truth_bound_entries=1,
        entries=entries,
    )

    assert contract.total_entries == 1
    assert contract.ready_entries == 1
