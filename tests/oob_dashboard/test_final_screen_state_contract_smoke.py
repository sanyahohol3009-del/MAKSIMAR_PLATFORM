from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.final_screen_state_contract import (
    build_final_screen_state_contract,
)


def test_final_screen_state_contract_builds() -> None:
    """Final screen state contract should build successfully."""
    contract = build_final_screen_state_contract()

    assert contract.contract_id == "final_screen_state_contract_001"
    assert contract.total_entries == 4
    assert contract.foundation_final_entries == 3
    assert contract.interaction_final_entries == 1
    assert contract.operator_visible_entries == 4
    assert contract.truth_bound_entries == 4


def test_final_screen_state_contract_contains_expected_entries() -> None:
    """Final screen state contract should contain expected canonical entries."""
    contract = build_final_screen_state_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert (
        entry_map["display_foundation_primary"].final_screen_state_class
        == "foundation_final_screen_state"
    )
    assert (
        entry_map["display_foundation_primary"].final_screen_state_mode
        == "assembled_foundation_final_screen_state"
    )

    assert (
        entry_map["display_operator_interaction"].final_screen_state_class
        == "interaction_final_screen_state"
    )
    assert (
        entry_map["display_operator_interaction"].final_screen_state_mode
        == "assembled_interaction_final_screen_state"
    )

    assert entry_map["display_foundation_primary"].final_visible_screen_state_ready is True
    assert entry_map["display_foundation_primary"].presentation_bundle_runtime_ready is True
