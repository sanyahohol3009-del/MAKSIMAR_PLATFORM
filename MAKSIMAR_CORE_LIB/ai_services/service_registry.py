from __future__ import annotations

from MAKSIMAR_CORE_LIB.ai_services.service_loader import load_all_service_definitions
from MAKSIMAR_CORE_LIB.ai_services.service_models import AIServiceDefinition


class AIServiceRegistry:
    """In-memory registry of AI service definitions."""

    def __init__(self) -> None:
        self._definitions: dict[str, AIServiceDefinition] = {}

    def load_all(self) -> None:
        """Load all AI service definitions."""
        for result in load_all_service_definitions():
            if not result.is_valid or result.definition is None:
                continue

            definition = result.definition
            self._definitions[definition.service_id] = definition

    def get(self, service_id: str) -> AIServiceDefinition | None:
        """Get AI service definition by id."""
        return self._definitions.get(service_id)

    def list_all(self) -> list[AIServiceDefinition]:
        """List all loaded AI service definitions."""
        return list(self._definitions.values())
