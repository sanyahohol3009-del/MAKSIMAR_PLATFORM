from __future__ import annotations

from MAKSIMAR_CORE_LIB.simulation_layer.simulation_loader import (
    load_all_simulation_definitions,
)
from MAKSIMAR_CORE_LIB.simulation_layer.simulation_models import (
    SimulationRequestDefinition,
)


class SimulationRegistry:
    """In-memory registry of simulation definitions."""

    def __init__(self) -> None:
        self._definitions: dict[str, SimulationRequestDefinition] = {}

    def load_all(self) -> None:
        """Load all simulation definitions."""
        for result in load_all_simulation_definitions():
            if not result.is_valid or result.definition is None:
                continue

            definition = result.definition
            self._definitions[definition.request_id] = definition

    def get(self, request_id: str) -> SimulationRequestDefinition | None:
        """Get simulation definition by id."""
        return self._definitions.get(request_id)

    def list_all(self) -> list[SimulationRequestDefinition]:
        """List all loaded simulation definitions."""
        return list(self._definitions.values())
