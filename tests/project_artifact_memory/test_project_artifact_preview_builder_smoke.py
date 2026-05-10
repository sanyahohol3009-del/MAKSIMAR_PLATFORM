from __future__ import annotations

from MAKSIMAR_CORE_LIB.project_artifact_memory import build_project_artifact_preview


def test_project_artifact_preview_builder_smoke() -> None:
    preview = build_project_artifact_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["model_repositories"] == 2
    assert preview["knowledge_bases"] == 3
    assert preview["project_workspaces"] == 3
    assert preview["artifact_bindings"] == 8
    assert preview["runtime_surface_allowed"] == 0
    assert len(preview["artifact_binding_ids"]) == 8
