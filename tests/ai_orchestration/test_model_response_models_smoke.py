from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.model_response_models import (
    ModelResponseModel,
    build_default_model_response_model,
)


def test_default_model_response_blocks_tool_call_and_execution() -> None:
    response = build_default_model_response_model()

    assert response.response_id == "model_response_v1"
    assert response.response_ready is True
    assert response.tool_call_allowed is False
    assert response.execution_allowed is False
    assert response.dashboard_safe is True
    assert response.read_only is True


def test_model_response_rejects_tool_call_allowed() -> None:
    with pytest.raises(ValueError, match="tool_call_allowed"):
        ModelResponseModel(
            response_id="bad_response",
            request_id="model_request_v1",
            selected_model="model",
            response_summary="summary",
            response_ready=True,
            tool_call_allowed=True,
            execution_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_model_response_rejects_execution_allowed() -> None:
    with pytest.raises(ValueError, match="execution_allowed"):
        ModelResponseModel(
            response_id="bad_response",
            request_id="model_request_v1",
            selected_model="model",
            response_summary="summary",
            response_ready=True,
            tool_call_allowed=False,
            execution_allowed=True,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
