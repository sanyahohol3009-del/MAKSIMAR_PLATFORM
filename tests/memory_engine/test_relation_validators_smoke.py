from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_models import (
    MemoryRelation,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_validators import (
    validate_relation_set_ready,
)


def test_relation_validators_smoke() -> None:
    relations = (
        MemoryRelation(
            relation_id="REL-0101",
            from_memory_id="ARCH-0001",
            to_ref="STEP-1",
            relation_type="next_step",
            graph_ready=True,
            timeline_ready=True,
        ),
    )
    validate_relation_set_ready(relations)
