from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import build_evidence_memory_contract


def test_evidence_pack_builder_smoke() -> None:
    contract = build_evidence_memory_contract()

    assert tuple(record.evidence_id for record in contract.records) == (
        "evidence_history_ingestion",
        "evidence_history_binding",
        "evidence_storage_registry",
        "evidence_media_memory",
        "evidence_memory_registry",
        "evidence_ai_router_binding",
    )
