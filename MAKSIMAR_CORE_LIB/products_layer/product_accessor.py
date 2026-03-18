from __future__ import annotations

from functools import lru_cache

from MAKSIMAR_CORE_LIB.products_layer.product_models import ProductDefinition
from MAKSIMAR_CORE_LIB.products_layer.product_registry import ProductRegistry


@lru_cache(maxsize=1)
def _get_registry() -> ProductRegistry:
    """Build cached product registry."""
    registry = ProductRegistry()
    registry.load_all()
    return registry


def get_product_definition(product_id: str) -> ProductDefinition:
    """Get product definition by id."""
    definition = _get_registry().get(product_id)
    if definition is None:
        raise KeyError(f"Product definition not found: {product_id}")
    return definition


def list_product_definitions() -> list[ProductDefinition]:
    """List all loaded product definitions."""
    return _get_registry().list_all()
