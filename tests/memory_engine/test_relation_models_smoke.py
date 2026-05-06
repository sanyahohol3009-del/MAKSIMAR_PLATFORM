from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_models import (
    MemoryRelation,
)


def test_relation_models_smoke() -> None:
    relation = MemoryRelation(
        relation_id="REL-0101",
        from_memory_id="ARCH-0001",
        to_ref="PHASE3-BATCH1",
        relation_type="next_step",
        graph_ready=True,
        timeline_ready=True,
    )

    assert relation.relation_type == "next_step"
