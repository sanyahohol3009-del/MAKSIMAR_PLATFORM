from __future__ import annotations

import re
from dataclasses import dataclass


_MEDIA_STORE_ID_PATTERN = re.compile(r"^media_store_[a-z][a-z0-9_]*$")
_STORAGE_NODE_ID_PATTERN = re.compile(r"^storage_node_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True, slots=True)
class MediaArtifactReference:
    """Metadata reference for generated media artifacts."""

    media_store_id: str
    title: str
    storage_node_id: str
    media_kind: str
    raw_binary_external: bool
    retrieval_indexed: bool

    def __post_init__(self) -> None:
        media_store_id = _ensure_non_empty_str(self.media_store_id, "media_store_id")
        title = _ensure_non_empty_str(self.title, "title")
        storage_node_id = _ensure_non_empty_str(self.storage_node_id, "storage_node_id")
        media_kind = _ensure_non_empty_str(self.media_kind, "media_kind")

        if not _MEDIA_STORE_ID_PATTERN.fullmatch(media_store_id):
            raise ValueError(f"Invalid media_store_id: {media_store_id}")
        if not _STORAGE_NODE_ID_PATTERN.fullmatch(storage_node_id):
            raise ValueError(f"Invalid storage_node_id: {storage_node_id}")
        if not isinstance(self.raw_binary_external, bool):
            raise ValueError("raw_binary_external must be bool")
        if not isinstance(self.retrieval_indexed, bool):
            raise ValueError("retrieval_indexed must be bool")

        object.__setattr__(self, "media_store_id", media_store_id)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "storage_node_id", storage_node_id)
        object.__setattr__(self, "media_kind", media_kind)
