from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class StorageRoot:
    root_id: str
    root_type: str
    root_path: str
    portable: bool
    relocation_ready: bool
    nas_ready: bool

    def __post_init__(self) -> None:
        root_id = _ensure_non_empty_str(self.root_id, "root_id")
        root_type = _ensure_non_empty_str(self.root_type, "root_type")
        root_path = _ensure_non_empty_str(self.root_path, "root_path")

        if not self.portable:
            raise ValueError("portable must be True")

        if not self.relocation_ready:
            raise ValueError("relocation_ready must be True")

        object.__setattr__(self, "root_id", root_id)
        object.__setattr__(self, "root_type", root_type)
        object.__setattr__(self, "root_path", root_path)
