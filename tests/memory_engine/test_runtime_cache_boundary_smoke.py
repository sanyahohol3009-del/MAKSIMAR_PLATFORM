from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.runtime_cache_boundary_contract import (
    RuntimeCacheBoundary,
    build_runtime_cache_boundary,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def test_runtime_cache_boundary_is_read_only_dashboard_safe_and_blocks_download() -> None:
    boundary = build_runtime_cache_boundary()
    read_model = boundary.to_read_model()

    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert read_model["immutable_project_truth_allowed"] is False
    assert read_model["runtime_cache_mutation_allowed"] is True
    assert read_model["source_refs_required"] is True
    assert read_model["direct_core_write_allowed"] is False
    assert read_model["dashboard_write_allowed"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["runtime_start_allowed"] is False


def test_runtime_cache_boundary_uses_only_runtime_roots() -> None:
    boundary = build_runtime_cache_boundary()

    assert all(root.startswith("~/MAKSIMAR_RUNTIME/") for root in boundary.cache_roots)
    assert "~/MAKSIMAR_RUNTIME/runtime_rag_cache" in boundary.cache_roots
    assert "~/MAKSIMAR_RUNTIME/runtime_vector_indexes" in boundary.cache_roots


def test_runtime_cache_boundary_rejects_core_write_enablement() -> None:
    with pytest.raises(ValueError):
        RuntimeCacheBoundary(
            boundary_id="bad_boundary",
            model_policy_id="model_policy",
            retrieval_policy_id="retrieval_policy",
            cache_roots=("~/MAKSIMAR_RUNTIME/runtime_rag_cache",),
            immutable_project_truth_allowed=False,
            runtime_cache_mutation_allowed=True,
            source_refs_required=True,
            direct_core_write_allowed=True,
            dashboard_write_allowed=False,
            model_download_allowed=False,
            runtime_start_allowed=False,
            read_only=True,
            dashboard_safe=True,
        )


def test_jarvis_roadmap_marks_jl4_ready_but_download_still_blocked_until_jl10() -> None:
    status = build_jarvis_live_full_roadmap_status()

    assert "JL-4" in status["ready_batches"]
    assert status["next_batch"]["batch_id"] == "JL-5"
    assert status["download_gate_status"]["storage_boundary_ready"] is True
    assert status["download_gate_status"]["vendor_boundary_ready"] is False
    assert status["model_download_allowed_now"] is False
