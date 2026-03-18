from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.products_layer.product_models import ProductDefinition
from MAKSIMAR_CORE_LIB.products_layer.query_models import (
    ProductQuery,
    ProductRetrievalItem,
)


@dataclass(slots=True)
class ProductRetrievalSummary:
    """Aggregated summary for one product retrieval request."""

    query_text: str
    total_matches: int
    returned_items: list[ProductRetrievalItem]


def build_product_summary(
    query: ProductQuery,
    definitions: list[ProductDefinition],
) -> ProductRetrievalSummary:
    """Build retrieval summary from loaded product definitions.

    Current matching model:
    - match if query text is contained in product_id
    - limit output by query.limit
    """
    normalized_query = query.query_text.strip().lower()

    matches = [
        definition
        for definition in definitions
        if normalized_query in definition.product_id.lower()
    ]

    limited_matches = matches[: query.limit]

    returned_items = [
        ProductRetrievalItem(
            product_id=definition.product_id,
            version=definition.version,
        )
        for definition in limited_matches
    ]

    return ProductRetrievalSummary(
        query_text=query.query_text,
        total_matches=len(matches),
        returned_items=returned_items,
    )
