from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.project_artifact_memory.knowledge_base_models import (
    build_knowledge_base_contract,
)
from MAKSIMAR_CORE_LIB.project_artifact_memory.model_repository_models import (
    build_model_repository_contract,
)
from MAKSIMAR_CORE_LIB.project_artifact_memory.project_workspace_models import (
    build_project_workspace_contract,
)

ProjectArtifactBindingKind = Literal[
    "model_repository",
    "knowledge_base",
    "project_workspace",
]

_BINDING_ID_PATTERN = re.compile(r"^project_artifact_binding_[a-z][a-z0-9_]*_[0-9]{3}$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class ProjectArtifactBindingEntry:
    artifact_binding_id: str
    binding_kind: ProjectArtifactBindingKind
    source_entity_id: str
    storage_node_id: str
    artifact_ref: str
    artifact_namespace: str
    source_bound: bool
    storage_node_bound: bool
    versioned: bool
    read_only: bool
    dashboard_visible: bool
    retrieval_visible: bool
    runtime_load_allowed: bool
    runtime_write_allowed: bool
    runtime_execution_allowed: bool
    binding_ready: bool
    description: str

    def __post_init__(self) -> None:
        binding_id = _ensure_non_empty_str(self.artifact_binding_id, "artifact_binding_id")
        if not _BINDING_ID_PATTERN.fullmatch(binding_id):
            raise ValueError(f"Invalid artifact_binding_id: {binding_id}")

        for field_name in (
            "source_entity_id",
            "storage_node_id",
            "artifact_ref",
            "artifact_namespace",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "source_bound",
            "storage_node_bound",
            "versioned",
            "read_only",
            "dashboard_visible",
            "retrieval_visible",
            "runtime_load_allowed",
            "runtime_write_allowed",
            "runtime_execution_allowed",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.source_bound:
            raise ValueError("source_bound must be True")
        if not self.storage_node_bound:
            raise ValueError("storage_node_bound must be True")
        if not self.versioned:
            raise ValueError("versioned must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.dashboard_visible:
            raise ValueError("dashboard_visible must be True")
        if self.runtime_load_allowed:
            raise ValueError("runtime_load_allowed must be False in Batch 2")
        if self.runtime_write_allowed:
            raise ValueError("runtime_write_allowed must be False in Batch 2")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False in Batch 2")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")


@dataclass(frozen=True, slots=True)
class ProjectArtifactBindingContract:
    total_bindings: int
    ready_bindings: int
    source_bound_bindings: int
    storage_node_bound_bindings: int
    versioned_bindings: int
    read_only_bindings: int
    dashboard_visible_bindings: int
    retrieval_visible_bindings: int
    runtime_load_allowed_bindings: int
    runtime_write_allowed_bindings: int
    runtime_execution_allowed_bindings: int
    model_repository_bindings: int
    knowledge_base_bindings: int
    project_workspace_bindings: int
    entries: tuple[ProjectArtifactBindingEntry, ...]

    def __post_init__(self) -> None:
        if self.total_bindings != len(self.entries):
            raise ValueError("total_bindings must match entries length")
        if self.total_bindings <= 0:
            raise ValueError("total_bindings must be >= 1")

        expected = {
            "ready_bindings": sum(1 for entry in self.entries if entry.binding_ready),
            "source_bound_bindings": sum(1 for entry in self.entries if entry.source_bound),
            "storage_node_bound_bindings": sum(1 for entry in self.entries if entry.storage_node_bound),
            "versioned_bindings": sum(1 for entry in self.entries if entry.versioned),
            "read_only_bindings": sum(1 for entry in self.entries if entry.read_only),
            "dashboard_visible_bindings": sum(1 for entry in self.entries if entry.dashboard_visible),
            "retrieval_visible_bindings": sum(1 for entry in self.entries if entry.retrieval_visible),
            "runtime_load_allowed_bindings": sum(1 for entry in self.entries if entry.runtime_load_allowed),
            "runtime_write_allowed_bindings": sum(1 for entry in self.entries if entry.runtime_write_allowed),
            "runtime_execution_allowed_bindings": sum(1 for entry in self.entries if entry.runtime_execution_allowed),
            "model_repository_bindings": sum(1 for entry in self.entries if entry.binding_kind == "model_repository"),
            "knowledge_base_bindings": sum(1 for entry in self.entries if entry.binding_kind == "knowledge_base"),
            "project_workspace_bindings": sum(1 for entry in self.entries if entry.binding_kind == "project_workspace"),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_bindings != self.total_bindings:
            raise ValueError("all artifact bindings must be ready")
        if self.source_bound_bindings != self.total_bindings:
            raise ValueError("all artifact bindings must be source-bound")
        if self.storage_node_bound_bindings != self.total_bindings:
            raise ValueError("all artifact bindings must be storage-node-bound")
        if self.versioned_bindings != self.total_bindings:
            raise ValueError("all artifact bindings must be versioned")
        if self.read_only_bindings != self.total_bindings:
            raise ValueError("all artifact bindings must be read-only")
        if self.dashboard_visible_bindings != self.total_bindings:
            raise ValueError("all artifact bindings must be dashboard-visible")
        if self.runtime_load_allowed_bindings != 0:
            raise ValueError("runtime artifact/model loading must remain blocked")
        if self.runtime_write_allowed_bindings != 0:
            raise ValueError("runtime artifact writes must remain blocked")
        if self.runtime_execution_allowed_bindings != 0:
            raise ValueError("runtime artifact execution must remain blocked")


def build_project_artifact_binding_contract() -> ProjectArtifactBindingContract:
    models = build_model_repository_contract()
    knowledge = build_knowledge_base_contract()
    workspaces = build_project_workspace_contract()

    entries: list[ProjectArtifactBindingEntry] = []

    for model in models.entries:
        entries.append(
            ProjectArtifactBindingEntry(
                artifact_binding_id=model.model_repository_id.replace(
                    "model_repository_",
                    "project_artifact_binding_model_repository_",
                    1,
                ),
                binding_kind="model_repository",
                source_entity_id=model.model_repository_id,
                storage_node_id=model.storage_node_id,
                artifact_ref=model.artifact_ref,
                artifact_namespace=f"model_repository::{model.model_repository_kind}",
                source_bound=model.source_bound,
                storage_node_bound=True,
                versioned=model.versioned,
                read_only=model.read_only,
                dashboard_visible=model.dashboard_visible,
                retrieval_visible=model.retrieval_visible,
                runtime_load_allowed=model.runtime_load_allowed,
                runtime_write_allowed=False,
                runtime_execution_allowed=False,
                binding_ready=model.repository_ready,
                description=f"Read-only artifact binding for {model.model_repository_id}.",
            )
        )

    for item in knowledge.entries:
        entries.append(
            ProjectArtifactBindingEntry(
                artifact_binding_id=item.knowledge_base_id.replace(
                    "knowledge_base_",
                    "project_artifact_binding_knowledge_base_",
                    1,
                ),
                binding_kind="knowledge_base",
                source_entity_id=item.knowledge_base_id,
                storage_node_id=item.storage_node_id,
                artifact_ref=item.source_ref,
                artifact_namespace=f"knowledge_base::{item.knowledge_base_kind}",
                source_bound=item.source_bound,
                storage_node_bound=True,
                versioned=item.versioned,
                read_only=item.read_only,
                dashboard_visible=item.dashboard_visible,
                retrieval_visible=item.retrieval_enabled,
                runtime_load_allowed=False,
                runtime_write_allowed=item.runtime_write_allowed,
                runtime_execution_allowed=False,
                binding_ready=item.knowledge_base_ready,
                description=f"Read-only artifact binding for {item.knowledge_base_id}.",
            )
        )

    for workspace in workspaces.entries:
        entries.append(
            ProjectArtifactBindingEntry(
                artifact_binding_id=workspace.workspace_id.replace(
                    "project_workspace_",
                    "project_artifact_binding_project_workspace_",
                    1,
                ),
                binding_kind="project_workspace",
                source_entity_id=workspace.workspace_id,
                storage_node_id=workspace.storage_node_id,
                artifact_ref=workspace.project_root_ref,
                artifact_namespace=workspace.artifact_namespace,
                source_bound=workspace.source_bound,
                storage_node_bound=True,
                versioned=workspace.versioned,
                read_only=workspace.read_only,
                dashboard_visible=workspace.dashboard_visible,
                retrieval_visible=False,
                runtime_load_allowed=False,
                runtime_write_allowed=workspace.runtime_write_allowed,
                runtime_execution_allowed=False,
                binding_ready=workspace.workspace_ready,
                description=f"Read-only artifact binding for {workspace.workspace_id}.",
            )
        )

    contract_entries = tuple(entries)

    return ProjectArtifactBindingContract(
        total_bindings=len(contract_entries),
        ready_bindings=sum(1 for entry in contract_entries if entry.binding_ready),
        source_bound_bindings=sum(1 for entry in contract_entries if entry.source_bound),
        storage_node_bound_bindings=sum(1 for entry in contract_entries if entry.storage_node_bound),
        versioned_bindings=sum(1 for entry in contract_entries if entry.versioned),
        read_only_bindings=sum(1 for entry in contract_entries if entry.read_only),
        dashboard_visible_bindings=sum(1 for entry in contract_entries if entry.dashboard_visible),
        retrieval_visible_bindings=sum(1 for entry in contract_entries if entry.retrieval_visible),
        runtime_load_allowed_bindings=sum(1 for entry in contract_entries if entry.runtime_load_allowed),
        runtime_write_allowed_bindings=sum(1 for entry in contract_entries if entry.runtime_write_allowed),
        runtime_execution_allowed_bindings=sum(1 for entry in contract_entries if entry.runtime_execution_allowed),
        model_repository_bindings=sum(1 for entry in contract_entries if entry.binding_kind == "model_repository"),
        knowledge_base_bindings=sum(1 for entry in contract_entries if entry.binding_kind == "knowledge_base"),
        project_workspace_bindings=sum(1 for entry in contract_entries if entry.binding_kind == "project_workspace"),
        entries=contract_entries,
    )
