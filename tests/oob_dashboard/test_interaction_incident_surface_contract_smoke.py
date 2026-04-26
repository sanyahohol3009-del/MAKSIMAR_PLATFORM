from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.interaction_incident_surface_contract import (
    build_interaction_incident_surface_contract,
)


def test_interaction_incident_surface_contract_builds() -> None:
    contract = build_interaction_incident_surface_contract()
    assert contract.contract_id == "interaction_incident_surface_contract_001"
    assert contract.total_entries == 2
    assert contract.ready_entries == 2
    assert contract.visible_entries == 2
    assert contract.guarded_entries == 2
