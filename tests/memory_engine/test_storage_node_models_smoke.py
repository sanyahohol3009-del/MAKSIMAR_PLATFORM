from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_id_models import (
    StorageNodeId,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_models import (
    StorageNode,
)


def test_storage_node_models_smoke() -> None:
    node = StorageNode(
        storage_node_id=StorageNodeId("HSTORE-RAW-001"),
        storage_node_type="raw_archive_store",
        title="Raw imported history files",
        path_role="raw_input",
        readable_by_jarvis=False,
        writable_by_ingestion=True,
        portable=True,
        dashboard_ready=True,
    )

    assert node.portable is True
    assert node.dashboard_ready is True
