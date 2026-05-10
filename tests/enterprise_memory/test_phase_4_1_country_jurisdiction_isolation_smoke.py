from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_legal_jurisdiction_contract,
    build_memory_isolation_contract,
    build_regulatory_memory_contract,
)


def test_phase_4_1_country_jurisdiction_isolation_smoke() -> None:
    jurisdictions = build_legal_jurisdiction_contract()
    regulatory = build_regulatory_memory_contract()
    isolation = build_memory_isolation_contract()

    assert {entry.country_code for entry in jurisdictions.entries} == {"DE", "UA", "EU"}
    assert {entry.country_code for entry in regulatory.entries} == {"DE", "UA", "EU"}
    assert {entry.country_code for entry in isolation.entries} == {"DE", "UA", "EU"}

    assert regulatory.country_bound_records == 3
    assert isolation.cross_country_merge_allowed_isolations == 0
