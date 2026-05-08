from __future__ import annotations

from MAKSIMAR_CORE_LIB.id_generation import (
    build_canonical_id_generation_contract,
)


def test_canonical_id_extension_fields_smoke() -> None:
    contract = build_canonical_id_generation_contract()

    assert contract.total_entries == len(contract.entries)
    assert contract.total_storage_node_ids == sum(
        1 for entry in contract.entries if entry.storage_node_id
    )
    assert contract.total_retrieval_source_ids == sum(
        1 for entry in contract.entries if entry.retrieval_source_id
    )

    for entry in contract.entries:
        assert entry.storage_node_id == f"storage_node_{entry.module_slug}"
        assert entry.artifact_ref_prefix == f"artifact://modules/{entry.module_slug}"
        assert entry.trace_id_prefix == f"trace_{entry.module_slug}"
        if entry.retrieval_source_id:
            assert entry.retrieval_source_id == f"retrieval_source_{entry.module_slug}"
        assert entry.collision_free is True
