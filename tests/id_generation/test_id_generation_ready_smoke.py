from __future__ import annotations

from MAKSIMAR_CORE_LIB.id_generation import (
    build_canonical_id_flow_preview,
    build_canonical_id_generation_contract,
)


def test_id_generation_ready_smoke() -> None:
    contract = build_canonical_id_generation_contract()
    preview = build_canonical_id_flow_preview(contract)

    assert contract.total_entries == len(contract.entries)
    assert contract.total_storage_node_ids == sum(
        1 for entry in contract.entries if entry.storage_node_id
    )
    assert preview["preview_ready"] is True
    assert preview["total_entries"] == contract.total_entries
    assert preview["total_storage_node_ids"] == contract.total_storage_node_ids
    assert preview["total_retrieval_source_ids"] == contract.total_retrieval_source_ids
