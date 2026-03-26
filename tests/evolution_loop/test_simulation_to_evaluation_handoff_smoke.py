from __future__ import annotations

from MAKSIMAR_CORE_LIB.evaluation_integration import EvaluationIntent
from MAKSIMAR_CORE_LIB.evolution_loop import (
    build_simulation_to_evaluation_handoff,
)
from MAKSIMAR_CORE_LIB.simulation_integration import (
    SimulationIntent,
    build_simulation_execution_contract,
    build_simulation_execution_envelope,
)


def test_simulation_to_evaluation_handoff_builds() -> None:
    """Simulation-to-evaluation handoff should build successfully."""
    simulation_envelope = build_simulation_execution_envelope(
        SimulationIntent(query_text="simulate robot arm")
    )
    simulation_contract = build_simulation_execution_contract(simulation_envelope)

    handoff = build_simulation_to_evaluation_handoff(
        simulation_contract=simulation_contract,
        evaluation_intent=EvaluationIntent(query_text="evaluate simulation result"),
    )

    assert handoff.simulation_execution_id == simulation_contract.execution_id
    assert handoff.simulation_backend_id == simulation_contract.backend_id
    assert handoff.simulation_payload_ref == simulation_contract.payload_ref
    assert handoff.evaluation_id
    assert handoff.handoff_status == "linked"


def test_simulation_to_evaluation_handoff_respects_preferred_evaluation() -> None:
    """Simulation-to-evaluation handoff should respect explicit evaluation choice."""
    simulation_envelope = build_simulation_execution_envelope(
        SimulationIntent(
            query_text="simulate cartpole",
            preferred_backend="simulation_backend_pybullet",
        )
    )
    simulation_contract = build_simulation_execution_contract(simulation_envelope)

    handoff = build_simulation_to_evaluation_handoff(
        simulation_contract=simulation_contract,
        evaluation_intent=EvaluationIntent(
            query_text="evaluate code generation",
            preferred_evaluation="codegen_eval",
        ),
    )

    assert handoff.evaluation_id == "codegen_eval"
