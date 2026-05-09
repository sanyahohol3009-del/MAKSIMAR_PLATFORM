from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_source_chain_contract,
    build_evidence_source_chain_preview,
)


def test_phase_2_1_batch1_evidence_source_chain_ready_smoke() -> None:
    contract = build_evidence_source_chain_contract()
    preview = build_evidence_source_chain_preview()

    assert preview["phase_batch_ready"] is True
    assert contract.total_items == preview["total_items"]
    assert contract.ready_items == contract.total_items
    assert contract.retrieval_phase_ready is True
    assert contract.storage_phase_ready is True
    assert contract.media_phase_ready is True
    assert contract.architecture_control_ready is True
