from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_panel_content_contract,
)


def test_panel_content_contract_builds() -> None:
    """Panel content contract should build successfully."""
    contract = build_panel_content_contract()

    assert contract.total_entries == 19
    assert contract.foundation_content_entries == 4
    assert contract.diagnostics_content_entries == 4
    assert contract.interaction_content_entries == 3
    assert contract.execution_content_entries == 7
    assert contract.navigation_content_entries == 1
    assert contract.read_only_entries == 16
    assert contract.interactive_entries == 3


def test_panel_content_foundation_runtime_entry() -> None:
    """Foundation runtime panel should bind to foundation content contract."""
    contract = build_panel_content_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.content_contract_kind == "foundation_status_summary_contract"
    assert entry.content_contract_name == "build_foundation_status_panel_summary_contract"
    assert entry.content_scope == "foundation"
    assert entry.read_only is True


def test_panel_content_chat_entry() -> None:
    """Chat panel should remain interaction content."""
    contract = build_panel_content_contract()
    entry = next(entry for entry in contract.entries if entry.panel_id == "panel_chat")

    assert entry.content_contract_kind == "interaction_contract"
    assert entry.content_contract_name == "build_dashboard_chat_contract"
    assert entry.content_scope == "interaction"
    assert entry.read_only is False


def test_panel_content_navigation_entry() -> None:
    """Navigation panel should use navigation content contract."""
    contract = build_panel_content_contract()
    entry = next(
        entry for entry in contract.entries if entry.panel_id == "panel_navigation"
    )

    assert entry.content_contract_kind == "navigation_contract"
    assert entry.content_contract_name == "build_dashboard_navigation_contract"
    assert entry.content_scope == "navigation"
    assert entry.read_only is True
