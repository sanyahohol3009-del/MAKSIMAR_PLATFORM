from __future__ import annotations

from MAKSIMAR_CORE_LIB.evaluation_integration import (
    EvaluationIntent,
    build_evaluation_execution_envelope,
)
from MAKSIMAR_CORE_LIB.evolution_loop.handoff_models import (
    SimulationEvaluationHandoff,
)
from MAKSIMAR_CORE_LIB.simulation_integration import (
    SimulationExecutionContract,
)


def build_simulation_to_evaluation_handoff(
    simulation_contract: SimulationExecutionContract,
    evaluation_intent: EvaluationIntent,
) -> SimulationEvaluationHandoff:
    """Build canonical handoff from simulation execution to evaluation."""
    evaluation_envelope = build_evaluation_execution_envelope(evaluation_intent)

    return SimulationEvaluationHandoff(
        simulation_execution_id=simulation_contract.execution_id,
        simulation_backend_id=simulation_contract.backend_id,
        simulation_payload_ref=simulation_contract.payload_ref,
        evaluation_execution_id=evaluation_envelope.execution_id,
        evaluation_id=evaluation_envelope.evaluation_id,
        handoff_status="linked",
    )
