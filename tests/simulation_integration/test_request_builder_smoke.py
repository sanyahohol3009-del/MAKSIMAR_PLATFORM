from __future__ import annotations

from MAKSIMAR_CORE_LIB.simulation_integration import (
    SimulationIntent,
    build_simulation_request,
)


def test_build_simulation_request_uses_default_backend() -> None:
    """Simulation request builder should use first available backend by default."""
    request = build_simulation_request(
        SimulationIntent(query_text="simulate robot arm")
    )

    assert request.backend_id.startswith("simulation_backend_")
    assert request.version.endswith(".v1")
    assert request.source_definition_id.startswith("backend_")


def test_build_simulation_request_respects_preferred_backend() -> None:
    """Simulation request builder should respect explicit preferred backend."""
    request = build_simulation_request(
        SimulationIntent(
            query_text="simulate cartpole",
            preferred_backend="simulation_backend_pybullet",
        )
    )

    assert request.backend_id == "simulation_backend_pybullet"
