from __future__ import annotations

import uuid

from MAKSIMAR_CORE_LIB.simulation_integration.request_builder import (
    build_simulation_request,
)
from MAKSIMAR_CORE_LIB.simulation_integration.request_models import (
    SimulationIntent,
)
from MAKSIMAR_CORE_LIB.simulation_integration.execution_models import (
    SimulationExecutionEnvelope,
)


def _generate_execution_id() -> str:
    """Generate unique execution id."""
    return f"sim_exec_{uuid.uuid4().hex}"


def build_simulation_execution_envelope(
    intent: SimulationIntent,
) -> SimulationExecutionEnvelope:
    """Build execution envelope from simulation intent."""
    request = build_simulation_request(intent)

    return SimulationExecutionEnvelope(
        request_text=request.request_text,
        backend_id=request.backend_id,
        version=request.version,
        source_definition_id=request.source_definition_id,
        execution_id=_generate_execution_id(),
        status="created",
    )
