from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_visual_shell_canonical_panel_contract,
)


def test_visual_shell_canonical_panel_contract_builds() -> None:
    """Visual-shell canonical panel contract should build successfully."""
    contract = build_visual_shell_canonical_panel_contract()

    assert contract.contract_id == "visual_shell_canonical_panel_contract_001"
    assert contract.total_entries > 0
    assert contract.canonical_only_entries == contract.total_entries
    assert contract.visual_shell_allowed_entries == contract.total_entries
    assert contract.legacy_alias_entries == 0


def test_visual_shell_canonical_panel_contract_contains_expected_panels() -> None:
    """Visual-shell canonical panel contract should contain canonical panels."""
    contract = build_visual_shell_canonical_panel_contract()

    panel_ids = {entry.panel_id for entry in contract.entries}

    assert "panel_navigation" in panel_ids
    assert "panel_chat" in panel_ids
    assert "panel_settings" in panel_ids
    assert "panel_foundation_runtime_status_001" in panel_ids


def test_visual_shell_canonical_panel_entries_are_canonical_only() -> None:
    """Every visual-shell panel entry should remain canonical-only."""
    contract = build_visual_shell_canonical_panel_contract()

    for entry in contract.entries:
        assert entry.canonical_panel_id_only is True
        assert entry.visual_shell_allowed is True


def test_visual_shell_canonical_panel_runtime_entry_is_present() -> None:
    """Runtime foundation panel should be present across visual-shell routing layers."""
    contract = build_visual_shell_canonical_panel_contract()
    entry = next(
        item
        for item in contract.entries
        if item.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.present_in_panel_binding is True
    assert entry.present_in_view_targeting is True
    assert entry.present_in_panel_view_display_chain is True
    assert entry.present_in_display_runtime_resolver is True
    assert entry.canonical_panel_id_only is True
    assert entry.visual_shell_allowed is True
