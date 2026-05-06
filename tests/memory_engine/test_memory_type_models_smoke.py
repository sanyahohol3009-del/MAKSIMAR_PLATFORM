from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_type_models import (
    SUPPORTED_MEMORY_TYPES,
)


def test_memory_type_models_smoke() -> None:
    assert "architecture_decision" in SUPPORTED_MEMORY_TYPES
    assert "incident" in SUPPORTED_MEMORY_TYPES
    assert "roadmap_checkpoint" in SUPPORTED_MEMORY_TYPES
    assert "storage_node" in SUPPORTED_MEMORY_TYPES
