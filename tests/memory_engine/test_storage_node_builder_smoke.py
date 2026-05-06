from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_builder import (
    build_default_storage_nodes,
)


def test_storage_node_builder_smoke() -> None:
    nodes = build_default_storage_nodes()

    assert len(nodes) == 3
    assert nodes[0].storage_node_id.value == "HSTORE-RAW-001"
    assert nodes[1].storage_node_id.value == "HSTORE-NORM-001"
    assert nodes[2].storage_node_id.value == "HSTORE-REG-001"
