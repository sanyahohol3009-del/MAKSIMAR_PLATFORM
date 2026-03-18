from __future__ import annotations

from functools import lru_cache

from MAKSIMAR_CORE_LIB.runtime_base.runtime_models import RuntimeDocument
from MAKSIMAR_CORE_LIB.runtime_base.runtime_registry import RuntimeRegistry


@lru_cache(maxsize=1)
def _get_registry() -> RuntimeRegistry:
    """Build cached runtime registry."""
    registry = RuntimeRegistry()
    registry.load_all()
    return registry


def get_runtime_document(name: str) -> RuntimeDocument:
    """Get runtime document by name.

    Args:
        name: Logical runtime document name.

    Returns:
        Runtime document.

    Raises:
        KeyError: If runtime document is not found.
    """
    document = _get_registry().get(name)
    if document is None:
        raise KeyError(f"Runtime document not found: {name}")
    return document


def list_runtime_documents(root_name: str) -> list[RuntimeDocument]:
    """List runtime documents loaded from one root."""
    return _get_registry().get_by_root(root_name)
