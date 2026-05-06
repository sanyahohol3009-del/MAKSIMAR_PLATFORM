from __future__ import annotations

from dataclasses import dataclass
import re


STORAGE_NODE_ID_PATTERN = re.compile(r"^HSTORE-[A-Z]+-\d{3}$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class StorageNodeId:
    value: str

    def __post_init__(self) -> None:
        value = _ensure_non_empty_str(self.value, "value")
        if not STORAGE_NODE_ID_PATTERN.match(value):
            raise ValueError("value must match STORAGE_NODE_ID_PATTERN")
        object.__setattr__(self, "value", value)
