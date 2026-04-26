from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_snapshot_contract import (
    build_visual_hud_snapshot_contract,
)


def test_visual_hud_snapshot_contract_builds() -> None:
    contract = build_visual_hud_snapshot_contract()
    assert contract.snapshot_id == "visual_hud_snapshot_contract_001"
    assert contract.composition_id == "visual_hud_composition_contract_001"
    assert contract.snapshot_ready is True
    assert contract.preview_safe is True
