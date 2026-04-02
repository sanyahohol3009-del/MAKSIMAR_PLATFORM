from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_preview_render_polish_readiness_contract import (
    build_visual_preview_render_polish_readiness_contract,
)


def test_visual_preview_render_polish_readiness_contract_builds() -> None:
    """Preview/render polish readiness contract should build successfully."""
    contract = build_visual_preview_render_polish_readiness_contract()

    assert contract.contract_id == "visual_preview_render_polish_readiness_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.read_only_entries == 1


def test_visual_preview_render_polish_readiness_contains_expected_entry() -> None:
    """Preview/render polish readiness contract should contain canonical entry."""
    contract = build_visual_preview_render_polish_readiness_contract()
    entry = contract.entries[0]

    assert entry.readiness_id == "visual_preview_render_polish_readiness_001"
    assert entry.phase_1_readiness_id == "visual_phase_1_readiness_001"
    assert entry.preview_state_id == "visual_hud_preview_state_001"
    assert entry.readiness_mode == "preview_render_polish_readiness"
    assert entry.readiness_status == "ready_for_preview_render_polish"


def test_visual_preview_render_polish_readiness_marks_all_inputs_ready() -> None:
    """Preview/render polish readiness should mark all required inputs ready."""
    contract = build_visual_preview_render_polish_readiness_contract()
    entry = contract.entries[0]

    assert entry.theme_hardening_ready is True
    assert entry.panel_hierarchy_ready is True
    assert entry.center_core_ready is True
    assert entry.sidebar_navigation_ready is True
    assert entry.status_ticker_ready is True
    assert entry.preview_state_ready is True


def test_visual_preview_render_polish_readiness_preserves_read_only_boundary() -> None:
    """Preview/render polish readiness should preserve read-only boundary."""
    contract = build_visual_preview_render_polish_readiness_contract()
    entry = contract.entries[0]

    assert entry.read_only is True
