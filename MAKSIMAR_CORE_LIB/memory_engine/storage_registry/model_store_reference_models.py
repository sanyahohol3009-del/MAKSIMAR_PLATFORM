from __future__ import annotations

import re
from dataclasses import dataclass


_MODEL_STORE_ID_PATTERN = re.compile(r"^model_store_[a-z][a-z0-9_]*$")
_STORAGE_NODE_ID_PATTERN = re.compile(r"^storage_node_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True, slots=True)
class ModelStoreReference:
    """Metadata reference for model weights/checkpoints."""

    model_store_id: str
    title: str
    storage_node_id: str
    model_family: str
    weights_external: bool
    portable: bool

    def __post_init__(self) -> None:
        model_store_id = _ensure_non_empty_str(self.model_store_id, "model_store_id")
        title = _ensure_non_empty_str(self.title, "title")
        storage_node_id = _ensure_non_empty_str(self.storage_node_id, "storage_node_id")
        model_family = _ensure_non_empty_str(self.model_family, "model_family")

        if not _MODEL_STORE_ID_PATTERN.fullmatch(model_store_id):
            raise ValueError(f"Invalid model_store_id: {model_store_id}")
        if not _STORAGE_NODE_ID_PATTERN.fullmatch(storage_node_id):
            raise ValueError(f"Invalid storage_node_id: {storage_node_id}")
        if not isinstance(self.weights_external, bool):
            raise ValueError("weights_external must be bool")
        if not isinstance(self.portable, bool):
            raise ValueError("portable must be bool")

        object.__setattr__(self, "model_store_id", model_store_id)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "storage_node_id", storage_node_id)
        object.__setattr__(self, "model_family", model_family)
