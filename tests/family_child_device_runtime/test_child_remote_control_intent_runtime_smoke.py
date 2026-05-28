from MAKSIMAR_CORE_LIB.family_child_device_control.child_remote_control_intent_contract import (
    ChildRemoteControlIntentContract,
)
from MAKSIMAR_SERVER.FAMILY_CHILD_DEVICE_RUNTIME.child_remote_control_intent_runtime import (
    ChildRemoteControlIntentRuntime,
)


def test_child_remote_control_intent_runtime_smoke() -> None:
    intent = ChildRemoteControlIntentContract(
        intent_id="child_remote_intent_001",
        child_device_id="child_device_001",
        guardian_id="guardian_001",
        intent_type="touch_control",
        guardian_authority_verified=True,
        family_policy_enabled=True,
        audit_required=True,
        visible_child_device_status_required=True,
        dashboard_bypass_allowed=False,
        runtime_execution_allowed=False,
    )

    decision = ChildRemoteControlIntentRuntime().evaluate(intent)

    assert decision.policy_intent_accepted is True
    assert decision.runtime_execution_allowed is False
