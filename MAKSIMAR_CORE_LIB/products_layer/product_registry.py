from __future__ import annotations

from MAKSIMAR_CORE_LIB.products_layer.product_loader import load_all_product_definitions
from MAKSIMAR_CORE_LIB.products_layer.product_models import ProductDefinition


class ProductRegistry:
    """In-memory registry of product definitions."""

    def __init__(self) -> None:
        self._definitions: dict[str, ProductDefinition] = {}

    def load_all(self) -> None:
        """Load all product definitions."""
        for result in load_all_product_definitions():
            if not result.is_valid or result.definition is None:
                continue

            definition = result.definition
            self._definitions[definition.product_id] = definition

    def get(self, product_id: str) -> ProductDefinition | None:
        """Get product definition by id."""
        return self._definitions.get(product_id)

    def list_all(self) -> list[ProductDefinition]:
        """List all loaded product definitions."""
        return list(self._definitions.values())
