from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    ModelProfile,
    build_model_profile_registry,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_role_binding_contract import (
    JARVIS_LIVE_MODEL_ROLES,
    build_default_model_role_bindings,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_profile_read_model_builder import (
    build_model_profile_read_model,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def test_model_profile_registry_covers_all_jarvis_live_roles() -> None:
    registry = build_model_profile_registry()
    read_model = registry.to_read_model()

    profile_roles = {profile["role"] for profile in read_model["profiles"]}
    assert profile_roles == set(JARVIS_LIVE_MODEL_ROLES)
    assert len(read_model["profiles"]) == 12
    assert read_model["duplicated_registry_surfaces"] == ()
    assert read_model["model_download_allowed_now"] is True
    assert read_model["runtime_start_allowed_now"] is False


def test_model_role_bindings_reuse_existing_architecture_surfaces() -> None:
    bindings = build_default_model_role_bindings()

    assert {binding.role for binding in bindings} == set(JARVIS_LIVE_MODEL_ROLES)
    assert all(binding.existing_service_surface == "AI_SERVICES/config" for binding in bindings)
    assert all(binding.existing_router_surface == "MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding" for binding in bindings)
    assert all(binding.existing_worker_surface == "MAKSIMAR_CORE_LIB/workers_registry" for binding in bindings)
    assert all(binding.existing_execution_surface == "MAKSIMAR_CORE_LIB/execution_control" for binding in bindings)
    assert all(binding.model_download_allowed is False for binding in bindings)
    assert all(binding.runtime_start_allowed is False for binding in bindings)
    assert all(binding.direct_shell_allowed is False for binding in bindings)


def test_model_profile_read_model_is_dashboard_safe_and_read_only() -> None:
    read_model = build_model_profile_read_model()

    assert read_model["summary_id"] == "jarvis_live_model_profile_read_model_v1"
    assert read_model["profile_count"] == 12
    assert read_model["model_download_allowed_now"] is True
    assert read_model["runtime_start_allowed_now"] is False
    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert "AI_SERVICES/config" in read_model["referenced_architecture_surfaces"]


def test_model_profile_rejects_download_enablement() -> None:
    with pytest.raises(ValueError):
        ModelProfile(
            profile_id="bad_profile",
            role="chat",
            candidate_family="bad",
            existing_service_surface="AI_SERVICES/config",
            resource_requirement_id="bad_requirement",
            runtime_asset_subdir="chat",
            proposal_only=True,
            enabled=False,
            model_download_allowed=True,
            runtime_start_allowed=False,
        )


def test_jarvis_live_full_roadmap_now_sees_jl2_ready() -> None:
    status = build_jarvis_live_full_roadmap_status()

    assert "JL-2" in status["ready_batches"]
    assert status["model_download_allowed_now"] == ("JL-10" in status["ready_batches"])
    assert status["runtime_start_allowed_now"] is False
