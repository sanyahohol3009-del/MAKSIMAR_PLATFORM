from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration import (
    AIOrchestrationPolicy,
    AIOrchestrationReadModel,
    build_default_ai_orchestration_foundation_readiness_model,
    build_default_ai_orchestration_policy,
    build_default_ai_orchestration_read_model,
)


def test_ai_orchestration_policy_allows_only_proposal_not_apply() -> None:
    policy = build_default_ai_orchestration_policy()

    assert policy.may_propose is True
    assert policy.may_apply is False
    assert policy.direct_action_execution_allowed is False
    assert policy.workflow_engine_execution_allowed is False
    assert policy.direct_autonomous_execution_allowed is False
    assert policy.runtime_mutation_allowed is False
    assert policy.production_deployment_allowed is False
    assert policy.public_exposure_allowed is False
    assert policy.dashboard_safe is True
    assert policy.read_only is True


def test_ai_orchestration_policy_rejects_direct_action_execution() -> None:
    readiness = build_default_ai_orchestration_foundation_readiness_model()

    with pytest.raises(ValueError, match="direct_action_execution_allowed"):
        AIOrchestrationPolicy(
            policy_id="bad",
            foundation_readiness=readiness,
            may_propose=True,
            may_apply=False,
            direct_action_execution_allowed=True,
            workflow_engine_execution_allowed=False,
            direct_autonomous_execution_allowed=False,
            runtime_mutation_allowed=False,
            production_deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_ai_orchestration_policy_rejects_workflow_engine_execution() -> None:
    readiness = build_default_ai_orchestration_foundation_readiness_model()

    with pytest.raises(ValueError, match="workflow_engine_execution_allowed"):
        AIOrchestrationPolicy(
            policy_id="bad",
            foundation_readiness=readiness,
            may_propose=True,
            may_apply=False,
            direct_action_execution_allowed=False,
            workflow_engine_execution_allowed=True,
            direct_autonomous_execution_allowed=False,
            runtime_mutation_allowed=False,
            production_deployment_allowed=False,
            public_exposure_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_ai_orchestration_read_model_exposes_proposal_provenance_budget_feedback() -> None:
    read_model = build_default_ai_orchestration_read_model()

    assert isinstance(read_model, AIOrchestrationReadModel)
    assert read_model.read_model_id == "ai_orchestration_read_model_v1"
    assert read_model.proposal_ready is True
    assert read_model.provenance_ready is True
    assert read_model.budget_guard_ready is True
    assert read_model.feedback_ready is True
    assert read_model.may_propose is True
    assert read_model.may_apply is False
    assert read_model.execution_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.dashboard_safe is True
