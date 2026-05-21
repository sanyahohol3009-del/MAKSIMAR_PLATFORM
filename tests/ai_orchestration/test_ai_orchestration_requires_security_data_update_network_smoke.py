from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.orchestration_policy import (
    AIOrchestrationFoundationReadinessModel,
    AIOrchestrationPolicy,
    build_default_ai_orchestration_foundation_readiness_model,
)


def test_ai_orchestration_foundation_readiness_requires_all_green() -> None:
    readiness = build_default_ai_orchestration_foundation_readiness_model()

    assert readiness.security_layer_green is True
    assert readiness.data_plane_green is True
    assert readiness.update_recovery_green is True
    assert readiness.network_containerization_green is True
    assert readiness.all_required_foundations_green is True
    assert readiness.dashboard_safe is True
    assert readiness.read_only is True


def test_ai_orchestration_foundation_readiness_rejects_security_red() -> None:
    with pytest.raises(ValueError, match="security_layer_green"):
        AIOrchestrationFoundationReadinessModel(
            readiness_id="bad",
            security_layer_green=False,
            data_plane_green=True,
            update_recovery_green=True,
            network_containerization_green=True,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_ai_orchestration_policy_rejects_incomplete_foundation_readiness() -> None:
    with pytest.raises(ValueError, match="data_plane_green"):
        AIOrchestrationFoundationReadinessModel(
            readiness_id="bad",
            security_layer_green=True,
            data_plane_green=False,
            update_recovery_green=True,
            network_containerization_green=True,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_ai_orchestration_policy_accepts_complete_foundation_readiness() -> None:
    readiness = build_default_ai_orchestration_foundation_readiness_model()

    policy = AIOrchestrationPolicy(
        policy_id="ai_orchestration_policy_v1",
        foundation_readiness=readiness,
        may_propose=True,
        may_apply=False,
        direct_action_execution_allowed=False,
        workflow_engine_execution_allowed=False,
        direct_autonomous_execution_allowed=False,
        runtime_mutation_allowed=False,
        production_deployment_allowed=False,
        public_exposure_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=("accepted",),
    )

    assert policy.foundation_readiness.all_required_foundations_green is True
    assert policy.may_propose is True
    assert policy.may_apply is False
