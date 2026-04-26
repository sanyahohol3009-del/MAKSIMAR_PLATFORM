from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_inventory_contract import (
    build_monitor_inventory_contract,
)


def test_monitor_inventory_contract_builds() -> None:
    """Monitor inventory contract should build successfully."""
    contract = build_monitor_inventory_contract()

    assert contract.contract_id == "monitor_inventory_contract_001"
    assert contract.total_entries == 3
    assert contract.foundation_monitor_entries == 2
    assert contract.operator_monitor_entries == 1
    assert contract.operator_visible_entries == 3


def test_monitor_inventory_contract_contains_expected_entries() -> None:
    """Monitor inventory contract should expose canonical monitor set."""
    contract = build_monitor_inventory_contract()
    entry_map = {entry.display_target_id: entry for entry in contract.entries}

    assert entry_map["display_foundation_primary"].monitor_role == "foundation_primary_monitor"
    assert entry_map["display_foundation_secondary"].monitor_role == "foundation_secondary_monitor"
    assert entry_map["display_operator_interaction"].monitor_role == "operator_interaction_monitor"


def test_monitor_inventory_contract_preserves_multi_monitor_semantics() -> None:
    """All canonical inventory entries should remain multi-monitor capable."""
    contract = build_monitor_inventory_contract()

    assert all(entry.multi_monitor_capable for entry in contract.entries)
    assert all(entry.operator_visible for entry in contract.entries)
