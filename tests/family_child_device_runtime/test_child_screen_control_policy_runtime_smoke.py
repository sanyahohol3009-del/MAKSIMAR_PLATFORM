from MAKSIMAR_CORE_LIB.family_child_device_control.child_screen_control_policy_contract import (
    ChildScreenControlPolicyContract,
)
from MAKSIMAR_SERVER.FAMILY_CHILD_DEVICE_RUNTIME.child_screen_control_policy_runtime import (
    ChildScreenControlPolicyRuntime,
)


def test_child_screen_control_policy_runtime_smoke() -> None:
    policy = ChildScreenControlPolicyContract(
        policy_id="child_screen_policy_001",
        device_profile="child_managed_device",
        guardian_authority_verified=True,
        family_policy_enabled=True,
        audit_required=True,
        visible_child_device_status_required=True,
        dashboard_bypass_allowed=False,
        screen_view_allowed_by_guardian_policy=True,
        screenshot_allowed_by_guardian_policy=True,
        screen_recording_allowed_by_guardian_policy=False,
        touch_control_allowed_by_guardian_policy=True,
        keyboard_input_allowed_by_guardian_policy=False,
    )

    decision = ChildScreenControlPolicyRuntime().evaluate(policy)

    assert decision.screen_view_allowed is True
    assert decision.screenshot_allowed is True
    assert decision.interactive_control_requested is True
    assert decision.runtime_execution_allowed is False
