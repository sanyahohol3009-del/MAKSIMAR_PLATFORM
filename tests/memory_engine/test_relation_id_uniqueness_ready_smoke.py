from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_id_models import (
    RelationId,
)


def test_relation_id_uniqueness_ready_smoke() -> None:
    first = RelationId("REL-0001")
    second = RelationId("REL-0002")
    assert first.value != second.value
