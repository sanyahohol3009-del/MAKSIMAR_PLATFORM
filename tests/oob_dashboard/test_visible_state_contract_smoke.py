from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visible_state_contract import (
    build_visible_state_contract,
)


def test_visible_state_contract_builds() -> None:
    """Visible state contract should build successfully."""
    contract = build_visible_state_contract()

    assert contract.contract_id == "visible_state_contract_001"
    assert contract.total_entries == 4
    assert contract.foundation_visible_entries == 3
    assert contract.interaction_visible_entries == 1
    assert contract.operator_visible_entries == 4
    assert contract.truth_bound_entries == 4


def test_visible_state_contract_contains_expected_entries() -> None:
    """Visible state contract should contain expected canonical entries."""
    contract = build_visible_state_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert (
        entry_map["display_foundation_primary"].visible_state_class
        == "foundation_visible_state"
    )
    assert (
        entry_map["display_foundation_primary"].visible_state_mode
        == "assembled_foundation_visible_state"
    )

    assert (
        entry_map["display_operator_interaction"].visible_state_class
        == "interaction_visible_state"
    )
    assert (
        entry_map["display_operator_interaction"].visible_state_mode
        == "assembled_interaction_visible_state"
    )

    assert entry_map["display_foundation_primary"].final_visible_screen_state_ready is True
