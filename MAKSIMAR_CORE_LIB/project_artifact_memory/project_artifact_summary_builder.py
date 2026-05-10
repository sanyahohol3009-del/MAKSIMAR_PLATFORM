from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.project_artifact_memory.knowledge_base_models import (
    build_knowledge_base_contract,
)
from MAKSIMAR_CORE_LIB.project_artifact_memory.model_repository_models import (
    build_model_repository_contract,
)
from MAKSIMAR_CORE_LIB.project_artifact_memory.project_artifact_binding_models import (
    build_project_artifact_binding_contract,
)
from MAKSIMAR_CORE_LIB.project_artifact_memory.project_workspace_models import (
    build_project_workspace_contract,
)


def build_project_artifact_summary() -> Dict[str, object]:
    models = build_model_repository_contract()
    knowledge = build_knowledge_base_contract()
    workspaces = build_project_workspace_contract()
    bindings = build_project_artifact_binding_contract()

    runtime_surface_allowed = (
        models.runtime_load_allowed_repositories
        + knowledge.runtime_write_allowed_knowledge_bases
        + workspaces.runtime_write_allowed_workspaces
        + bindings.runtime_load_allowed_bindings
        + bindings.runtime_write_allowed_bindings
        + bindings.runtime_execution_allowed_bindings
    )

    summary_ready = (
        models.ready_repositories == models.total_repositories
        and knowledge.ready_knowledge_bases == knowledge.total_knowledge_bases
        and workspaces.ready_workspaces == workspaces.total_workspaces
        and bindings.ready_bindings == bindings.total_bindings
        and bindings.model_repository_bindings == models.total_repositories
        and bindings.knowledge_base_bindings == knowledge.total_knowledge_bases
        and bindings.project_workspace_bindings == workspaces.total_workspaces
        and bindings.source_bound_bindings == bindings.total_bindings
        and bindings.storage_node_bound_bindings == bindings.total_bindings
        and bindings.versioned_bindings == bindings.total_bindings
        and bindings.read_only_bindings == bindings.total_bindings
        and runtime_surface_allowed == 0
    )

    return {
        "model_repositories": models.total_repositories,
        "model_ready_repositories": models.ready_repositories,
        "knowledge_bases": knowledge.total_knowledge_bases,
        "knowledge_ready_bases": knowledge.ready_knowledge_bases,
        "project_workspaces": workspaces.total_workspaces,
        "project_ready_workspaces": workspaces.ready_workspaces,
        "artifact_bindings": bindings.total_bindings,
        "artifact_ready_bindings": bindings.ready_bindings,
        "model_repository_bindings": bindings.model_repository_bindings,
        "knowledge_base_bindings": bindings.knowledge_base_bindings,
        "project_workspace_bindings": bindings.project_workspace_bindings,
        "source_bound_bindings": bindings.source_bound_bindings,
        "storage_node_bound_bindings": bindings.storage_node_bound_bindings,
        "versioned_bindings": bindings.versioned_bindings,
        "read_only_bindings": bindings.read_only_bindings,
        "dashboard_visible_bindings": bindings.dashboard_visible_bindings,
        "retrieval_visible_bindings": bindings.retrieval_visible_bindings,
        "runtime_surface_allowed": runtime_surface_allowed,
        "runtime_load_allowed_bindings": bindings.runtime_load_allowed_bindings,
        "runtime_write_allowed_bindings": bindings.runtime_write_allowed_bindings,
        "runtime_execution_allowed_bindings": bindings.runtime_execution_allowed_bindings,
        "summary_ready": summary_ready,
    }
