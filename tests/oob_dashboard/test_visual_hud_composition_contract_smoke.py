from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_composition_contract import (
    build_visual_hud_composition_contract,
)


def test_visual_hud_composition_contract_builds() -> None:
    contract = build_visual_hud_composition_contract()
    assert contract.composition_id == "visual_hud_composition_contract_001"
    assert contract.shell_id == "visual_shell_contract_001"
    assert contract.renderer_id == "visual_renderer_contract_001"
    assert contract.signal_overlay_ready is True
    assert contract.topology_overlay_ready is True
    assert contract.explainability_sidebar_ready is True
    assert contract.status_bar_ready is True
    assert contract.bottom_ticker_ready is True
    assert contract.composition_ready is True
