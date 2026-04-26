from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_preview_contract import (
    build_visual_hud_preview_contract,
)


def test_visual_hud_preview_contract_builds() -> None:
    contract = build_visual_hud_preview_contract()
    assert contract.preview_id == "visual_hud_preview_contract_001"
    assert contract.snapshot_id == "visual_hud_snapshot_contract_001"
    assert contract.preview_ready is True
    assert contract.renderer_preview_enabled is True
