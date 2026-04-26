from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.presentation_bundle_runtime_contract import (
    build_presentation_bundle_runtime_contract,
)


def test_presentation_bundle_runtime_contract_builds() -> None:
    """Presentation-bundle runtime contract should build successfully."""
    contract = build_presentation_bundle_runtime_contract()

    assert contract.contract_id == "presentation_bundle_runtime_contract_001"
    assert contract.total_entries == 4
    assert contract.foundation_runtime_entries == 3
    assert contract.interaction_runtime_entries == 1
    assert contract.operator_visible_entries == 4
    assert contract.truth_bound_entries == 4


def test_presentation_bundle_runtime_contract_contains_expected_entries() -> None:
    """Presentation-bundle runtime contract should contain expected canonical entries."""
    contract = build_presentation_bundle_runtime_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert (
        entry_map["display_foundation_primary"].presentation_bundle_runtime_class
        == "foundation_presentation_runtime"
    )
    assert (
        entry_map["display_foundation_primary"].presentation_bundle_runtime_mode
        == "assembled_foundation_presentation_runtime"
    )

    assert (
        entry_map["display_operator_interaction"].presentation_bundle_runtime_class
        == "interaction_presentation_runtime"
    )
    assert (
        entry_map["display_operator_interaction"].presentation_bundle_runtime_mode
        == "assembled_interaction_presentation_runtime"
    )

    assert entry_map["display_foundation_primary"].visible_state_ready is True
