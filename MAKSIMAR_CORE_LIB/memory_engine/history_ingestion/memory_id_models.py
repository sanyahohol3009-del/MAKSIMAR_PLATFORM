from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Literal


MemoryIdPrefix = Literal[
    "ARCH",
    "INC",
    "ROADMAP",
    "HCHAT",
    "HMSG",
    "IMPORT",
    "HSTORE",
    "REL",
]

MEMORY_ID_PATTERN = re.compile(r"^[A-Z]+-\d{4}$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class MemoryObjectId:
    prefix: MemoryIdPrefix
    numeric_id: int
    value: str

    def __post_init__(self) -> None:
        if self.prefix not in (
            "ARCH",
            "INC",
            "ROADMAP",
            "HCHAT",
            "HMSG",
            "IMPORT",
            "HSTORE",
            "REL",
        ):
            raise ValueError("Unsupported memory id prefix")

        if self.numeric_id < 0:
            raise ValueError("numeric_id must be >= 0")

        value = _ensure_non_empty_str(self.value, "value")
        if not MEMORY_ID_PATTERN.match(value):
            raise ValueError("value must match MEMORY_ID_PATTERN")

        expected = f"{self.prefix}-{self.numeric_id:04d}"
        if value != expected:
            raise ValueError("value must match prefix and numeric_id")

        object.__setattr__(self, "value", value)
