from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_renderer_contract import (
    build_visual_renderer_contract,
)


def test_visual_renderer_contract_builds() -> None:
    contract = build_visual_renderer_contract()
    assert contract.renderer_id == "visual_renderer_contract_001"
    assert contract.shell_id == "visual_shell_contract_001"
    assert contract.render_surface_contract_id == "visual_render_surface_contract_001"
    assert contract.renderer_ready is True
    assert contract.semantic_leakage_allowed is False
