from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_shell_contract import (
    build_visual_shell_contract,
)


def test_visual_shell_contract_builds() -> None:
    contract = build_visual_shell_contract()
    assert contract.shell_id == "visual_shell_contract_001"
    assert contract.canonical_panel_contract_id == "visual_shell_canonical_panel_contract_001"
    assert contract.render_surface_contract_id == "visual_render_surface_contract_001"
    assert contract.theme_id == "visual_theme_operator_hud_001"
    assert contract.shell_ready is True
