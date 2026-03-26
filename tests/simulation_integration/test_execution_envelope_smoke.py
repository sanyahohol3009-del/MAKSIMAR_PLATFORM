from __future__ import annotations

from MAKSIMAR_CORE_LIB.simulation_integration import (
    SimulationIntent,
    build_simulation_execution_envelope,
)


def test_execution_envelope_builds() -> None:
    """Execution envelope should be created correctly."""
    envelope = build_simulation_execution_envelope(
        SimulationIntent(query_text="simulate robot arm")
    )

    assert envelope.execution_id.startswith("sim_exec_")
    assert envelope.status == "created"
    assert envelope.backend_id.startswith("simulation_backend_")


def test_execution_envelope_respects_backend() -> None:
    """Execution envelope should respect preferred backend."""
    envelope = build_simulation_execution_envelope(
        SimulationIntent(
            query_text="simulate cartpole",
            preferred_backend="simulation_backend_pybullet",
        )
    )

    assert envelope.backend_id == "simulation_backend_pybullet"
