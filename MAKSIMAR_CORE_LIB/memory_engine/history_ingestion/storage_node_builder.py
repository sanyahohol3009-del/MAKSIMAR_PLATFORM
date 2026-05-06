from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_id_models import (
    StorageNodeId,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_models import (
    StorageNode,
)


def build_default_storage_nodes() -> Tuple[StorageNode, ...]:
    return (
        StorageNode(
            storage_node_id=StorageNodeId("HSTORE-RAW-001"),
            storage_node_type="raw_archive_store",
            title="Raw imported history files",
            path_role="raw_input",
            readable_by_jarvis=False,
            writable_by_ingestion=True,
            portable=True,
            dashboard_ready=True,
        ),
        StorageNode(
            storage_node_id=StorageNodeId("HSTORE-NORM-001"),
            storage_node_type="normalized_history_store",
            title="Normalized project history memory",
            path_role="normalized_memory",
            readable_by_jarvis=True,
            writable_by_ingestion=True,
            portable=True,
            dashboard_ready=True,
        ),
        StorageNode(
            storage_node_id=StorageNodeId("HSTORE-REG-001"),
            storage_node_type="import_registry_store",
            title="Import session and manifest registry",
            path_role="registry",
            readable_by_jarvis=True,
            writable_by_ingestion=True,
            portable=True,
            dashboard_ready=True,
        ),
    )


def build_storage_node_preview(
    storage_node: StorageNode,
) -> Dict[str, object]:
    return {
        "storage_node_id": storage_node.storage_node_id.value,
        "storage_node_type": storage_node.storage_node_type,
        "title": storage_node.title,
        "path_role": storage_node.path_role,
        "readable_by_jarvis": storage_node.readable_by_jarvis,
        "writable_by_ingestion": storage_node.writable_by_ingestion,
        "portable": storage_node.portable,
        "dashboard_ready": storage_node.dashboard_ready,
    }
