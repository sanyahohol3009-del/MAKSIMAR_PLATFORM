from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.runtime_retrieval_storage_policy_contract import (
    RuntimeRetrievalStoragePolicy,
    build_runtime_retrieval_storage_policy,
)


def test_runtime_retrieval_policy_separates_cache_from_project_truth() -> None:
    policy = build_runtime_retrieval_storage_policy()
    read_model = policy.to_read_model()

    assert read_model["retrieval_root"] == "~/MAKSIMAR_RUNTIME/runtime_retrieval"
    assert read_model["embeddings_root"] == "~/MAKSIMAR_RUNTIME/runtime_embeddings"
    assert read_model["vector_indexes_root"] == "~/MAKSIMAR_RUNTIME/runtime_vector_indexes"
    assert read_model["rag_cache_root"] == "~/MAKSIMAR_RUNTIME/runtime_rag_cache"
    assert read_model["source_truth_root"] == "MAKSIMAR_CORE_LIB/memory_engine"
    assert read_model["project_truth_stored_in_retrieval_cache"] is False
    assert read_model["source_refs_required"] is True
    assert read_model["model_download_allowed"] is False
    assert read_model["runtime_start_allowed"] is False


def test_runtime_retrieval_policy_rejects_project_truth_inside_cache() -> None:
    with pytest.raises(ValueError):
        RuntimeRetrievalStoragePolicy(
            policy_id="bad_policy",
            retrieval_root="~/MAKSIMAR_RUNTIME/runtime_retrieval",
            embeddings_root="~/MAKSIMAR_RUNTIME/runtime_embeddings",
            vector_indexes_root="~/MAKSIMAR_RUNTIME/runtime_vector_indexes",
            rag_cache_root="~/MAKSIMAR_RUNTIME/runtime_rag_cache",
            source_truth_root="MAKSIMAR_CORE_LIB/memory_engine",
            runtime_assets_only=True,
            project_truth_stored_in_retrieval_cache=True,
            source_refs_required=True,
            mutable_runtime_cache=True,
            model_download_allowed=False,
            runtime_start_allowed=False,
            read_only=True,
        )


def test_runtime_retrieval_policy_rejects_wrong_source_truth_owner() -> None:
    with pytest.raises(ValueError):
        RuntimeRetrievalStoragePolicy(
            policy_id="bad_policy",
            retrieval_root="~/MAKSIMAR_RUNTIME/runtime_retrieval",
            embeddings_root="~/MAKSIMAR_RUNTIME/runtime_embeddings",
            vector_indexes_root="~/MAKSIMAR_RUNTIME/runtime_vector_indexes",
            rag_cache_root="~/MAKSIMAR_RUNTIME/runtime_rag_cache",
            source_truth_root="~/MAKSIMAR_RUNTIME/runtime_rag_cache",
            runtime_assets_only=True,
            project_truth_stored_in_retrieval_cache=False,
            source_refs_required=True,
            mutable_runtime_cache=True,
            model_download_allowed=False,
            runtime_start_allowed=False,
            read_only=True,
        )


def test_runtime_retrieval_policy_rejects_download_enablement() -> None:
    with pytest.raises(ValueError):
        RuntimeRetrievalStoragePolicy(
            policy_id="bad_policy",
            retrieval_root="~/MAKSIMAR_RUNTIME/runtime_retrieval",
            embeddings_root="~/MAKSIMAR_RUNTIME/runtime_embeddings",
            vector_indexes_root="~/MAKSIMAR_RUNTIME/runtime_vector_indexes",
            rag_cache_root="~/MAKSIMAR_RUNTIME/runtime_rag_cache",
            source_truth_root="MAKSIMAR_CORE_LIB/memory_engine",
            runtime_assets_only=True,
            project_truth_stored_in_retrieval_cache=False,
            source_refs_required=True,
            mutable_runtime_cache=True,
            model_download_allowed=True,
            runtime_start_allowed=False,
            read_only=True,
        )
