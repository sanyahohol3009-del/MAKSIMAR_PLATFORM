from __future__ import annotations

from MAKSIMAR_CORE_LIB.simulation_integration.backend_registry_summary import (
    build_simulation_backend_summary,
)
from MAKSIMAR_CORE_LIB.simulation_integration.request_models import (
    SimulationIntent,
    SimulationIntegrationRequest,
)


def _resolve_backend(
    intent: SimulationIntent,
) -> tuple[str, str, str]:
    """Resolve simulation backend from intent and backend registry."""
    summary = build_simulation_backend_summary()
    if not summary.records:
        raise RuntimeError("No simulation backends available.")

    if intent.preferred_backend is not None:
        for record in summary.records:
            if record.backend_id == intent.preferred_backend:
                return record.backend_id, record.version, record.source_definition_id

    record = summary.records[0]
    return record.backend_id, record.version, record.source_definition_id


def build_simulation_request(
    intent: SimulationIntent,
) -> SimulationIntegrationRequest:
    """Build canonical simulation integration request."""
    backend_id, version, source_definition_id = _resolve_backend(intent)

    return SimulationIntegrationRequest(
        request_text=intent.query_text,
        backend_id=backend_id,
        version=version,
        source_definition_id=source_definition_id,
    )
