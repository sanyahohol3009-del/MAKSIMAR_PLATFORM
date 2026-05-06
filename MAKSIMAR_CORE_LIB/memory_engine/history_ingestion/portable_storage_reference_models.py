from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class PortableStorageReference:
    storage_node_id: str
    root_id: str
    relative_path: str
    portable: bool
    manifest_safe: bool
    nas_ready: bool

    def __post_init__(self) -> None:
        storage_node_id = _ensure_non_empty_str(self.storage_node_id, "storage_node_id")
        root_id = _ensure_non_empty_str(self.root_id, "root_id")
        relative_path = _ensure_non_empty_str(self.relative_path, "relative_path")

        if relative_path.startswith("/"):
            raise ValueError("relative_path must stay relative, not absolute")

        if not self.portable:
            raise ValueError("portable must be True")

        if not self.manifest_safe:
            raise ValueError("manifest_safe must be True")

        object.__setattr__(self, "storage_node_id", storage_node_id)
        object.__setattr__(self, "root_id", root_id)
        object.__setattr__(self, "relative_path", relative_path)
