from __future__ import annotations

from functools import lru_cache

from MAKSIMAR_CORE_LIB.memory_engine.memory_models import MemoryEntityDefinition
from MAKSIMAR_CORE_LIB.memory_engine.memory_registry import MemoryRegistry


@lru_cache(maxsize=1)
def _get_registry() -> MemoryRegistry:
    """Build cached memory registry."""
    registry = MemoryRegistry()
    registry.load_all()
    return registry


def get_memory_definition(entity_id: str) -> MemoryEntityDefinition:
    """Get memory definition by id."""
    definition = _get_registry().get(entity_id)
    if definition is None:
        raise KeyError(f"Memory definition not found: {entity_id}")
    return definition


def list_memory_definitions() -> list[MemoryEntityDefinition]:
    """List all loaded memory definitions."""
    return _get_registry().list_all()
