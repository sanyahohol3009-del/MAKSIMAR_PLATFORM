from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_panel_view_display_chain_contract,
)


def test_panel_view_display_chain_contract_builds() -> None:
    """Panel → view → display chain contract should build successfully."""
    contract = build_panel_view_display_chain_contract()

    assert contract.total_entries == 19
    assert contract.primary_operator_chains == 3
    assert contract.diagnostics_chains == 8
    assert contract.expansion_chains == 8
    assert contract.default_chains == 19


def test_panel_view_display_chain_chat_entry() -> None:
    """Chat panel should map to chat view and primary operator display."""
    contract = build_panel_view_display_chain_contract()
    entry = next(entry for entry in contract.entries if entry.panel_id == "panel_chat")

    assert entry.view_id == "view_chat"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.display_role == "primary_operator"
    assert entry.display_zone == "center"
    assert entry.is_default_chain is True


def test_panel_view_display_chain_foundation_runtime_entry() -> None:
    """Foundation runtime panel should map to foundation view and diagnostics display."""
    contract = build_panel_view_display_chain_contract()
    entry = next(
        entry
        for entry in contract.entries
        if entry.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.view_id == "view_foundation_runtime"
    assert entry.display_target_id == "display_secondary_diagnostics"
    assert entry.display_role == "diagnostics"
    assert entry.display_zone == "right"


def test_panel_view_display_chain_navigation_entry() -> None:
    """Navigation panel should map to navigation view and expansion display."""
    contract = build_panel_view_display_chain_contract()
    entry = next(
        entry for entry in contract.entries if entry.panel_id == "panel_navigation"
    )

    assert entry.view_id == "view_navigation"
    assert entry.display_target_id == "display_tertiary_expansion"
    assert entry.display_role == "expansion"
    assert entry.display_zone == "left"
