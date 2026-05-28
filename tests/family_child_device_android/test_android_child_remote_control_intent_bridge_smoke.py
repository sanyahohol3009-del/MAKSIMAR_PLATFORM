import pytest

from ANDROID_SHELL.family_child_device.android_child_remote_control_intent_bridge import (
    AndroidChildRemoteControlIntentBridge,
)
from MAKSIMAR_CORE_LIB.family_child_device_control.child_remote_control_intent_contract import (
    ChildRemoteControlIntentContract,
)


def test_android_child_remote_control_intent_bridge_smoke() -> None:
    bridge = AndroidChildRemoteControlIntentBridge(
        intent_id="android_child_remote_intent_001",
        child_device_id="child_android_device_001",
        guardian_id="guardian_001",
        intent_type="touch_control",
        guardian_authority_verified=True,
        family_policy_enabled=True,
        audit_required=True,
        visible_child_device_status_required=True,
        dashboard_bypass_allowed=False,
        android_platform_api_call_allowed=False,
        runtime_execution_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
    )

    contract = bridge.build_intent_contract()
    read_model = bridge.to_read_model()

    assert isinstance(contract, ChildRemoteControlIntentContract)
    assert contract.intent_id == "android_child_remote_intent_001"
    assert contract.child_device_id == "child_android_device_001"
    assert contract.guardian_id == "guardian_001"
    assert contract.intent_type == "touch_control"
    assert contract.guardian_authority_verified is True
    assert contract.family_policy_enabled is True
    assert contract.audit_required is True
    assert contract.visible_child_device_status_required is True
    assert contract.dashboard_bypass_allowed is False
    assert contract.runtime_execution_allowed is False

    assert read_model["bridge"] == "child_remote_control_intent"
    assert read_model["android_platform_api_call_allowed"] is False
    assert read_model["runtime_execution_allowed"] is False


def test_android_child_remote_control_intent_bridge_rejects_runtime_execution() -> None:
    with pytest.raises(ValueError, match="runtime_execution_allowed must be False"):
        AndroidChildRemoteControlIntentBridge(
            intent_id="android_child_remote_intent_001",
            child_device_id="child_android_device_001",
            guardian_id="guardian_001",
            intent_type="touch_control",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            audit_required=True,
            visible_child_device_status_required=True,
            dashboard_bypass_allowed=False,
            android_platform_api_call_allowed=False,
            runtime_execution_allowed=True,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
