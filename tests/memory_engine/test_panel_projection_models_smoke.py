from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.panel_projection_models import (
    PanelProjection,
)


def test_panel_projection_models_smoke() -> None:
    projection = PanelProjection(
        memory_id="ARCH-0001",
        title="Runtime truth path fixed",
        status="validated",
        truth_level="validated_project_fact",
        project_area=("runtime", "truth_feed"),
        affected_files=("CORE_ROOT/core_guard.py",),
        panel_ready=True,
    )

    assert projection.panel_ready is True
