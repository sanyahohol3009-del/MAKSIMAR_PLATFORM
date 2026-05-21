from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_ai_orchestration_enrollment_builder import (
    AI_ORCHESTRATION_FOUNDATION_EXISTING_SURFACES,
    AIOrchestrationFoundationEnrollmentReadModel,
    build_ai_orchestration_foundation_enrollment_read_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_dashboard_visibility_models import (
    build_foundation_dashboard_visibility_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_domain_enrollment_models import (
    build_foundation_domain_enrollment_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_manifest_models import (
    build_foundation_layer_manifest_model,
)


def test_ai_orchestration_foundation_enrollment_is_registry_and_dashboard_visible() -> None:
    read_model = build_ai_orchestration_foundation_enrollment_read_model()

    assert read_model.read_model_id == "ai_orchestration_foundation_enrollment_read_model_v1"
    assert read_model.layer_manifest.layer_id == "ai_orchestration"
    assert read_model.domain_enrollment.registry_domain_id == "ai_orchestration"
    assert read_model.dashboard_visibility.domain_enrollment.registry_domain_id == "ai_orchestration"
    assert read_model.existing_ai_orchestration_surfaces == AI_ORCHESTRATION_FOUNDATION_EXISTING_SURFACES
    assert read_model.ai_orchestration_registry_visible is True
    assert read_model.ai_orchestration_dashboard_visible is True
    assert read_model.existing_ai_orchestration_accounted is True
    assert read_model.replaces_ai_orchestration is False
    assert read_model.migrates_ai_orchestration is False
    assert read_model.duplicates_ai_orchestration_logic is False
    assert read_model.registry_write_allowed is False
    assert read_model.auto_enrollment_write_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.dashboard_control_allowed is False
    assert read_model.ai_execution_allowed is False
    assert read_model.direct_tool_execution_allowed is False
    assert read_model.deployment_allowed is False
    assert read_model.public_exposure_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.read_only is True


def test_ai_orchestration_foundation_enrollment_accounts_expected_surfaces() -> None:
    read_model = build_ai_orchestration_foundation_enrollment_read_model()

    assert "AI_ORCHESTRATION/layer_manifest.yaml" in read_model.existing_ai_orchestration_surfaces
    assert "AI_ORCHESTRATION/container_contract.yaml" in read_model.existing_ai_orchestration_surfaces
    assert "MAKSIMAR_CORE_LIB/ai_orchestration/ai_orchestration_acceptance_read_model.py" in read_model.existing_ai_orchestration_surfaces
    assert "MAKSIMAR_SERVER/AI_ORCHESTRATION/ai_orchestration_read_model_builder.py" in read_model.existing_ai_orchestration_surfaces
    assert "docs/architecture/foundation/ai_orchestration_foundation_v1.md" in read_model.existing_ai_orchestration_surfaces


def test_ai_orchestration_foundation_enrollment_to_dict_is_non_executing() -> None:
    payload = build_ai_orchestration_foundation_enrollment_read_model().to_dict()

    assert payload["ai_orchestration_registry_visible"] is True
    assert payload["ai_orchestration_dashboard_visible"] is True
    assert payload["registry_write_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["dashboard_control_allowed"] is False
    assert payload["ai_execution_allowed"] is False
    assert payload["direct_tool_execution_allowed"] is False
    assert payload["deployment_allowed"] is False
    assert payload["public_exposure_allowed"] is False
    assert payload["dashboard_safe"] is True
    assert payload["read_only"] is True


def test_ai_orchestration_foundation_enrollment_rejects_ai_execution() -> None:
    with pytest.raises(ValueError, match="ai_execution_allowed"):
        AIOrchestrationFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("ai_orchestration"),
            domain_enrollment=build_foundation_domain_enrollment_model("ai_orchestration"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("ai_orchestration"),
            existing_ai_orchestration_surfaces=AI_ORCHESTRATION_FOUNDATION_EXISTING_SURFACES,
            ai_orchestration_registry_visible=True,
            ai_orchestration_dashboard_visible=True,
            existing_ai_orchestration_accounted=True,
            replaces_ai_orchestration=False,
            migrates_ai_orchestration=False,
            duplicates_ai_orchestration_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            ai_execution_allowed=True,
            direct_tool_execution_allowed=False,
            deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_ai_orchestration_foundation_enrollment_rejects_wrong_layer_binding() -> None:
    with pytest.raises(ValueError, match="layer_manifest must describe ai_orchestration"):
        AIOrchestrationFoundationEnrollmentReadModel(
            read_model_id="bad",
            layer_manifest=build_foundation_layer_manifest_model("security_layer"),
            domain_enrollment=build_foundation_domain_enrollment_model("ai_orchestration"),
            dashboard_visibility=build_foundation_dashboard_visibility_model("ai_orchestration"),
            existing_ai_orchestration_surfaces=AI_ORCHESTRATION_FOUNDATION_EXISTING_SURFACES,
            ai_orchestration_registry_visible=True,
            ai_orchestration_dashboard_visible=True,
            existing_ai_orchestration_accounted=True,
            replaces_ai_orchestration=False,
            migrates_ai_orchestration=False,
            duplicates_ai_orchestration_logic=False,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_control_allowed=False,
            ai_execution_allowed=False,
            direct_tool_execution_allowed=False,
            deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
