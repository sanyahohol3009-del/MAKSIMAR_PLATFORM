from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_status_bar_contract import (
    build_visual_status_bar_contract,
)


def test_visual_status_bar_contract_builds() -> None:
    contract = build_visual_status_bar_contract()
    assert contract.status_bar_id == "visual_status_bar_contract_001"
    assert contract.theme_id == "visual_theme_operator_hud_001"
    assert contract.global_health_visible is True
    assert contract.workspace_state_visible is True
    assert contract.mode_visible is True
