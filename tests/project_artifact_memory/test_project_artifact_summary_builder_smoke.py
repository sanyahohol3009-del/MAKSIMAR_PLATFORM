from __future__ import annotations

from MAKSIMAR_CORE_LIB.project_artifact_memory import build_project_artifact_summary


def test_project_artifact_summary_builder_smoke() -> None:
    summary = build_project_artifact_summary()

    assert summary["summary_ready"] is True
    assert summary["model_repositories"] == 2
    assert summary["knowledge_bases"] == 3
    assert summary["project_workspaces"] == 3
    assert summary["artifact_bindings"] == 8
    assert summary["runtime_surface_allowed"] == 0
    assert summary["runtime_load_allowed_bindings"] == 0
    assert summary["runtime_write_allowed_bindings"] == 0
    assert summary["runtime_execution_allowed_bindings"] == 0
