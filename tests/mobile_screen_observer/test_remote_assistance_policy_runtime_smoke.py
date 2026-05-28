from MAKSIMAR_CORE_LIB.mobile_screen_observer.remote_assistance_intent_contract import (
    RemoteAssistanceIntentContract,
)
from MAKSIMAR_SERVER.MOBILE_SCREEN_OBSERVER_RUNTIME.remote_assistance_policy_runtime import (
    RemoteAssistancePolicyRuntime,
)


def test_remote_assistance_policy_runtime_smoke() -> None:
    intent = RemoteAssistanceIntentContract(
        intent_id="remote_assist_001",
        session_id="screen_session_001",
        intent_state="approval_required",
        owner_approval_required=True,
        consent_required=True,
        audit_required=True,
        disabled_by_default=True,
        dashboard_direct_execute_allowed=False,
        device_control_execution_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
    )

    decision = RemoteAssistancePolicyRuntime().evaluate(intent)

    assert decision.allowed_to_execute is False
    assert decision.approval_required is True
    assert "non_executing" in decision.reason
