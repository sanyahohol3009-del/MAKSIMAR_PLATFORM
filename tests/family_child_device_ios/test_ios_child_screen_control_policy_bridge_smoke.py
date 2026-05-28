import pytest

from IOS_SHELL.family_child_device.ios_child_screen_control_policy_bridge import (
    IOSChildScreenControlPolicyBridge,
)
from MAKSIMAR_CORE_LIB.family_child_device_control.child_screen_control_policy_contract import (
    ChildScreenControlPolicyContract,
)


def test_ios_child_screen_control_policy_bridge_smoke() -> None:
    bridge = IOSChildScreenControlPolicyBridge(
        policy_id="ios_child_screen_policy_001",
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
        ios_platform_api_call_allowed=False,
        screen_capture_runtime_allowed=False,
        touch_execution_allowed=False,
        keyboard_execution_allowed=False,
        runtime_execution_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
    )

    contract = bridge.build_policy_contract()
    read_model = bridge.to_read_model()

    assert isinstance(contract, ChildScreenControlPolicyContract)
    assert contract.policy_id == "ios_child_screen_policy_001"
    assert contract.device_profile == "child_managed_device"
    assert contract.guardian_authority_verified is True
    assert contract.family_policy_enabled is True
    assert contract.audit_required is True
    assert contract.visible_child_device_status_required is True
    assert contract.dashboard_bypass_allowed is False
    assert contract.screen_view_allowed_by_guardian_policy is True
    assert contract.screenshot_allowed_by_guardian_policy is True
    assert contract.touch_control_allowed_by_guardian_policy is True

    assert read_model["bridge"] == "child_screen_control_policy"
    assert read_model["ios_platform_api_call_allowed"] is False
    assert read_model["screen_capture_runtime_allowed"] is False
    assert read_model["touch_execution_allowed"] is False
    assert read_model["keyboard_execution_allowed"] is False
    assert read_model["runtime_execution_allowed"] is False


def test_ios_child_screen_control_policy_bridge_rejects_screen_capture_runtime() -> None:
    with pytest.raises(ValueError, match="screen_capture_runtime_allowed must be False"):
        IOSChildScreenControlPolicyBridge(
            policy_id="ios_child_screen_policy_001",
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
            ios_platform_api_call_allowed=False,
            screen_capture_runtime_allowed=True,
            touch_execution_allowed=False,
            keyboard_execution_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
