from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.tool_call_boundary_models import (
    ToolCallBoundaryModel,
    build_default_tool_call_boundary_model,
)


def test_default_tool_call_boundary_is_proposal_only_and_blocked() -> None:
    boundary = build_default_tool_call_boundary_model(tool_call_requested=True)

    assert boundary.boundary_id == "tool_call_boundary_v1"
    assert boundary.proposal_boundary_only is True
    assert boundary.tool_call_requested is True
    assert boundary.tool_call_allowed is False
    assert boundary.execution_allowed is False
    assert boundary.action_library_execution_allowed is False
    assert boundary.workflow_engine_execution_allowed is False
    assert boundary.direct_autonomous_execution_allowed is False
    assert boundary.runtime_mutation_allowed is False
    assert boundary.dashboard_safe is True
    assert boundary.read_only is True


def test_tool_call_boundary_rejects_tool_call_allowed() -> None:
    with pytest.raises(ValueError, match="tool_call_allowed"):
        ToolCallBoundaryModel(
            boundary_id="bad_boundary",
            proposal_boundary_only=True,
            tool_call_requested=True,
            tool_call_allowed=True,
            execution_allowed=False,
            action_library_execution_allowed=False,
            workflow_engine_execution_allowed=False,
            direct_autonomous_execution_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_tool_call_boundary_rejects_execution_allowed() -> None:
    with pytest.raises(ValueError, match="execution_allowed"):
        ToolCallBoundaryModel(
            boundary_id="bad_boundary",
            proposal_boundary_only=True,
            tool_call_requested=True,
            tool_call_allowed=False,
            execution_allowed=True,
            action_library_execution_allowed=False,
            workflow_engine_execution_allowed=False,
            direct_autonomous_execution_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
