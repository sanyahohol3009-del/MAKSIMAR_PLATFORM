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
from MAKSIMAR_CORE_LIB.project_artifact_memory.project_artifact_summary_builder import (
    build_project_artifact_summary,
)
from MAKSIMAR_CORE_LIB.project_artifact_memory.project_workspace_models import (
    build_project_workspace_contract,
)


_PROJECT_ARTIFACT_PREVIEW_FLOW = (
    "model_repository",
    "knowledge_base",
    "project_workspace",
    "project_artifact_binding",
    "project_artifact_summary",
    "project_artifact_preview",
)


def build_project_artifact_preview() -> Dict[str, object]:
    models = build_model_repository_contract()
    knowledge = build_knowledge_base_contract()
    workspaces = build_project_workspace_contract()
    bindings = build_project_artifact_binding_contract()
    summary = build_project_artifact_summary()

    return {
        "flow": _PROJECT_ARTIFACT_PREVIEW_FLOW,
        "preview_ready": bool(summary["summary_ready"]),
        "summary_ready": summary["summary_ready"],
        "model_repositories": summary["model_repositories"],
        "knowledge_bases": summary["knowledge_bases"],
        "project_workspaces": summary["project_workspaces"],
        "artifact_bindings": summary["artifact_bindings"],
        "model_repository_bindings": summary["model_repository_bindings"],
        "knowledge_base_bindings": summary["knowledge_base_bindings"],
        "project_workspace_bindings": summary["project_workspace_bindings"],
        "source_bound_bindings": summary["source_bound_bindings"],
        "storage_node_bound_bindings": summary["storage_node_bound_bindings"],
        "versioned_bindings": summary["versioned_bindings"],
        "read_only_bindings": summary["read_only_bindings"],
        "dashboard_visible_bindings": summary["dashboard_visible_bindings"],
        "retrieval_visible_bindings": summary["retrieval_visible_bindings"],
        "runtime_surface_allowed": summary["runtime_surface_allowed"],
        "runtime_load_allowed_bindings": summary["runtime_load_allowed_bindings"],
        "runtime_write_allowed_bindings": summary["runtime_write_allowed_bindings"],
        "runtime_execution_allowed_bindings": summary["runtime_execution_allowed_bindings"],
        "model_repository_ids": tuple(entry.model_repository_id for entry in models.entries),
        "knowledge_base_ids": tuple(entry.knowledge_base_id for entry in knowledge.entries),
        "workspace_ids": tuple(entry.workspace_id for entry in workspaces.entries),
        "artifact_binding_ids": tuple(entry.artifact_binding_id for entry in bindings.entries),
        "artifact_namespaces": tuple(entry.artifact_namespace for entry in bindings.entries),
    }
