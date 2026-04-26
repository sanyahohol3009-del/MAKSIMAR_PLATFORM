from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.voice_display_handoff_contract import (
    build_voice_display_handoff_contract,
)


def test_voice_display_handoff_contract_builds() -> None:
    contract = build_voice_display_handoff_contract()
    assert contract.contract_id == "voice_display_handoff_contract_001"
    assert contract.total_entries == 3
    assert contract.ready_entries == 3
    assert contract.guarded_entries == 3
