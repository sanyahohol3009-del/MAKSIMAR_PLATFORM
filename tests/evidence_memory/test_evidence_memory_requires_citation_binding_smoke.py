from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import build_evidence_memory_contract


def test_evidence_memory_requires_citation_binding_smoke() -> None:
    contract = build_evidence_memory_contract()

    assert contract.citation_required_records == contract.total_records
    for record in contract.records:
        assert record.citation_required is True
