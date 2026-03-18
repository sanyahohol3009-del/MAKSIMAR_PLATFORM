from __future__ import annotations

from functools import lru_cache

from MAKSIMAR_CORE_LIB.simulation_layer.simulation_models import (
    SimulationRequestDefinition,
)
from MAKSIMAR_CORE_LIB.simulation_layer.simulation_registry import SimulationRegistry


@lru_cache(maxsize=1)
def _get_registry() -> SimulationRegistry:
    """Build cached simulation registry."""
    registry = SimulationRegistry()
    registry.load_all()
    return registry


def get_simulation_definition(request_id: str) -> SimulationRequestDefinition:
    """Get simulation definition by id."""
    definition = _get_registry().get(request_id)
    if definition is None:
        raise KeyError(f"Simulation definition not found: {request_id}")
    return definition


def list_simulation_definitions() -> list[SimulationRequestDefinition]:
    """List all loaded simulation definitions."""
    return _get_registry().list_all()
