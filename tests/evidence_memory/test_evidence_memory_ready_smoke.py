from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import (
    build_evidence_memory_contract,
    build_evidence_memory_preview,
    build_evidence_memory_summary,
)


def test_evidence_memory_ready_smoke() -> None:
    contract = build_evidence_memory_contract()
    summary = build_evidence_memory_summary()
    preview = build_evidence_memory_preview()

    assert contract.ready_records == contract.total_records
    assert summary["summary_ready"] is True
    assert preview["phase_batch_ready"] is True
