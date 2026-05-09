from __future__ import annotations

from pathlib import Path


def test_dashboard_read_only_views_no_core_visualization_layer_smoke() -> None:
    assert not Path("MAKSIMAR_CORE_LIB/memory_engine/visualization_read_models").exists()
