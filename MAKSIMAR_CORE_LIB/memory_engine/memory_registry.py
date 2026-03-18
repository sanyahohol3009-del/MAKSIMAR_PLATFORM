from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.memory_loader import load_all_memory_definitions
from MAKSIMAR_CORE_LIB.memory_engine.memory_models import MemoryEntityDefinition


class MemoryRegistry:
    """In-memory registry of memory definitions."""

    def __init__(self) -> None:
        self._definitions: dict[str, MemoryEntityDefinition] = {}

    def load_all(self) -> None:
        """Load all memory definitions."""
        for result in load_all_memory_definitions():
            if not result.is_valid or result.definition is None:
                continue

            definition = result.definition
            self._definitions[definition.entity_id] = definition

    def get(self, entity_id: str) -> MemoryEntityDefinition | None:
        """Get memory definition by id."""
        return self._definitions.get(entity_id)

    def list_all(self) -> list[MemoryEntityDefinition]:
        """List all loaded memory definitions."""
        return list(self._definitions.values())
