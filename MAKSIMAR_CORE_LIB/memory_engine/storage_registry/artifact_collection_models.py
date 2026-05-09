from __future__ import annotations

import re
from dataclasses import dataclass


_COLLECTION_ID_PATTERN = re.compile(r"^artifact_collection_[a-z][a-z0-9_]*$")
_STORAGE_NODE_ID_PATTERN = re.compile(r"^storage_node_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True, slots=True)
class ArtifactCollectionReference:
    """Metadata reference for a logical artifact collection."""

    collection_id: str
    title: str
    storage_node_id: str
    artifact_kind: str
    portable: bool
    dashboard_ready: bool

    def __post_init__(self) -> None:
        collection_id = _ensure_non_empty_str(self.collection_id, "collection_id")
        title = _ensure_non_empty_str(self.title, "title")
        storage_node_id = _ensure_non_empty_str(self.storage_node_id, "storage_node_id")
        artifact_kind = _ensure_non_empty_str(self.artifact_kind, "artifact_kind")

        if not _COLLECTION_ID_PATTERN.fullmatch(collection_id):
            raise ValueError(f"Invalid collection_id: {collection_id}")
        if not _STORAGE_NODE_ID_PATTERN.fullmatch(storage_node_id):
            raise ValueError(f"Invalid storage_node_id: {storage_node_id}")
        if not isinstance(self.portable, bool):
            raise ValueError("portable must be bool")
        if not isinstance(self.dashboard_ready, bool):
            raise ValueError("dashboard_ready must be bool")

        object.__setattr__(self, "collection_id", collection_id)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "storage_node_id", storage_node_id)
        object.__setattr__(self, "artifact_kind", artifact_kind)
