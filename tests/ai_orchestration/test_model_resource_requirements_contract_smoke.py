from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.model_resource_requirements_contract import (
    ModelResourceRequirement,
    build_default_model_resource_requirements,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_role_binding_contract import (
    JARVIS_LIVE_MODEL_ROLES,
)


def test_model_resource_requirements_cover_all_roles_and_require_admission() -> None:
    requirements = build_default_model_resource_requirements()

    assert {requirement.role for requirement in requirements} == set(JARVIS_LIVE_MODEL_ROLES)
    assert all(requirement.queue_required is True for requirement in requirements)
    assert all(requirement.admission_required is True for requirement in requirements)
    assert all(requirement.resource_snapshot_required is True for requirement in requirements)
    assert all(requirement.model_download_allowed is False for requirement in requirements)
    assert all(requirement.runtime_start_allowed is False for requirement in requirements)


def test_model_resource_requirements_keep_runtime_assets_outside_core_truth() -> None:
    requirements = build_default_model_resource_requirements()

    assert all(
        requirement.runtime_asset_root == "~/MAKSIMAR_RUNTIME/runtime_models"
        for requirement in requirements
    )
    assert not any("MAKSIMAR_CORE_LIB" in requirement.runtime_asset_root for requirement in requirements)
    assert not any("memory_engine" in requirement.runtime_asset_root for requirement in requirements)


def test_coder_and_vision_have_gpu_weighted_requirements_but_no_download() -> None:
    by_role = {requirement.role: requirement for requirement in build_default_model_resource_requirements()}

    assert by_role["coder"].preferred_vram_gb >= 12
    assert by_role["vision"].preferred_vram_gb >= 12
    assert by_role["video"].preferred_vram_gb >= by_role["image"].preferred_vram_gb
    assert by_role["coder"].model_download_allowed is False
    assert by_role["vision"].runtime_start_allowed is False


def test_resource_requirement_rejects_invalid_role() -> None:
    with pytest.raises(ValueError):
        ModelResourceRequirement(
            role="unknown",
            requirement_id="bad",
            min_vram_gb=0,
            preferred_vram_gb=0,
            min_ram_gb=1,
            min_cpu_threads=1,
            queue_required=True,
            admission_required=True,
            resource_snapshot_required=True,
            runtime_asset_root="~/MAKSIMAR_RUNTIME/runtime_models",
            model_download_allowed=False,
            runtime_start_allowed=False,
        )


def test_resource_requirement_rejects_download_enablement() -> None:
    with pytest.raises(ValueError):
        ModelResourceRequirement(
            role="chat",
            requirement_id="bad",
            min_vram_gb=0,
            preferred_vram_gb=0,
            min_ram_gb=1,
            min_cpu_threads=1,
            queue_required=True,
            admission_required=True,
            resource_snapshot_required=True,
            runtime_asset_root="~/MAKSIMAR_RUNTIME/runtime_models",
            model_download_allowed=True,
            runtime_start_allowed=False,
        )
