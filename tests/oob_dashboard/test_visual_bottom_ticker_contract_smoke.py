from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_bottom_ticker_contract import (
    build_visual_bottom_ticker_contract,
)


def test_visual_bottom_ticker_contract_builds() -> None:
    """Visual bottom ticker contract should build successfully."""
    contract = build_visual_bottom_ticker_contract()

    assert contract.contract_id == "visual_bottom_ticker_contract_001"
    assert contract.total_entries == 1
    assert contract.visible_entries == 1
    assert contract.read_only_entries == 1


def test_visual_bottom_ticker_contains_expected_entry() -> None:
    """Visual bottom ticker should contain canonical bottom-strip entry."""
    contract = build_visual_bottom_ticker_contract()
    entry = contract.entries[0]

    assert entry.ticker_id == "visual_bottom_ticker_001"
    assert entry.panel_id == "panel_logs_001"
    assert entry.renderer_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.severity == "normal"
    assert entry.mode == "log_stream"
    assert entry.visible is True
    assert entry.read_only is True


def test_visual_bottom_ticker_log_counts_are_consistent() -> None:
    """Visual bottom ticker log counts should remain internally consistent."""
    contract = build_visual_bottom_ticker_contract()
    entry = contract.entries[0]

    assert entry.total_log_sources == 4
    assert entry.active_log_sources == 4
    assert entry.highlighted_log_sources == 0


def test_visual_bottom_ticker_severity_counts_are_consistent() -> None:
    """Visual bottom ticker severity counts should remain internally consistent."""
    contract = build_visual_bottom_ticker_contract()

    assert (
        contract.normal_entries
        + contract.warning_entries
        + contract.critical_entries
        == contract.total_entries
    )
