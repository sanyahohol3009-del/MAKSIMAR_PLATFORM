from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration import (
    ModelRouterContract,
    ModelRouterReadModel,
    build_default_model_request_model,
    build_model_router_contract,
    build_model_router_read_model,
)


def test_model_router_contract_is_contract_only_and_non_executing() -> None:
    contract = build_model_router_contract()

    assert contract.contract_id == "model_router_contract_v1"
    assert contract.contract_only is True
    assert contract.execution_allowed is False
    assert contract.dashboard_safe is True
    assert contract.read_only is True
    assert contract.read_model.tool_call_allowed is False
    assert contract.read_model.execution_allowed is False
    assert contract.read_model.direct_action_execution_allowed is False
    assert contract.read_model.workflow_engine_execution_allowed is False


def test_model_router_read_model_exposes_dashboard_fields() -> None:
    request = build_default_model_request_model()
    read_model = build_model_router_read_model(request)

    assert read_model.request_id == request.request_id
    assert read_model.requested_capability == request.requested_capability
    assert read_model.selected_model == "existing_ai_router_selected_model"
    assert read_model.model_route_reason == "existing_ai_router_binding_reference"
    assert read_model.tool_call_requested is False
    assert read_model.tool_call_allowed is False
    assert read_model.execution_allowed is False
    assert read_model.dashboard_safe is True


def test_model_router_read_model_rejects_execution_allowed() -> None:
    with pytest.raises(ValueError, match="execution_allowed"):
        ModelRouterReadModel(
            request_id="bad_request",
            requested_capability="general_reasoning",
            selected_model="model",
            model_route_reason="test",
            tool_call_requested=False,
            tool_call_allowed=False,
            execution_allowed=True,
            direct_action_execution_allowed=False,
            workflow_engine_execution_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_model_router_contract_rejects_execution_allowed() -> None:
    contract = build_model_router_contract()

    with pytest.raises(ValueError, match="execution_allowed"):
        ModelRouterContract(
            contract_id="bad_contract",
            request=contract.request,
            response=contract.response,
            agent_plan=contract.agent_plan,
            tool_call_boundary=contract.tool_call_boundary,
            read_model=contract.read_model,
            contract_only=True,
            execution_allowed=True,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
