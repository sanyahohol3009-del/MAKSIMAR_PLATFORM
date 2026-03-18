from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_executor.action_loader import load_all_action_definitions
from MAKSIMAR_CORE_LIB.action_executor.action_models import ActionDefinition


class ActionRegistry:
    """In-memory registry of action definitions."""

    def __init__(self) -> None:
        self._definitions: dict[str, ActionDefinition] = {}

    def load_all(self) -> None:
        """Load all action definitions."""
        for result in load_all_action_definitions():
            if not result.is_valid or result.definition is None:
                continue

            definition = result.definition
            self._definitions[definition.action_id] = definition

    def get(self, action_id: str) -> ActionDefinition | None:
        """Get action definition by id."""
        return self._definitions.get(action_id)

    def list_all(self) -> list[ActionDefinition]:
        """List all loaded action definitions."""
        return list(self._definitions.values())
