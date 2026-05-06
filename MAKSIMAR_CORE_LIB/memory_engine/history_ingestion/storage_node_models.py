from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_id_models import (
    StorageNodeId,
)


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class StorageNode:
    storage_node_id: StorageNodeId
    storage_node_type: str
    title: str
    path_role: str
    readable_by_jarvis: bool
    writable_by_ingestion: bool
    portable: bool
    dashboard_ready: bool

    def __post_init__(self) -> None:
        storage_node_type = _ensure_non_empty_str(
            self.storage_node_type,
            "storage_node_type",
        )
        title = _ensure_non_empty_str(self.title, "title")
        path_role = _ensure_non_empty_str(self.path_role, "path_role")

        if not self.portable:
            raise ValueError("portable must be True")

        if not self.dashboard_ready:
            raise ValueError("dashboard_ready must be True")

        object.__setattr__(self, "storage_node_type", storage_node_type)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "path_role", path_role)
