from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.filter_projection_models import (
    FilterProjection,
)


def test_filter_projection_models_smoke() -> None:
    projection = FilterProjection(
        memory_id="ARCH-0001",
        status="validated",
        truth_level="validated_project_fact",
        tags=("runtime", "truth"),
        project_area=("runtime", "truth_feed"),
        filter_ready=True,
    )

    assert projection.filter_ready is True
