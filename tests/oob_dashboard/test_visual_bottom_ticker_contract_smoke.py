from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_bottom_ticker_contract import (
    build_visual_bottom_ticker_contract,
)


def test_visual_bottom_ticker_contract_builds() -> None:
    contract = build_visual_bottom_ticker_contract()
    assert contract.bottom_ticker_id == "visual_bottom_ticker_contract_001"
    assert contract.theme_id == "visual_theme_operator_hud_001"
    assert contract.ticker_enabled is True
    assert contract.incident_summary_visible is True
    assert contract.flow_state_visible is True
