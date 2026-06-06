from __future__ import annotations

from dataclasses import dataclass
from typing import Any


RUNTIME_RETRIEVAL_ROOTS: tuple[str, ...] = (
    "~/MAKSIMAR_RUNTIME/runtime_retrieval",
    "~/MAKSIMAR_RUNTIME/runtime_embeddings",
    "~/MAKSIMAR_RUNTIME/runtime_vector_indexes",
    "~/MAKSIMAR_RUNTIME/runtime_rag_cache",
)


@dataclass(frozen=True, slots=True)
class RuntimeRetrievalStoragePolicy:
    policy_id: str
    retrieval_root: str
    embeddings_root: str
    vector_indexes_root: str
    rag_cache_root: str
    source_truth_root: str
    runtime_assets_only: bool
    project_truth_stored_in_retrieval_cache: bool
    source_refs_required: bool
    mutable_runtime_cache: bool
    model_download_allowed: bool
    runtime_start_allowed: bool
    read_only: bool

    def __post_init__(self) -> None:
        for field_name in (
            "policy_id",
            "retrieval_root",
            "embeddings_root",
            "vector_indexes_root",
            "rag_cache_root",
            "source_truth_root",
        ):
            _require_non_empty(getattr(self, field_name), field_name)

        for root in (
            self.retrieval_root,
            self.embeddings_root,
            self.vector_indexes_root,
            self.rag_cache_root,
        ):
            if not root.startswith("~/MAKSIMAR_RUNTIME/"):
                raise ValueError("retrieval runtime roots must live under ~/MAKSIMAR_RUNTIME")

        if self.source_truth_root != "MAKSIMAR_CORE_LIB/memory_engine":
            raise ValueError("project truth must remain owned by MAKSIMAR_CORE_LIB/memory_engine")

        _require_true(self.runtime_assets_only, "runtime_assets_only")
        _require_false(
            self.project_truth_stored_in_retrieval_cache,
            "project_truth_stored_in_retrieval_cache",
        )
        _require_true(self.source_refs_required, "source_refs_required")
        _require_true(self.mutable_runtime_cache, "mutable_runtime_cache")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_true(self.read_only, "read_only")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "retrieval_root": self.retrieval_root,
            "embeddings_root": self.embeddings_root,
            "vector_indexes_root": self.vector_indexes_root,
            "rag_cache_root": self.rag_cache_root,
            "source_truth_root": self.source_truth_root,
            "runtime_assets_only": self.runtime_assets_only,
            "project_truth_stored_in_retrieval_cache": self.project_truth_stored_in_retrieval_cache,
            "source_refs_required": self.source_refs_required,
            "mutable_runtime_cache": self.mutable_runtime_cache,
            "model_download_allowed": self.model_download_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
            "read_only": self.read_only,
        }


def build_runtime_retrieval_storage_policy() -> RuntimeRetrievalStoragePolicy:
    return RuntimeRetrievalStoragePolicy(
        policy_id="jarvis_live_runtime_retrieval_storage_policy_v1",
        retrieval_root="~/MAKSIMAR_RUNTIME/runtime_retrieval",
        embeddings_root="~/MAKSIMAR_RUNTIME/runtime_embeddings",
        vector_indexes_root="~/MAKSIMAR_RUNTIME/runtime_vector_indexes",
        rag_cache_root="~/MAKSIMAR_RUNTIME/runtime_rag_cache",
        source_truth_root="MAKSIMAR_CORE_LIB/memory_engine",
        runtime_assets_only=True,
        project_truth_stored_in_retrieval_cache=False,
        source_refs_required=True,
        mutable_runtime_cache=True,
        model_download_allowed=False,
        runtime_start_allowed=False,
        read_only=True,
    )


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")
