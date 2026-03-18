from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ProductDefinition:
    """Canonical product definition loaded from contracts."""

    product_id: str
    version: str
    file_path: Path
    payload: dict[str, Any]


@dataclass(slots=True)
class ProductLoadResult:
    """Result of loading one product definition."""

    definition: ProductDefinition | None
    is_valid: bool
    error: str | None = None
