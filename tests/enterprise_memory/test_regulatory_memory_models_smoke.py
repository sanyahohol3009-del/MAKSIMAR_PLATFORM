from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_regulatory_memory_contract,
)


def test_regulatory_memory_models_smoke() -> None:
    contract = build_regulatory_memory_contract()

    assert contract.total_records == 3
    assert contract.ready_records == contract.total_records
    assert contract.source_bound_records == contract.total_records
    assert contract.versioned_records == contract.total_records
    assert contract.conflict_marker_allowed_records == contract.total_records
    assert contract.read_only_records == contract.total_records
    assert contract.runtime_policy_binding_allowed_records == 0
    assert contract.pending_approval_records == contract.total_records
    assert contract.country_bound_records == 3
