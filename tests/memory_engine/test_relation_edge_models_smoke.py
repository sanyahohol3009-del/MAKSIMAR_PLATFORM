from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_edge_models import (
    RelationEdge,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_id_models import (
    RelationId,
)


def test_relation_edge_models_smoke() -> None:
    edge = RelationEdge(
        relation_id=RelationId("REL-0001"),
        from_id="HSTORE-RAW-001",
        to_id="HSTORE-NORM-001",
        relation_type="normalized_into",
        graph_ready=True,
    )

    assert edge.graph_ready is True
    assert edge.relation_type == "normalized_into"
