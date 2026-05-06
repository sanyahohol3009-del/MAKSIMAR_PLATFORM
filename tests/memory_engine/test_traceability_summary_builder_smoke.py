from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.traceability_summary_builder import (
    build_traceability_projection_preview,
)


def test_traceability_summary_builder_smoke() -> None:
    preview = build_traceability_projection_preview(build_minimal_memory_object())
    assert preview["memory_id"] == "ARCH-0001"
