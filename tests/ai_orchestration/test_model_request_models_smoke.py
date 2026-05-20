from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.model_request_models import (
    ModelRequestModel,
    build_default_model_request_model,
)


def test_default_model_request_is_dashboard_safe_and_read_only() -> None:
    request = build_default_model_request_model()

    assert request.request_id == "model_request_v1"
    assert request.requested_capability == "general_reasoning"
    assert request.tool_call_requested is False
    assert request.direct_action_requested is False
    assert request.workflow_execution_requested is False
    assert request.dashboard_safe is True
    assert request.read_only is True


def test_model_request_rejects_direct_action_request() -> None:
    with pytest.raises(ValueError, match="direct_action_requested"):
        ModelRequestModel(
            request_id="bad_request",
            requested_capability="general_reasoning",
            requester_id="test",
            input_reference="input",
            tool_call_requested=False,
            direct_action_requested=True,
            workflow_execution_requested=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_model_request_rejects_workflow_execution_request() -> None:
    with pytest.raises(ValueError, match="workflow_execution_requested"):
        ModelRequestModel(
            request_id="bad_request",
            requested_capability="general_reasoning",
            requester_id="test",
            input_reference="input",
            tool_call_requested=False,
            direct_action_requested=False,
            workflow_execution_requested=True,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
