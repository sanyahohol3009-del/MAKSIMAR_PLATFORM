from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.id_generation import (
    CanonicalIdGenerationContract,
    build_canonical_id_generation_contract,
)


def test_canonical_id_collision_boundary_smoke() -> None:
    contract = build_canonical_id_generation_contract()
    first = contract.entries[0]

    with pytest.raises(ValueError, match="Duplicate module_ids detected"):
        CanonicalIdGenerationContract(
            total_entries=2,
            total_skill_ids=2 if first.skill_id else 0,
            total_memory_tier_ids=2 if first.memory_tier_id else 0,
            total_worker_ids=2 if first.worker_id else 0,
            total_storage_node_ids=2,
            total_retrieval_source_ids=2 if first.retrieval_source_id else 0,
            total_panel_ids=len(first.panel_ids) * 2,
            entries=(first, first),
        )
