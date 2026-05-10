from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

ProjectWorkspaceKind = Literal["robotics", "cad_3d", "energy"]

_WORKSPACE_ID_PATTERN = re.compile(r"^project_workspace_[a-z][a-z0-9_]*_[0-9]{3}$")


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
class ProjectWorkspaceEntry:
    workspace_id: str
    workspace_kind: ProjectWorkspaceKind
    storage_node_id: str
    project_root_ref: str
    artifact_namespace: str
    source_bound: bool
    versioned: bool
    read_only: bool
    runtime_write_allowed: bool
    dashboard_visible: bool
    workspace_ready: bool
    description: str

    def __post_init__(self) -> None:
        workspace_id = _ensure_non_empty_str(self.workspace_id, "workspace_id")
        if not _WORKSPACE_ID_PATTERN.fullmatch(workspace_id):
            raise ValueError(f"Invalid workspace_id: {workspace_id}")

        for field_name in (
            "storage_node_id",
            "project_root_ref",
            "artifact_namespace",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "source_bound",
            "versioned",
            "read_only",
            "runtime_write_allowed",
            "dashboard_visible",
            "workspace_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.source_bound:
            raise ValueError("source_bound must be True")
        if not self.versioned:
            raise ValueError("versioned must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.runtime_write_allowed:
            raise ValueError("runtime_write_allowed must be False in Batch 1")
        if not self.dashboard_visible:
            raise ValueError("dashboard_visible must be True")
        if not self.workspace_ready:
            raise ValueError("workspace_ready must be True")


@dataclass(frozen=True, slots=True)
class ProjectWorkspaceContract:
    total_workspaces: int
    ready_workspaces: int
    source_bound_workspaces: int
    versioned_workspaces: int
    read_only_workspaces: int
    runtime_write_allowed_workspaces: int
    dashboard_visible_workspaces: int
    entries: tuple[ProjectWorkspaceEntry, ...]

    def __post_init__(self) -> None:
        if self.total_workspaces != len(self.entries):
            raise ValueError("total_workspaces must match entries length")
        if self.total_workspaces <= 0:
            raise ValueError("total_workspaces must be >= 1")

        expected = {
            "ready_workspaces": sum(1 for entry in self.entries if entry.workspace_ready),
            "source_bound_workspaces": sum(1 for entry in self.entries if entry.source_bound),
            "versioned_workspaces": sum(1 for entry in self.entries if entry.versioned),
            "read_only_workspaces": sum(1 for entry in self.entries if entry.read_only),
            "runtime_write_allowed_workspaces": sum(1 for entry in self.entries if entry.runtime_write_allowed),
            "dashboard_visible_workspaces": sum(1 for entry in self.entries if entry.dashboard_visible),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_workspaces != self.total_workspaces:
            raise ValueError("all project workspaces must be ready")
        if self.source_bound_workspaces != self.total_workspaces:
            raise ValueError("all project workspaces must be source-bound")
        if self.versioned_workspaces != self.total_workspaces:
            raise ValueError("all project workspaces must be versioned")
        if self.read_only_workspaces != self.total_workspaces:
            raise ValueError("all project workspaces must be read-only")
        if self.runtime_write_allowed_workspaces != 0:
            raise ValueError("runtime workspace writes must remain blocked in Batch 1")


def build_project_workspace_contract() -> ProjectWorkspaceContract:
    entries = (
        ProjectWorkspaceEntry(
            workspace_id="project_workspace_robotics_001",
            workspace_kind="robotics",
            storage_node_id="storage_node_artifact_store",
            project_root_ref="projects/robotics",
            artifact_namespace="project_artifacts::robotics",
            source_bound=True,
            versioned=True,
            read_only=True,
            runtime_write_allowed=False,
            dashboard_visible=True,
            workspace_ready=True,
            description="Read-only robotics project workspace placeholder.",
        ),
        ProjectWorkspaceEntry(
            workspace_id="project_workspace_cad_3d_001",
            workspace_kind="cad_3d",
            storage_node_id="storage_node_artifact_store",
            project_root_ref="projects/cad_3d",
            artifact_namespace="project_artifacts::cad_3d",
            source_bound=True,
            versioned=True,
            read_only=True,
            runtime_write_allowed=False,
            dashboard_visible=True,
            workspace_ready=True,
            description="Read-only CAD/3D project workspace placeholder.",
        ),
        ProjectWorkspaceEntry(
            workspace_id="project_workspace_energy_001",
            workspace_kind="energy",
            storage_node_id="storage_node_artifact_store",
            project_root_ref="projects/energy",
            artifact_namespace="project_artifacts::energy",
            source_bound=True,
            versioned=True,
            read_only=True,
            runtime_write_allowed=False,
            dashboard_visible=True,
            workspace_ready=True,
            description="Read-only energy project workspace placeholder.",
        ),
    )

    return ProjectWorkspaceContract(
        total_workspaces=len(entries),
        ready_workspaces=sum(1 for entry in entries if entry.workspace_ready),
        source_bound_workspaces=sum(1 for entry in entries if entry.source_bound),
        versioned_workspaces=sum(1 for entry in entries if entry.versioned),
        read_only_workspaces=sum(1 for entry in entries if entry.read_only),
        runtime_write_allowed_workspaces=sum(1 for entry in entries if entry.runtime_write_allowed),
        dashboard_visible_workspaces=sum(1 for entry in entries if entry.dashboard_visible),
        entries=entries,
    )
