from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.DATA_PLANE.data_plane_health import build_data_plane_health_read_model


def test_data_plane_health_reports_ready_when_required_paths_exist(tmp_path: Path) -> None:
    for rel_path in ("DATA_PLANE", "MAKSIMAR_CORE_LIB/data_plane", "MAKSIMAR_SERVER/DATA_PLANE"):
        (tmp_path / rel_path).mkdir(parents=True)

    health = build_data_plane_health_read_model(tmp_path)

    assert health.layer_id == "DATA_PLANE"
    assert health.status == "ready"
    assert health.health_ok is True
    assert health.missing_paths == ()


def test_data_plane_health_reports_degraded_when_paths_are_missing(tmp_path: Path) -> None:
    health = build_data_plane_health_read_model(tmp_path)

    assert health.status == "degraded"
    assert health.health_ok is False
    assert health.missing_paths
    assert health.dashboard_safe is True
