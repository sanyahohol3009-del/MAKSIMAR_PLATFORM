from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_metadata_contract import (
    build_monitor_metadata_contract,
)


def test_monitor_metadata_contract_builds() -> None:
    """Monitor metadata contract should build successfully."""
    contract = build_monitor_metadata_contract()

    assert contract.contract_id == "monitor_metadata_contract_001"
    assert contract.total_entries == 3
    assert contract.foundation_metadata_entries == 2
    assert contract.operator_metadata_entries == 1
    assert contract.operator_visible_entries == 3


def test_monitor_metadata_contract_contains_expected_entries() -> None:
    """Monitor metadata contract should expose canonical metadata set."""
    contract = build_monitor_metadata_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert entry_map["display_foundation_primary"].display_role == "foundation_primary_display"
    assert entry_map["display_foundation_primary"].display_zone == "foundation_main_zone"
    assert entry_map["display_foundation_primary"].fallback_display_target_id == "display_foundation_secondary"

    assert entry_map["display_foundation_secondary"].display_role == "foundation_secondary_display"
    assert entry_map["display_foundation_secondary"].display_zone == "foundation_secondary_zone"
    assert entry_map["display_foundation_secondary"].fallback_display_target_id == "display_foundation_primary"

    assert entry_map["display_operator_interaction"].display_role == "operator_interaction_display"
    assert entry_map["display_operator_interaction"].display_zone == "operator_interaction_zone"
    assert entry_map["display_operator_interaction"].fallback_display_target_id == "display_operator_interaction"


def test_monitor_metadata_contract_preserves_assignment_and_visibility_semantics() -> None:
    """Canonical metadata entries should preserve assignment counts and visibility."""
    contract = build_monitor_metadata_contract()

    assert all(entry.assignment_count >= 1 for entry in contract.entries)
    assert all(entry.multi_monitor_capable for entry in contract.entries)
    assert all(entry.operator_visible for entry in contract.entries)
