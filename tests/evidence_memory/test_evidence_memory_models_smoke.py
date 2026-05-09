from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import build_evidence_memory_contract


def test_evidence_memory_models_smoke() -> None:
    contract = build_evidence_memory_contract()

    assert contract.total_records == 6
    assert contract.ready_records == contract.total_records
    assert contract.conflict_detected_records == 0
