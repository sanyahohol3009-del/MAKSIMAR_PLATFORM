from __future__ import annotations

from MAKSIMAR_CORE_LIB.project_artifact_memory import (
    build_knowledge_base_contract,
    build_model_repository_contract,
    build_project_workspace_contract,
)


def test_phase_4_2_batch1_ready_smoke() -> None:
    models = build_model_repository_contract()
    knowledge = build_knowledge_base_contract()
    workspaces = build_project_workspace_contract()

    assert models.runtime_load_allowed_repositories == 0
    assert knowledge.runtime_write_allowed_knowledge_bases == 0
    assert workspaces.runtime_write_allowed_workspaces == 0

    assert models.read_only_repositories == models.total_repositories
    assert knowledge.read_only_knowledge_bases == knowledge.total_knowledge_bases
    assert workspaces.read_only_workspaces == workspaces.total_workspaces
