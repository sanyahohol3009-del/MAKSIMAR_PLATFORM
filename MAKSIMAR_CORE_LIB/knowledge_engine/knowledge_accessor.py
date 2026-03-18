from __future__ import annotations

from functools import lru_cache

from MAKSIMAR_CORE_LIB.knowledge_engine.knowledge_models import (
    KnowledgeObjectDefinition,
)
from MAKSIMAR_CORE_LIB.knowledge_engine.knowledge_registry import KnowledgeRegistry


@lru_cache(maxsize=1)
def _get_registry() -> KnowledgeRegistry:
    """Build cached knowledge registry."""
    registry = KnowledgeRegistry()
    registry.load_all()
    return registry


def get_knowledge_definition(object_id: str) -> KnowledgeObjectDefinition:
    """Get knowledge definition by id."""
    definition = _get_registry().get(object_id)
    if definition is None:
        raise KeyError(f"Knowledge definition not found: {object_id}")
    return definition


def list_knowledge_definitions() -> list[KnowledgeObjectDefinition]:
    """List all loaded knowledge definitions."""
    return _get_registry().list_all()
