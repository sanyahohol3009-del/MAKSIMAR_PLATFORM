from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.runtime_model_storage_policy_contract import (
    RuntimeModelStoragePolicy,
    build_runtime_model_storage_policy,
)


def test_runtime_model_storage_policy_keeps_weights_outside_git_core_memory_dashboard() -> None:
    policy = build_runtime_model_storage_policy()
    read_model = policy.to_read_model()

    assert read_model["runtime_assets_only"] is True
    assert read_model["project_truth_allowed"] is False
    assert read_model["git_storage_allowed"] is False
    assert read_model["core_storage_allowed"] is False
    assert read_model["dashboard_storage_allowed"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["read_only"] is True
    assert all(root.startswith("~/MAKSIMAR_RUNTIME/runtime_models/") for root in read_model["allowed_roots"])


def test_runtime_model_storage_policy_has_expected_model_role_roots() -> None:
    policy = build_runtime_model_storage_policy()

    joined = "\n".join(policy.allowed_roots)
    for role in (
        "chat",
        "planner",
        "coder",
        "vision",
        "stt",
        "tts",
        "image",
        "video",
        "embedding",
        "reranker",
    ):
        assert f"/{role}" in joined


def test_runtime_model_storage_policy_rejects_core_storage_root() -> None:
    with pytest.raises(ValueError):
        RuntimeModelStoragePolicy(
            policy_id="bad_policy",
            allowed_roots=("MAKSIMAR_CORE_LIB/runtime_models/chat",),
            forbidden_markers=("MAKSIMAR_CORE_LIB",),
            runtime_assets_only=True,
            project_truth_allowed=False,
            git_storage_allowed=False,
            core_storage_allowed=False,
            dashboard_storage_allowed=False,
            model_download_allowed=False,
            runtime_start_allowed=False,
            read_only=True,
        )


def test_runtime_model_storage_policy_rejects_download_enablement() -> None:
    with pytest.raises(ValueError):
        RuntimeModelStoragePolicy(
            policy_id="bad_policy",
            allowed_roots=("~/MAKSIMAR_RUNTIME/runtime_models/chat",),
            forbidden_markers=("MAKSIMAR_CORE_LIB",),
            runtime_assets_only=True,
            project_truth_allowed=False,
            git_storage_allowed=False,
            core_storage_allowed=False,
            dashboard_storage_allowed=False,
            model_download_allowed=True,
            runtime_start_allowed=False,
            read_only=True,
        )
