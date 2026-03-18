from __future__ import annotations

from functools import lru_cache

from MAKSIMAR_CORE_LIB.action_executor.action_models import ActionDefinition
from MAKSIMAR_CORE_LIB.action_executor.action_registry import ActionRegistry


@lru_cache(maxsize=1)
def _get_registry() -> ActionRegistry:
    """Build cached action registry."""
    registry = ActionRegistry()
    registry.load_all()
    return registry


def get_action_definition(action_id: str) -> ActionDefinition:
    """Get action definition by id."""
    definition = _get_registry().get(action_id)
    if definition is None:
        raise KeyError(f"Action definition not found: {action_id}")
    return definition


def list_action_definitions() -> list[ActionDefinition]:
    """List all loaded action definitions."""
    return _get_registry().list_all()
