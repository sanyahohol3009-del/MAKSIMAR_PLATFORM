from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

ModelRepositoryKind = Literal["local_weights", "adapter_weights", "embedding_model"]

_MODEL_REPOSITORY_ID_PATTERN = re.compile(r"^model_repository_[a-z][a-z0-9_]*_[0-9]{3}$")


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
class ModelRepositoryEntry:
    model_repository_id: str
    model_name: str
    model_repository_kind: ModelRepositoryKind
    storage_node_id: str
    artifact_ref: str
    version: str
    source_bound: bool
    versioned: bool
    read_only: bool
    runtime_load_allowed: bool
    dashboard_visible: bool
    retrieval_visible: bool
    repository_ready: bool
    description: str

    def __post_init__(self) -> None:
        repository_id = _ensure_non_empty_str(self.model_repository_id, "model_repository_id")
        if not _MODEL_REPOSITORY_ID_PATTERN.fullmatch(repository_id):
            raise ValueError(f"Invalid model_repository_id: {repository_id}")

        for field_name in (
            "model_name",
            "storage_node_id",
            "artifact_ref",
            "version",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "source_bound",
            "versioned",
            "read_only",
            "runtime_load_allowed",
            "dashboard_visible",
            "retrieval_visible",
            "repository_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.source_bound:
            raise ValueError("source_bound must be True")
        if not self.versioned:
            raise ValueError("versioned must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.runtime_load_allowed:
            raise ValueError("runtime_load_allowed must be False in Batch 1")
        if not self.dashboard_visible:
            raise ValueError("dashboard_visible must be True")
        if not self.repository_ready:
            raise ValueError("repository_ready must be True")


@dataclass(frozen=True, slots=True)
class ModelRepositoryContract:
    total_repositories: int
    ready_repositories: int
    source_bound_repositories: int
    versioned_repositories: int
    read_only_repositories: int
    runtime_load_allowed_repositories: int
    dashboard_visible_repositories: int
    entries: tuple[ModelRepositoryEntry, ...]

    def __post_init__(self) -> None:
        if self.total_repositories != len(self.entries):
            raise ValueError("total_repositories must match entries length")
        if self.total_repositories <= 0:
            raise ValueError("total_repositories must be >= 1")

        expected = {
            "ready_repositories": sum(1 for entry in self.entries if entry.repository_ready),
            "source_bound_repositories": sum(1 for entry in self.entries if entry.source_bound),
            "versioned_repositories": sum(1 for entry in self.entries if entry.versioned),
            "read_only_repositories": sum(1 for entry in self.entries if entry.read_only),
            "runtime_load_allowed_repositories": sum(1 for entry in self.entries if entry.runtime_load_allowed),
            "dashboard_visible_repositories": sum(1 for entry in self.entries if entry.dashboard_visible),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_repositories != self.total_repositories:
            raise ValueError("all model repositories must be ready")
        if self.source_bound_repositories != self.total_repositories:
            raise ValueError("all model repositories must be source-bound")
        if self.versioned_repositories != self.total_repositories:
            raise ValueError("all model repositories must be versioned")
        if self.read_only_repositories != self.total_repositories:
            raise ValueError("all model repositories must be read-only")
        if self.runtime_load_allowed_repositories != 0:
            raise ValueError("runtime model loading must remain blocked in Batch 1")


def build_model_repository_contract() -> ModelRepositoryContract:
    entries = (
        ModelRepositoryEntry(
            model_repository_id="model_repository_local_llm_001",
            model_name="local_llm_weights_placeholder",
            model_repository_kind="local_weights",
            storage_node_id="storage_node_model_store",
            artifact_ref="artifact_ref_model_weights_local_llm_v1",
            version="v1",
            source_bound=True,
            versioned=True,
            read_only=True,
            runtime_load_allowed=False,
            dashboard_visible=True,
            retrieval_visible=False,
            repository_ready=True,
            description="Read-only placeholder for local model weights storage.",
        ),
        ModelRepositoryEntry(
            model_repository_id="model_repository_embedding_001",
            model_name="embedding_model_placeholder",
            model_repository_kind="embedding_model",
            storage_node_id="storage_node_model_store",
            artifact_ref="artifact_ref_model_weights_embedding_v1",
            version="v1",
            source_bound=True,
            versioned=True,
            read_only=True,
            runtime_load_allowed=False,
            dashboard_visible=True,
            retrieval_visible=True,
            repository_ready=True,
            description="Read-only placeholder for embedding model storage.",
        ),
    )

    return ModelRepositoryContract(
        total_repositories=len(entries),
        ready_repositories=sum(1 for entry in entries if entry.repository_ready),
        source_bound_repositories=sum(1 for entry in entries if entry.source_bound),
        versioned_repositories=sum(1 for entry in entries if entry.versioned),
        read_only_repositories=sum(1 for entry in entries if entry.read_only),
        runtime_load_allowed_repositories=sum(1 for entry in entries if entry.runtime_load_allowed),
        dashboard_visible_repositories=sum(1 for entry in entries if entry.dashboard_visible),
        entries=entries,
    )
