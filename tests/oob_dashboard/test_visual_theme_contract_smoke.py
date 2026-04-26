from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_theme_contract import (
    build_visual_theme_contract,
)


def test_visual_theme_contract_builds() -> None:
    contract = build_visual_theme_contract()
    assert contract.theme_id == "visual_theme_operator_hud_001"
    assert contract.theme_family == "operator_hud_theme"
    assert contract.glow_enabled is True
    assert contract.depth_enabled is True
