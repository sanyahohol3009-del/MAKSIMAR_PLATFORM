from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ConfigValueType = Literal[
    "string",
    "integer",
    "boolean",
]

ConfigScope = Literal[
    "runtime",
    "feature_flag",
    "environment",
]


@dataclass(frozen=True, slots=True)
class TypedConfigEntry:
    """One typed config boundary entry."""

    key: str
    value_type: ConfigValueType
    scope: ConfigScope
    required: bool


@dataclass(frozen=True, slots=True)
class TypedConfigBoundaryContract:
    """Unified typed config boundary contract."""

    total_entries: int
    entries: tuple[TypedConfigEntry, ...]
