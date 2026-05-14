from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_track_contract


def test_regulatory_track_models_smoke() -> None:
    contract = build_regulatory_track_contract()

    assert contract.regulatory_track_ready is True
    assert contract.roadmap_family == "regulatory_memory_foundation"
    assert contract.track_id == "multi_tenant_multi_country_regulatory_memory_foundation"
    assert len(contract.stages) == 9
    assert len(contract.rules) == 5
    assert contract.memory_v5_1_closed_reference is True
    assert contract.reopen_memory_v5_1_allowed is False
