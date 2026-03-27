from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_system_status_panel_content_contract,
)


def test_system_status_panel_content_contract_builds() -> None:
    """System-status panel content contract should build successfully."""
    contract = build_system_status_panel_content_contract()

    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.main_dashboard_visible_entries == 1
    assert contract.oob_visible_entries == 1


def test_system_status_panel_content_entry() -> None:
    """System-status panel content entry should remain canonical."""
    contract = build_system_status_panel_content_contract()
    entry = contract.entries[0]

    assert entry.panel_id == "panel_system_status_001"
    assert entry.runtime_panel_id == "panel_foundation_runtime_status_001"
    assert entry.guard_panel_id == "panel_foundation_guard_status_001"
    assert entry.core_guard_panel_id == "panel_foundation_core_guard_status_001"
    assert entry.kernel_guard_panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.total_foundation_entries == 4
    assert entry.visible_in_main_dashboard is True
    assert entry.visible_in_oob_dashboard is True
    assert entry.read_only is True
