from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ProductType = Literal[
    "manifest",
    "profile",
    "bundle",
    "deployment",
    "lifecycle",
    "branding",
    "feature_set",
]


@dataclass(frozen=True, slots=True)
class ProductQuery:
    """Canonical product query model."""

    query_text: str
    product_type: ProductType | None = None
    limit: int = 10


@dataclass(frozen=True, slots=True)
class ProductRetrievalItem:
    """Canonical product retrieval item."""

    product_id: str
    version: str
