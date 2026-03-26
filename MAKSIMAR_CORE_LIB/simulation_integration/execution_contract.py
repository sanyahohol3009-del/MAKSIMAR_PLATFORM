from __future__ import annotations

from MAKSIMAR_CORE_LIB.simulation_integration.execution_contract_models import (
    SimulationExecutionContract,
)
from MAKSIMAR_CORE_LIB.simulation_integration.execution_models import (
    SimulationExecutionEnvelope,
)


def _build_payload_ref(envelope: SimulationExecutionEnvelope) -> str:
    """Build stable payload reference for sandbox handoff."""
    return f"{envelope.execution_id}:{envelope.source_definition_id}"


def build_simulation_execution_contract(
    envelope: SimulationExecutionEnvelope,
) -> SimulationExecutionContract:
    """Build simulation execution contract as sandbox boundary."""
    return SimulationExecutionContract(
        execution_id=envelope.execution_id,
        backend_id=envelope.backend_id,
        source_definition_id=envelope.source_definition_id,
        payload_ref=_build_payload_ref(envelope),
        sandbox_required=True,
        network_access=False,
        write_to_core_allowed=False,
        status="ready_for_sandbox",
    )
