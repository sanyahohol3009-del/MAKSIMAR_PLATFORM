from __future__ import annotations

from MAKSIMAR_CORE_LIB.knowledge_engine.knowledge_loader import (
    load_all_knowledge_definitions,
)
from MAKSIMAR_CORE_LIB.knowledge_engine.knowledge_models import (
    KnowledgeObjectDefinition,
)


class KnowledgeRegistry:
    """In-memory registry of knowledge definitions."""

    def __init__(self) -> None:
        self._definitions: dict[str, KnowledgeObjectDefinition] = {}

    def load_all(self) -> None:
        """Load all knowledge definitions."""
        for result in load_all_knowledge_definitions():
            if not result.is_valid or result.definition is None:
                continue

            definition = result.definition
            self._definitions[definition.object_id] = definition

    def get(self, object_id: str) -> KnowledgeObjectDefinition | None:
        """Get knowledge definition by id."""
        return self._definitions.get(object_id)

    def list_all(self) -> list[KnowledgeObjectDefinition]:
        """List all loaded knowledge definitions."""
        return list(self._definitions.values())
