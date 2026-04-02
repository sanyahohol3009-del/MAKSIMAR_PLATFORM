from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_signal_overlay_contract import (
    build_visual_signal_overlay_contract,
)


def test_visual_signal_overlay_contract_builds() -> None:
    """Visual signal overlay contract should build successfully."""
    contract = build_visual_signal_overlay_contract()

    assert contract.contract_id == "visual_signal_overlay_contract_001"
    assert contract.total_entries > 0
    assert contract.read_only_entries == contract.total_entries


def test_visual_signal_overlay_contract_contains_runtime_core_signal() -> None:
    """Visual signal overlay should contain runtime foundation signal entry."""
    contract = build_visual_signal_overlay_contract()
    entry = next(
        item
        for item in contract.entries
        if item.source_panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.signal_id == "visual_signal_panel_foundation_runtime_status_001"
    assert entry.target_anchor_role == "core"
    assert entry.line_style == "core_stream"
    assert entry.line_state == "highlighted"
    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.read_only is True


def test_visual_signal_overlay_contract_contains_navigation_signal() -> None:
    """Visual signal overlay should contain navigation signal entry."""
    contract = build_visual_signal_overlay_contract()
    entry = next(
        item for item in contract.entries if item.source_panel_id == "panel_navigation"
    )

    assert entry.target_anchor_role == "left_navigation"
    assert entry.line_style == "operator_stream"
    assert entry.line_state == "passive"
    assert entry.visual_priority == "supporting"


def test_visual_signal_overlay_contract_counts_are_consistent() -> None:
    """Visual signal overlay counts should remain internally consistent."""
    contract = build_visual_signal_overlay_contract()

    assert (
        contract.active_entries
        + contract.passive_entries
        + contract.highlighted_entries
        == contract.total_entries
    )
    assert (
        contract.core_stream_entries
        + contract.diagnostics_stream_entries
        + contract.topology_stream_entries
        + contract.operator_stream_entries
        == contract.total_entries
    )
