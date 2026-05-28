import pytest

from MAKSIMAR_CORE_LIB.family_child_device_control.child_screen_control_policy_contract import (
    ChildScreenControlPolicyContract,
)


def test_child_screen_control_policy_contract_smoke() -> None:
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

    assert policy.allows_interactive_control() is True


def test_child_screen_control_policy_rejects_dashboard_bypass() -> None:
    with pytest.raises(ValueError, match="dashboard_bypass_allowed must be False"):
        ChildScreenControlPolicyContract(
            policy_id="child_screen_policy_bad",
            device_profile="child_managed_device",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            audit_required=True,
            visible_child_device_status_required=True,
            dashboard_bypass_allowed=True,
            screen_view_allowed_by_guardian_policy=True,
            screenshot_allowed_by_guardian_policy=True,
            screen_recording_allowed_by_guardian_policy=False,
            touch_control_allowed_by_guardian_policy=True,
            keyboard_input_allowed_by_guardian_policy=False,
        )
