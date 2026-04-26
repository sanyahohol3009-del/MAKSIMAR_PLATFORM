from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_shell_canonical_panel_contract import (
    build_visual_shell_canonical_panel_contract,
)


def test_visual_shell_canonical_panel_contract_builds() -> None:
    """Visual-shell canonical panel contract should build successfully."""
    contract = build_visual_shell_canonical_panel_contract()

    assert contract.contract_id == "visual_shell_canonical_panel_contract_001"
    assert contract.total_entries == 3
    assert contract.read_only_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.no_renderer_leakage_entries == 3
    assert contract.operator_visible is True


def test_visual_shell_canonical_panel_contract_contains_runtime_entry() -> None:
    """Visual-shell canonical panel contract should contain runtime entry."""
    contract = build_visual_shell_canonical_panel_contract()

    entry = next(
        item
        for item in contract.entries
        if item.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.canonical_panel_kind == "foundation_runtime_status"
    assert entry.panel_semantics == "runtime_truth_surface"
    assert entry.renderer_semantics_leakage_allowed is False
    assert entry.read_only is True
    assert entry.operator_visible is True
