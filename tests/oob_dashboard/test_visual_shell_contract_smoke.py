from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_visual_shell_contract,
)


def test_visual_shell_contract_builds() -> None:
    """Visual-shell contract should build successfully."""
    contract = build_visual_shell_contract()

    assert contract.contract_id == "visual_shell_contract_001"
    assert contract.total_entries > 0
    assert contract.renderer_ready_entries == contract.total_entries
    assert contract.total_canonical_panel_entries > 0


def test_visual_shell_contract_contains_operator_shell_entry() -> None:
    """Visual-shell contract should contain canonical operator shell entry."""
    contract = build_visual_shell_contract()
    entry = contract.entries[0]

    assert entry.shell_id == "visual_shell_001"
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.renderer_ready is True
    assert entry.visual_mode == "operator_hud"


def test_visual_shell_contract_preserves_workspace_interaction_boundary() -> None:
    """Visual-shell contract should preserve workspace interaction boundary."""
    contract = build_visual_shell_contract()
    entry = contract.entries[0]

    assert entry.read_only is False
    assert entry.interactive is True


def test_visual_shell_contract_uses_canonical_panel_inventory() -> None:
    """Visual-shell contract should use canonical panel inventory."""
    contract = build_visual_shell_contract()
    entry = contract.entries[0]

    assert entry.canonical_panel_entries == contract.total_canonical_panel_entries
    assert entry.total_panels > 0
