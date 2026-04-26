from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_signal_overlay_contract import (
    build_visual_signal_overlay_contract,
)


def test_visual_signal_overlay_contract_builds() -> None:
    contract = build_visual_signal_overlay_contract()
    assert contract.contract_id == "visual_signal_overlay_contract_001"
    assert contract.total_entries == 2
    assert contract.overlay_ready_entries == 2
    assert contract.operator_visible_entries == 2
    assert contract.truth_bound_entries == 2
