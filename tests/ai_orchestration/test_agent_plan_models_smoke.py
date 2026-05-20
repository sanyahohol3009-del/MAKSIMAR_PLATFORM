from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.agent_plan_models import (
    AgentPlanModel,
    build_default_agent_plan_model,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.tool_call_boundary_models import (
    build_default_tool_call_boundary_model,
)


def test_default_agent_plan_is_proposal_only_and_non_executable() -> None:
    plan = build_default_agent_plan_model()

    assert plan.plan_id == "agent_plan_v1"
    assert plan.proposal_only is True
    assert plan.execution_allowed is False
    assert plan.action_library_execution_allowed is False
    assert plan.workflow_engine_execution_allowed is False
    assert plan.direct_autonomous_execution_allowed is False
    assert plan.runtime_mutation_allowed is False
    assert plan.dashboard_safe is True
    assert plan.read_only is True
    assert plan.tool_call_boundary.tool_call_allowed is False


def test_agent_plan_rejects_execution_allowed() -> None:
    with pytest.raises(ValueError, match="execution_allowed"):
        AgentPlanModel(
            plan_id="bad_plan",
            request_id="model_request_v1",
            plan_steps=("inspect",),
            proposal_only=True,
            tool_call_boundary=build_default_tool_call_boundary_model(),
            execution_allowed=True,
            action_library_execution_allowed=False,
            workflow_engine_execution_allowed=False,
            direct_autonomous_execution_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_agent_plan_rejects_workflow_engine_execution_allowed() -> None:
    with pytest.raises(ValueError, match="workflow_engine_execution_allowed"):
        AgentPlanModel(
            plan_id="bad_plan",
            request_id="model_request_v1",
            plan_steps=("inspect",),
            proposal_only=True,
            tool_call_boundary=build_default_tool_call_boundary_model(),
            execution_allowed=False,
            action_library_execution_allowed=False,
            workflow_engine_execution_allowed=True,
            direct_autonomous_execution_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
