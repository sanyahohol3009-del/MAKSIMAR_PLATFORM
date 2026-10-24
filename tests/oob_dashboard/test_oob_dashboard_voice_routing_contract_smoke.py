from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.voice_routing_contract import (
    build_voice_routing_contract,
)


def test_voice_routing_contract_builds() -> None:
    contract = build_voice_routing_contract()
    assert contract.contract_id == "voice_routing_contract_001"
    assert contract.total_entries == 3
    assert contract.routed_entries == 3
    assert contract.guarded_entries == 3
