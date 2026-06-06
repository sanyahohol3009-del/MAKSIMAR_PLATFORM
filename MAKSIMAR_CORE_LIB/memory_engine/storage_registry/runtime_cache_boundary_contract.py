from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.runtime_model_storage_policy_contract import (
    build_runtime_model_storage_policy,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.runtime_retrieval_storage_policy_contract import (
    build_runtime_retrieval_storage_policy,
)


@dataclass(frozen=True, slots=True)
class RuntimeCacheBoundary:
    boundary_id: str
    model_policy_id: str
    retrieval_policy_id: str
    cache_roots: tuple[str, ...]
    immutable_project_truth_allowed: bool
    runtime_cache_mutation_allowed: bool
    source_refs_required: bool
    direct_core_write_allowed: bool
    dashboard_write_allowed: bool
    model_download_allowed: bool
    runtime_start_allowed: bool
    read_only: bool
    dashboard_safe: bool

    def __post_init__(self) -> None:
        _require_non_empty(self.boundary_id, "boundary_id")
        _require_non_empty(self.model_policy_id, "model_policy_id")
        _require_non_empty(self.retrieval_policy_id, "retrieval_policy_id")
        _require_non_empty_tuple(self.cache_roots, "cache_roots")

        for root in self.cache_roots:
            if not root.startswith("~/MAKSIMAR_RUNTIME/"):
                raise ValueError("cache roots must live under ~/MAKSIMAR_RUNTIME")

        _require_false(self.immutable_project_truth_allowed, "immutable_project_truth_allowed")
        _require_true(self.runtime_cache_mutation_allowed, "runtime_cache_mutation_allowed")
        _require_true(self.source_refs_required, "source_refs_required")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.dashboard_write_allowed, "dashboard_write_allowed")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "boundary_id": self.boundary_id,
            "model_policy_id": self.model_policy_id,
            "retrieval_policy_id": self.retrieval_policy_id,
            "cache_roots": self.cache_roots,
            "immutable_project_truth_allowed": self.immutable_project_truth_allowed,
            "runtime_cache_mutation_allowed": self.runtime_cache_mutation_allowed,
            "source_refs_required": self.source_refs_required,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "dashboard_write_allowed": self.dashboard_write_allowed,
            "model_download_allowed": self.model_download_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
        }


def build_runtime_cache_boundary() -> RuntimeCacheBoundary:
    model_policy = build_runtime_model_storage_policy()
    retrieval_policy = build_runtime_retrieval_storage_policy()

    return RuntimeCacheBoundary(
        boundary_id="jarvis_live_runtime_cache_boundary_v1",
        model_policy_id=model_policy.policy_id,
        retrieval_policy_id=retrieval_policy.policy_id,
        cache_roots=(
            "~/MAKSIMAR_RUNTIME/runtime_retrieval",
            "~/MAKSIMAR_RUNTIME/runtime_embeddings",
            "~/MAKSIMAR_RUNTIME/runtime_vector_indexes",
            "~/MAKSIMAR_RUNTIME/runtime_rag_cache",
        ),
        immutable_project_truth_allowed=False,
        runtime_cache_mutation_allowed=True,
        source_refs_required=True,
        direct_core_write_allowed=False,
        dashboard_write_allowed=False,
        model_download_allowed=False,
        runtime_start_allowed=False,
        read_only=True,
        dashboard_safe=True,
    )


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_non_empty_tuple(value: tuple[str, ...], field_name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise ValueError(f"{field_name} must be a non-empty tuple")
    for item in value:
        _require_non_empty(item, field_name)


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")
