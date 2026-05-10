from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.project_artifact_memory.knowledge_base_models import (
    build_knowledge_base_contract,
)
from MAKSIMAR_CORE_LIB.project_artifact_memory.model_repository_models import (
    build_model_repository_contract,
)
from MAKSIMAR_CORE_LIB.project_artifact_memory.project_artifact_binding_models import (
    build_project_artifact_binding_contract,
)
from MAKSIMAR_CORE_LIB.project_artifact_memory.project_artifact_preview_builder import (
    build_project_artifact_preview,
)
from MAKSIMAR_CORE_LIB.project_artifact_memory.project_artifact_summary_builder import (
    build_project_artifact_summary,
)
from MAKSIMAR_CORE_LIB.project_artifact_memory.project_workspace_models import (
    build_project_workspace_contract,
)


_FORBIDDEN_ARTIFACT_RUNTIME_ROOTS = (
    "runtime_artifact_writer",
    "canonical_artifact_writer",
    "direct_canonical_artifact_writer",
    "artifact_runtime_executor",
    "model_runtime_loader",
)


@dataclass(frozen=True, slots=True)
class ProjectArtifactPhaseReadiness:
    model_repositories: int
    knowledge_bases: int
    project_workspaces: int
    artifact_bindings: int
    model_repository_bindings: int
    knowledge_base_bindings: int
    project_workspace_bindings: int
    retrieval_visible_bindings: int
    flow: Tuple[str, ...]
    model_repository_ready: bool
    knowledge_base_ready: bool
    project_workspace_ready: bool
    artifact_binding_ready: bool
    source_bound_ready: bool
    storage_node_bound_ready: bool
    versioned_ready: bool
    read_only_ready: bool
    dashboard_visible_ready: bool
    no_runtime_load: bool
    no_runtime_write: bool
    no_runtime_execution: bool
    no_runtime_surface: bool
    no_direct_canonical_write: bool
    artifact_write_approval_gate_required: bool
    sandbox_staging_only_future_write_path: bool
    no_forbidden_artifact_runtime_roots: bool
    phase_ready: bool


def _no_forbidden_artifact_runtime_roots() -> bool:
    return not any(Path(root_name).exists() for root_name in _FORBIDDEN_ARTIFACT_RUNTIME_ROOTS)


def build_project_artifact_phase_readiness() -> ProjectArtifactPhaseReadiness:
    models = build_model_repository_contract()
    knowledge = build_knowledge_base_contract()
    workspaces = build_project_workspace_contract()
    bindings = build_project_artifact_binding_contract()
    summary = build_project_artifact_summary()
    preview = build_project_artifact_preview()

    model_repository_ready = models.ready_repositories == models.total_repositories
    knowledge_base_ready = knowledge.ready_knowledge_bases == knowledge.total_knowledge_bases
    project_workspace_ready = workspaces.ready_workspaces == workspaces.total_workspaces
    artifact_binding_ready = bindings.ready_bindings == bindings.total_bindings

    source_bound_ready = bindings.source_bound_bindings == bindings.total_bindings
    storage_node_bound_ready = bindings.storage_node_bound_bindings == bindings.total_bindings
    versioned_ready = bindings.versioned_bindings == bindings.total_bindings
    read_only_ready = bindings.read_only_bindings == bindings.total_bindings
    dashboard_visible_ready = bindings.dashboard_visible_bindings == bindings.total_bindings

    no_runtime_load = int(summary["runtime_load_allowed_bindings"]) == 0
    no_runtime_write = int(summary["runtime_write_allowed_bindings"]) == 0
    no_runtime_execution = int(summary["runtime_execution_allowed_bindings"]) == 0
    no_runtime_surface = int(summary["runtime_surface_allowed"]) == 0

    no_forbidden_artifact_runtime_roots = _no_forbidden_artifact_runtime_roots()

    artifact_write_approval_gate_required = True
    sandbox_staging_only_future_write_path = True
    no_direct_canonical_write = (
        no_runtime_write
        and no_runtime_execution
        and no_forbidden_artifact_runtime_roots
        and artifact_write_approval_gate_required
        and sandbox_staging_only_future_write_path
    )

    phase_ready = (
        bool(summary["summary_ready"])
        and bool(preview["preview_ready"])
        and model_repository_ready
        and knowledge_base_ready
        and project_workspace_ready
        and artifact_binding_ready
        and source_bound_ready
        and storage_node_bound_ready
        and versioned_ready
        and read_only_ready
        and dashboard_visible_ready
        and no_runtime_load
        and no_runtime_write
        and no_runtime_execution
        and no_runtime_surface
        and no_direct_canonical_write
        and artifact_write_approval_gate_required
        and sandbox_staging_only_future_write_path
        and no_forbidden_artifact_runtime_roots
    )

    return ProjectArtifactPhaseReadiness(
        model_repositories=models.total_repositories,
        knowledge_bases=knowledge.total_knowledge_bases,
        project_workspaces=workspaces.total_workspaces,
        artifact_bindings=bindings.total_bindings,
        model_repository_bindings=bindings.model_repository_bindings,
        knowledge_base_bindings=bindings.knowledge_base_bindings,
        project_workspace_bindings=bindings.project_workspace_bindings,
        retrieval_visible_bindings=bindings.retrieval_visible_bindings,
        flow=tuple(str(item) for item in preview["flow"]),
        model_repository_ready=model_repository_ready,
        knowledge_base_ready=knowledge_base_ready,
        project_workspace_ready=project_workspace_ready,
        artifact_binding_ready=artifact_binding_ready,
        source_bound_ready=source_bound_ready,
        storage_node_bound_ready=storage_node_bound_ready,
        versioned_ready=versioned_ready,
        read_only_ready=read_only_ready,
        dashboard_visible_ready=dashboard_visible_ready,
        no_runtime_load=no_runtime_load,
        no_runtime_write=no_runtime_write,
        no_runtime_execution=no_runtime_execution,
        no_runtime_surface=no_runtime_surface,
        no_direct_canonical_write=no_direct_canonical_write,
        artifact_write_approval_gate_required=artifact_write_approval_gate_required,
        sandbox_staging_only_future_write_path=sandbox_staging_only_future_write_path,
        no_forbidden_artifact_runtime_roots=no_forbidden_artifact_runtime_roots,
        phase_ready=phase_ready,
    )


def build_project_artifact_phase_preview() -> Dict[str, object]:
    readiness = build_project_artifact_phase_readiness()

    return {
        "flow": readiness.flow,
        "preview_ready": readiness.phase_ready,
        "phase_ready": readiness.phase_ready,
        "model_repositories": readiness.model_repositories,
        "knowledge_bases": readiness.knowledge_bases,
        "project_workspaces": readiness.project_workspaces,
        "artifact_bindings": readiness.artifact_bindings,
        "model_repository_bindings": readiness.model_repository_bindings,
        "knowledge_base_bindings": readiness.knowledge_base_bindings,
        "project_workspace_bindings": readiness.project_workspace_bindings,
        "retrieval_visible_bindings": readiness.retrieval_visible_bindings,
        "model_repository_ready": readiness.model_repository_ready,
        "knowledge_base_ready": readiness.knowledge_base_ready,
        "project_workspace_ready": readiness.project_workspace_ready,
        "artifact_binding_ready": readiness.artifact_binding_ready,
        "source_bound_ready": readiness.source_bound_ready,
        "storage_node_bound_ready": readiness.storage_node_bound_ready,
        "versioned_ready": readiness.versioned_ready,
        "read_only_ready": readiness.read_only_ready,
        "dashboard_visible_ready": readiness.dashboard_visible_ready,
        "no_runtime_load": readiness.no_runtime_load,
        "no_runtime_write": readiness.no_runtime_write,
        "no_runtime_execution": readiness.no_runtime_execution,
        "no_runtime_surface": readiness.no_runtime_surface,
        "no_direct_canonical_write": readiness.no_direct_canonical_write,
        "artifact_write_approval_gate_required": readiness.artifact_write_approval_gate_required,
        "sandbox_staging_only_future_write_path": readiness.sandbox_staging_only_future_write_path,
        "no_forbidden_artifact_runtime_roots": readiness.no_forbidden_artifact_runtime_roots,
    }
