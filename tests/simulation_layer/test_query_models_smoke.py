from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.simulation_layer.query_models import SimulationQuery
from MAKSIMAR_CORE_LIB.simulation_layer.simulation_models import (
    SimulationRequestDefinition,
)
from MAKSIMAR_CORE_LIB.simulation_layer.simulation_summary import (
    build_simulation_summary,
)


def test_build_simulation_summary_matches_request_ids() -> None:
    """Retrieval summary should match by request_id substring."""
    definitions = [
        SimulationRequestDefinition(
            request_id="simulation_request",
            version="simulation_request.v1",
            file_path=Path("simulation_request.v1.yaml"),
            payload={},
        ),
        SimulationRequestDefinition(
            request_id="simulation_result",
            version="simulation_result.v1",
            file_path=Path("simulation_result.v1.yaml"),
            payload={},
        ),
    ]

    query = SimulationQuery(query_text="request", limit=10)
    summary = build_simulation_summary(query, definitions)

    assert summary.total_matches == 1
    assert len(summary.returned_items) == 1
    assert summary.returned_items[0].request_id == "simulation_request"


def test_build_simulation_summary_respects_limit() -> None:
    """Retrieval summary should respect query limit."""
    definitions = [
        SimulationRequestDefinition(
            request_id="simulation_request",
            version="simulation_request.v1",
            file_path=Path("simulation_request.v1.yaml"),
            payload={},
        ),
        SimulationRequestDefinition(
            request_id="simulation_result",
            version="simulation_result.v1",
            file_path=Path("simulation_result.v1.yaml"),
            payload={},
        ),
    ]

    query = SimulationQuery(query_text="simulation", limit=1)
    summary = build_simulation_summary(query, definitions)

    assert summary.total_matches == 2
    assert len(summary.returned_items) == 1
