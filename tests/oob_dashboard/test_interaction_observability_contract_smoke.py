from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.interaction_observability_contract import (
    build_interaction_observability_contract,
)


def test_interaction_observability_contract_builds() -> None:
    contract = build_interaction_observability_contract()
    assert contract.contract_id == "interaction_observability_contract_001"
    assert contract.total_entries == 2
    assert contract.observable_entries == 2
    assert contract.incident_trackable_entries == 2
    assert contract.guarded_entries == 2
