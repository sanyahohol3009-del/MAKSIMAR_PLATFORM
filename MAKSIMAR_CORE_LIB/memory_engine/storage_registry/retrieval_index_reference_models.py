from __future__ import annotations

import re
from dataclasses import dataclass


_INDEX_ID_PATTERN = re.compile(r"^retrieval_index_[a-z][a-z0-9_]*$")
_STORAGE_NODE_ID_PATTERN = re.compile(r"^storage_node_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True, slots=True)
class RetrievalIndexReference:
    """Metadata reference for retrieval/RAG index storage."""

    retrieval_index_id: str
    title: str
    storage_node_id: str
    backend_kind: str
    rebuild_required: bool
    portable: bool

    def __post_init__(self) -> None:
        retrieval_index_id = _ensure_non_empty_str(
            self.retrieval_index_id,
            "retrieval_index_id",
        )
        title = _ensure_non_empty_str(self.title, "title")
        storage_node_id = _ensure_non_empty_str(self.storage_node_id, "storage_node_id")
        backend_kind = _ensure_non_empty_str(self.backend_kind, "backend_kind")

        if not _INDEX_ID_PATTERN.fullmatch(retrieval_index_id):
            raise ValueError(f"Invalid retrieval_index_id: {retrieval_index_id}")
        if not _STORAGE_NODE_ID_PATTERN.fullmatch(storage_node_id):
            raise ValueError(f"Invalid storage_node_id: {storage_node_id}")
        if not isinstance(self.rebuild_required, bool):
            raise ValueError("rebuild_required must be bool")
        if not isinstance(self.portable, bool):
            raise ValueError("portable must be bool")

        object.__setattr__(self, "retrieval_index_id", retrieval_index_id)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "storage_node_id", storage_node_id)
        object.__setattr__(self, "backend_kind", backend_kind)
