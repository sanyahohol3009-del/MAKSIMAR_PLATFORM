from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_builder import (
    build_default_storage_nodes,
)


def test_storage_node_dashboard_readiness_smoke() -> None:
    nodes = build_default_storage_nodes()
    assert all(node.dashboard_ready for node in nodes)
