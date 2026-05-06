from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_status_models import (
    SUPPORTED_MEMORY_STATUSES,
)


def test_memory_status_models_smoke() -> None:
    assert SUPPORTED_MEMORY_STATUSES == ("draft", "validated", "deprecated")
