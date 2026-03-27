from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_guard_chain_panel_content_contract,
)


def test_guard_chain_panel_content_contract_builds() -> None:
    """Guard-chain panel content contract should build successfully."""
    contract = build_guard_chain_panel_content_contract()

    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.main_dashboard_visible_entries == 1
    assert contract.oob_visible_entries == 1


def test_guard_chain_panel_content_entry() -> None:
    """Guard-chain panel content entry should remain canonical."""
    contract = build_guard_chain_panel_content_contract()
    entry = contract.entries[0]

    assert entry.panel_id == "panel_guard_chain_001"
    assert entry.total_chain_entries == 4
    assert entry.runtime_entry_present is True
    assert entry.guard_entry_present is True
    assert entry.core_guard_entry_present is True
    assert entry.kernel_guard_entry_present is True
    assert entry.visible_in_main_dashboard is True
    assert entry.visible_in_oob_dashboard is True
    assert entry.read_only is True
