from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_main_operator_dashboard_contract,
)


def test_main_operator_dashboard_contract_builds() -> None:
    """Main operator dashboard contract should build successfully."""
    contract = build_main_operator_dashboard_contract()

    assert contract.total_entries == 1
    assert contract.operator_workspace_entries == 1
    assert contract.read_only_entries == 0
    assert contract.interactive_entries == 1


def test_main_operator_dashboard_entry() -> None:
    """Main operator dashboard entry should remain canonical."""
    contract = build_main_operator_dashboard_contract()
    entry = contract.entries[0]

    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.total_panels == 3
    assert entry.main_focus_panels == 2
    assert entry.secondary_panels == 1
    assert entry.read_only is False
