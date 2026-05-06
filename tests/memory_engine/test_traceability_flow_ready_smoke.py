from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.traceability_summary_builder import (
    build_traceability_projection,
)


def test_traceability_flow_ready_smoke() -> None:
    projection = build_traceability_projection(build_minimal_memory_object())
    assert projection.traceability_ready is True
