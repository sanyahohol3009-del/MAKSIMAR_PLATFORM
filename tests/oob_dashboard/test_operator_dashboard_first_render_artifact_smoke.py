from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_first_render_artifact import (
    build_operator_dashboard_first_render_artifact,
    write_operator_dashboard_first_render_artifact,
)


def test_operator_dashboard_first_render_artifact_builds() -> None:
    """First operator render artifact should build successfully."""
    artifact = build_operator_dashboard_first_render_artifact()

    assert artifact.artifact_id == "operator_dashboard_first_render_artifact_001"
    assert artifact.dashboard_id == "dashboard_main_operator_001"
    assert artifact.workspace_id == "workspace_operator_main"
    assert artifact.output_path == "SANDBOX/operator_dashboard_first_render_artifact.html"
    assert artifact.title == "MAKSIMAR Operator Screen"


def test_operator_dashboard_first_render_artifact_contains_truthful_screen_markers() -> None:
    """First operator render artifact should contain visible truthful screen content."""
    artifact = build_operator_dashboard_first_render_artifact()

    assert "MAKSIMAR Operator Screen" in artifact.html
    assert "System Health" in artifact.html
    assert "Main Workspace / Operator Core" in artifact.html
    assert "Explain Panel" in artifact.html
    assert "Command Strip" in artifact.html
    assert "truthful_live_operator_screen" in artifact.html
    assert "render_surface_workspace_operator_main_001" in artifact.html


def test_operator_dashboard_first_render_artifact_write_to_disk(tmp_path: Path) -> None:
    """First operator render artifact should be writable to disk."""
    output_path = tmp_path / "operator_dashboard_first_render_artifact.html"
    written_path = write_operator_dashboard_first_render_artifact(output_path)

    assert written_path.exists()
    content = written_path.read_text(encoding="utf-8")
    assert "MAKSIMAR Operator Screen" in content
    assert "Sidebar" in content
    assert "Bottom Summary" in content


def test_operator_dashboard_first_render_artifact_contains_visual_payload_values() -> None:
    """First operator render artifact should expose visual payload values."""
    artifact = build_operator_dashboard_first_render_artifact()

    assert "Topology" in artifact.html
    assert "Signals" in artifact.html
    assert "Explainability" in artifact.html
    assert "Ticker" in artifact.html
