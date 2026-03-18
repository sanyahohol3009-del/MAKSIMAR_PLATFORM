from __future__ import annotations

from functools import lru_cache

from MAKSIMAR_CORE_LIB.ai_services.service_models import AIServiceDefinition
from MAKSIMAR_CORE_LIB.ai_services.service_registry import AIServiceRegistry


@lru_cache(maxsize=1)
def _get_registry() -> AIServiceRegistry:
    """Build cached AI service registry."""
    registry = AIServiceRegistry()
    registry.load_all()
    return registry


def get_service_definition(service_id: str) -> AIServiceDefinition:
    """Get AI service definition by id."""
    definition = _get_registry().get(service_id)
    if definition is None:
        raise KeyError(f"AI service definition not found: {service_id}")
    return definition


def list_service_definitions() -> list[AIServiceDefinition]:
    """List all loaded AI service definitions."""
    return _get_registry().list_all()
