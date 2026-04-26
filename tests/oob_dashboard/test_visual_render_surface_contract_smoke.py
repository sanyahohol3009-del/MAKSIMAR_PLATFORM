from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_render_surface_contract import (
    build_visual_render_surface_contract,
)


def test_visual_render_surface_contract_builds() -> None:
    contract = build_visual_render_surface_contract()
    assert contract.contract_id == "visual_render_surface_contract_001"
    assert contract.total_entries == 3
    assert contract.render_ready_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3
