from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.project_area_models import (
    SUPPORTED_PROJECT_AREAS,
)


def test_project_area_models_smoke() -> None:
    assert "runtime" in SUPPORTED_PROJECT_AREAS
    assert "memory" in SUPPORTED_PROJECT_AREAS
    assert "history_ingestion" in SUPPORTED_PROJECT_AREAS
    assert "storage" in SUPPORTED_PROJECT_AREAS
