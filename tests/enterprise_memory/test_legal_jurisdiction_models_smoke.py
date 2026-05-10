from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_legal_jurisdiction_contract,
)


def test_legal_jurisdiction_models_smoke() -> None:
    contract = build_legal_jurisdiction_contract()

    assert contract.total_jurisdictions == 3
    assert contract.ready_jurisdictions == contract.total_jurisdictions
    assert contract.source_bound_jurisdictions == contract.total_jurisdictions
    assert contract.versioned_jurisdictions == contract.total_jurisdictions
    assert contract.read_only_jurisdictions == contract.total_jurisdictions
    assert contract.approval_required_jurisdictions == contract.total_jurisdictions

    country_codes = {entry.country_code for entry in contract.entries}
    assert country_codes == {"DE", "UA", "EU"}
