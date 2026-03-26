from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SimulationIntent:
    """Raw simulation intent before integration-level normalization."""

    query_text: str
    preferred_backend: str | None = None


@dataclass(frozen=True, slots=True)
class SimulationIntegrationRequest:
    """Canonical simulation request built by integration layer."""

    request_text: str
    backend_id: str
    version: str
    source_definition_id: str
