from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_status_bar_contract import (
    build_visual_status_bar_contract,
)


def test_visual_status_bar_contract_builds() -> None:
    """Visual status bar contract should build successfully."""
    contract = build_visual_status_bar_contract()

    assert contract.contract_id == "visual_status_bar_contract_001"
    assert contract.total_entries == 1
    assert contract.visible_entries == 1
    assert contract.read_only_entries == 1


def test_visual_status_bar_contains_expected_entry() -> None:
    """Visual status bar should contain canonical top-strip entry."""
    contract = build_visual_status_bar_contract()
    entry = contract.entries[0]

    assert entry.status_bar_id == "visual_status_bar_001"
    assert entry.panel_id == "panel_system_status_001"
    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.severity == "normal"
    assert entry.mode == "foundation_summary"
    assert entry.visible is True
    assert entry.read_only is True


def test_visual_status_bar_runtime_counts_are_consistent() -> None:
    """Visual status bar runtime counts should remain internally consistent."""
    contract = build_visual_status_bar_contract()
    entry = contract.entries[0]

    assert entry.total_runtime_surfaces == 4
    assert entry.active_runtime_surfaces == 4
    assert entry.warning_runtime_surfaces == 0


def test_visual_status_bar_severity_counts_are_consistent() -> None:
    """Visual status bar severity counts should remain internally consistent."""
    contract = build_visual_status_bar_contract()

    assert (
        contract.normal_entries
        + contract.warning_entries
        + contract.critical_entries
        == contract.total_entries
    )
