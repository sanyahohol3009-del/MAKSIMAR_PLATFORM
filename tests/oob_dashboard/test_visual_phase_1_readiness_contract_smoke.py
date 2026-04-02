from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_phase_1_readiness_contract import (
    build_visual_phase_1_readiness_contract,
)


def test_visual_phase_1_readiness_contract_builds() -> None:
    """Visual Phase 1 readiness contract should build successfully."""
    contract = build_visual_phase_1_readiness_contract()

    assert contract.contract_id == "visual_phase_1_readiness_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_phase_1_readiness_contains_expected_entry() -> None:
    """Visual Phase 1 readiness contract should contain canonical entry."""
    contract = build_visual_phase_1_readiness_contract()
    entry = contract.entries[0]

    assert entry.readiness_id == "visual_phase_1_readiness_001"
    assert entry.readiness_mode == "phase_1_visual_polish_readiness"
    assert entry.readiness_status == "ready_for_preview_render_polish"
    assert entry.theme_hardening_id == "visual_theme_hardening_001"
    assert (
        entry.panel_hierarchy_hardening_id
        == "visual_panel_hierarchy_hardening_001"
    )
    assert entry.center_core_refinement_id == "visual_center_core_refinement_001"
    assert (
        entry.sidebar_navigation_refinement_id
        == "visual_sidebar_navigation_refinement_001"
    )
    assert (
        entry.status_ticker_refinement_id
        == "visual_status_ticker_refinement_001"
    )


def test_visual_phase_1_readiness_marks_all_phase_1_passes_complete() -> None:
    """Visual Phase 1 readiness should mark all Phase 1 passes complete."""
    contract = build_visual_phase_1_readiness_contract()
    entry = contract.entries[0]

    assert entry.theme_hardening_complete is True
    assert entry.panel_hierarchy_complete is True
    assert entry.center_core_complete is True
    assert entry.sidebar_navigation_complete is True
    assert entry.status_ticker_complete is True


def test_visual_phase_1_readiness_preserves_read_only_boundary() -> None:
    """Visual Phase 1 readiness should preserve read-only boundary."""
    contract = build_visual_phase_1_readiness_contract()
    entry = contract.entries[0]

    assert entry.read_only is True
