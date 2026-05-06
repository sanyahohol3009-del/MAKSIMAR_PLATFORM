from __future__ import annotations

from dataclasses import dataclass
import re


RELATION_ID_PATTERN = re.compile(r"^REL-\d{4}$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class RelationId:
    value: str

    def __post_init__(self) -> None:
        value = _ensure_non_empty_str(self.value, "value")
        if not RELATION_ID_PATTERN.match(value):
            raise ValueError("value must match RELATION_ID_PATTERN")
        object.__setattr__(self, "value", value)
