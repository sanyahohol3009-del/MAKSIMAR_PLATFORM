from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration import (
    AIOrchestrationSurfaceReadModel,
    ExistingAIOrchestrationBindingReadModel,
    build_ai_orchestration_surface_read_model,
    build_existing_ai_orchestration_binding_read_model,
)


def test_existing_ai_orchestration_binding_read_model_binds_existing_surfaces() -> None:
    read_model = build_existing_ai_orchestration_binding_read_model()

    assert read_model.read_model_id == "existing_ai_orchestration_binding_read_model_v1"
    assert read_model.ai_services_bound is True
    assert read_model.workers_bound is True
    assert read_model.control_plane_ai_router_bound is True
    assert read_model.duplicate_ai_services_allowed is False
    assert read_model.duplicate_workers_allowed is False
    assert read_model.duplicate_router_allowed is False
    assert read_model.mempalace_source_of_truth is False
    assert read_model.dashboard_safe is True
    assert read_model.read_only is True


def test_ai_orchestration_surface_read_model_blocks_execution_and_mutation() -> None:
    read_model = build_ai_orchestration_surface_read_model()

    assert read_model.read_model_id == "ai_orchestration_surface_read_model_v1"
    assert read_model.direct_autonomous_execution_allowed is False
    assert read_model.proposal_execution_allowed is False
    assert read_model.stage_execution_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.production_deployment_allowed is False
    assert read_model.public_exposure_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.read_only is True


def test_ai_orchestration_surface_read_model_rejects_direct_autonomous_execution() -> None:
    binding = build_existing_ai_orchestration_binding_read_model()

    with pytest.raises(ValueError, match="direct_autonomous_execution_allowed"):
        AIOrchestrationSurfaceReadModel(
            read_model_id="bad",
            layer_id="AI_ORCHESTRATION",
            binding=binding,
            direct_autonomous_execution_allowed=True,
            proposal_execution_allowed=False,
            stage_execution_allowed=False,
            runtime_mutation_allowed=False,
            production_deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_existing_ai_orchestration_binding_rejects_duplicate_ai_services() -> None:
    with pytest.raises(ValueError, match="duplicate_ai_services_allowed"):
        ExistingAIOrchestrationBindingReadModel(
            read_model_id="bad",
            layer_id="AI_ORCHESTRATION",
            ai_services_bound=True,
            workers_bound=True,
            control_plane_ai_router_bound=True,
            ai_service_binding_paths=("AI_SERVICES",),
            worker_binding_paths=("MAKSIMAR_SERVER/WORKERS",),
            control_plane_ai_router_binding_paths=("MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",),
            duplicate_ai_services_allowed=True,
            duplicate_workers_allowed=False,
            duplicate_router_allowed=False,
            mempalace_source_of_truth=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_ai_orchestration_facade_exports_surface_read_model() -> None:
    read_model = build_ai_orchestration_surface_read_model()

    assert isinstance(read_model, AIOrchestrationSurfaceReadModel)
    assert isinstance(read_model.binding, ExistingAIOrchestrationBindingReadModel)
