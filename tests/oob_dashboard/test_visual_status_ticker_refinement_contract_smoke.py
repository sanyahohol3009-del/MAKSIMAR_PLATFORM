from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_status_ticker_refinement_contract import (
    build_visual_status_ticker_refinement_contract,
)


def test_visual_status_ticker_refinement_contract_builds() -> None:
    """Visual status/ticker refinement contract should build successfully."""
    contract = build_visual_status_ticker_refinement_contract()

    assert contract.contract_id == "visual_status_ticker_refinement_contract_001"
    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.stronger_status_entries == 1
    assert contract.stronger_ticker_entries == 1


def test_visual_status_ticker_refinement_contains_expected_entry() -> None:
    """Visual status/ticker refinement contract should contain canonical entry."""
    contract = build_visual_status_ticker_refinement_contract()
    entry = contract.entries[0]

    assert entry.refinement_id == "visual_status_ticker_refinement_001"
    assert (
        entry.sidebar_navigation_refinement_id
        == "visual_sidebar_navigation_refinement_001"
    )
    assert entry.refinement_mode == "phase_1_status_ticker_refinement"
    assert entry.status_clarity_profile == "strong_top_status_readability"
    assert entry.ticker_clarity_profile == "strong_bottom_ticker_readability"
    assert entry.operator_signal_profile == "clear_operator_signal_ribbon"


def test_visual_status_ticker_refinement_preserves_read_only_boundary() -> None:
    """Visual status/ticker refinement should preserve read-only boundary."""
    contract = build_visual_status_ticker_refinement_contract()
    entry = contract.entries[0]

    assert entry.read_only is True
    assert entry.status_entries > 0
    assert entry.ticker_entries > 0


def test_visual_status_ticker_refinement_enables_allowed_phase_1_strengthening() -> None:
    """Visual status/ticker refinement should enable allowed Phase 1 strengthening."""
    contract = build_visual_status_ticker_refinement_contract()
    entry = contract.entries[0]

    assert entry.stronger_top_status_readability is True
    assert entry.stronger_bottom_ticker_readability is True
    assert entry.stronger_status_hierarchy is True
    assert entry.stronger_signal_ribbon_clarity is True
