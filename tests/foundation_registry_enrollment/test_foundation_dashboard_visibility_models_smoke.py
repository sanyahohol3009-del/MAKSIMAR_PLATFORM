from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_dashboard_visibility_models import (
    FoundationDashboardVisibilityModel,
    build_dashboard_visibility_from_enrollments,
    build_default_foundation_dashboard_visibility_models,
    build_foundation_dashboard_visibility_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_domain_enrollment_models import (
    build_default_foundation_domain_enrollments,
    build_foundation_domain_enrollment_model,
)
from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_manifest_models import (
    FOUNDATION_LAYER_IDS,
)


def test_default_foundation_dashboard_visibility_covers_all_layers() -> None:
    visibility = build_default_foundation_dashboard_visibility_models()

    assert tuple(item.domain_enrollment.registry_domain_id for item in visibility) == FOUNDATION_LAYER_IDS
    assert all(item.visible_in_foundation_dashboard is True for item in visibility)
    assert all(item.dashboard_control_allowed is False for item in visibility)
    assert all(item.dashboard_registry_write_allowed is False for item in visibility)
    assert all(item.runtime_mutation_allowed is False for item in visibility)
    assert all(item.dashboard_safe is True for item in visibility)
    assert all(item.read_only is True for item in visibility)


def test_dashboard_visibility_builder_from_enrollments_preserves_order() -> None:
    enrollments = build_default_foundation_domain_enrollments()
    visibility = build_dashboard_visibility_from_enrollments(enrollments)

    assert tuple(item.domain_enrollment.registry_domain_id for item in visibility) == FOUNDATION_LAYER_IDS


def test_foundation_dashboard_visibility_builder_returns_expected_layer() -> None:
    visibility = build_foundation_dashboard_visibility_model("ai_orchestration")

    assert visibility.visibility_id == "ai_orchestration_dashboard_visibility_v1"
    assert visibility.domain_enrollment.registry_domain_id == "ai_orchestration"
    assert visibility.dashboard_surface_id == "foundation_registry_enrollment_dashboard_read_model"


def test_foundation_dashboard_visibility_rejects_dashboard_control() -> None:
    enrollment = build_foundation_domain_enrollment_model("security_layer")

    with pytest.raises(ValueError, match="dashboard_control_allowed"):
        FoundationDashboardVisibilityModel(
            visibility_id="bad",
            domain_enrollment=enrollment,
            dashboard_surface_id="foundation_registry_enrollment_dashboard_read_model",
            visible_in_foundation_dashboard=True,
            dashboard_control_allowed=True,
            dashboard_registry_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_foundation_dashboard_visibility_rejects_dashboard_registry_write() -> None:
    enrollment = build_foundation_domain_enrollment_model("security_layer")

    with pytest.raises(ValueError, match="dashboard_registry_write_allowed"):
        FoundationDashboardVisibilityModel(
            visibility_id="bad",
            domain_enrollment=enrollment,
            dashboard_surface_id="foundation_registry_enrollment_dashboard_read_model",
            visible_in_foundation_dashboard=True,
            dashboard_control_allowed=False,
            dashboard_registry_write_allowed=True,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
