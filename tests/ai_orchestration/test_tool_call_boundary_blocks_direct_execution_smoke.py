from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.tool_call_boundary_models import ToolCallBoundaryModel


def test_tool_call_boundary_blocks_direct_action_library_execution() -> None:
    with pytest.raises(ValueError, match="action_library_execution_allowed"):
        ToolCallBoundaryModel(
            boundary_id="bad_boundary",
            proposal_boundary_only=True,
            tool_call_requested=True,
            tool_call_allowed=False,
            execution_allowed=False,
            action_library_execution_allowed=True,
            workflow_engine_execution_allowed=False,
            direct_autonomous_execution_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_tool_call_boundary_blocks_direct_workflow_engine_execution() -> None:
    with pytest.raises(ValueError, match="workflow_engine_execution_allowed"):
        ToolCallBoundaryModel(
            boundary_id="bad_boundary",
            proposal_boundary_only=True,
            tool_call_requested=True,
            tool_call_allowed=False,
            execution_allowed=False,
            action_library_execution_allowed=False,
            workflow_engine_execution_allowed=True,
            direct_autonomous_execution_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_tool_call_boundary_blocks_direct_autonomous_execution() -> None:
    with pytest.raises(ValueError, match="direct_autonomous_execution_allowed"):
        ToolCallBoundaryModel(
            boundary_id="bad_boundary",
            proposal_boundary_only=True,
            tool_call_requested=True,
            tool_call_allowed=False,
            execution_allowed=False,
            action_library_execution_allowed=False,
            workflow_engine_execution_allowed=False,
            direct_autonomous_execution_allowed=True,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
