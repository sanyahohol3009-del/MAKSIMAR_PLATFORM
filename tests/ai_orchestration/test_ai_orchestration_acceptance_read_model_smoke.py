from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.ai_orchestration_acceptance_read_model import (
    AIOrchestrationAcceptanceReadModel,
    build_ai_orchestration_acceptance_read_model,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.ai_orchestration_read_model import (
    build_default_ai_orchestration_read_model,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.ai_router_binding_contract import (
    build_ai_router_binding_contract,
)


def test_ai_orchestration_acceptance_read_model_is_ready_and_inert() -> None:
    read_model = build_ai_orchestration_acceptance_read_model()

    assert read_model.read_model_id == "ai_orchestration_acceptance_read_model_v1"
    assert read_model.ai_services_accounted is True
    assert read_model.workers_accounted is True
    assert read_model.ai_router_binding_accounted is True
    assert read_model.manifest_present is True
    assert read_model.proposal_only is True
    assert read_model.direct_execution_blocked is True
    assert read_model.action_library_direct_execution_allowed is False
    assert read_model.workflow_engine_direct_execution_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.production_deployment_allowed is False
    assert read_model.public_exposure_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.read_only is True
    assert read_model.acceptance_ready is True


def test_ai_orchestration_acceptance_rejects_missing_ai_services_accounting() -> None:
    with pytest.raises(ValueError, match="ai_services_accounted"):
        AIOrchestrationAcceptanceReadModel(
            read_model_id="bad",
            ai_orchestration_read_model=build_default_ai_orchestration_read_model(),
            ai_router_binding_contract=build_ai_router_binding_contract(),
            ai_services_accounted=False,
            workers_accounted=True,
            ai_router_binding_accounted=True,
            manifest_present=True,
            proposal_only=True,
            direct_execution_blocked=True,
            action_library_direct_execution_allowed=False,
            workflow_engine_direct_execution_allowed=False,
            runtime_mutation_allowed=False,
            production_deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            acceptance_ready=True,
            reason_codes=("bad",),
        )


def test_ai_orchestration_acceptance_rejects_action_library_direct_execution() -> None:
    with pytest.raises(ValueError, match="action_library_direct_execution_allowed"):
        AIOrchestrationAcceptanceReadModel(
            read_model_id="bad",
            ai_orchestration_read_model=build_default_ai_orchestration_read_model(),
            ai_router_binding_contract=build_ai_router_binding_contract(),
            ai_services_accounted=True,
            workers_accounted=True,
            ai_router_binding_accounted=True,
            manifest_present=True,
            proposal_only=True,
            direct_execution_blocked=True,
            action_library_direct_execution_allowed=True,
            workflow_engine_direct_execution_allowed=False,
            runtime_mutation_allowed=False,
            production_deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            acceptance_ready=True,
            reason_codes=("bad",),
        )


def test_ai_orchestration_acceptance_rejects_workflow_engine_direct_execution() -> None:
    with pytest.raises(ValueError, match="workflow_engine_direct_execution_allowed"):
        AIOrchestrationAcceptanceReadModel(
            read_model_id="bad",
            ai_orchestration_read_model=build_default_ai_orchestration_read_model(),
            ai_router_binding_contract=build_ai_router_binding_contract(),
            ai_services_accounted=True,
            workers_accounted=True,
            ai_router_binding_accounted=True,
            manifest_present=True,
            proposal_only=True,
            direct_execution_blocked=True,
            action_library_direct_execution_allowed=False,
            workflow_engine_direct_execution_allowed=True,
            runtime_mutation_allowed=False,
            production_deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            acceptance_ready=True,
            reason_codes=("bad",),
        )
