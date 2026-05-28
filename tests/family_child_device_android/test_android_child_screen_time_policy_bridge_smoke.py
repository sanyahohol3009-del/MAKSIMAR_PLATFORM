import pytest

from ANDROID_SHELL.family_child_device.android_child_screen_time_policy_bridge import (
    AndroidChildScreenTimePolicyBridge,
)
from MAKSIMAR_CORE_LIB.family_child_device_control.child_screen_time_policy_contract import (
    ChildScreenTimePolicyContract,
)


def test_android_child_screen_time_policy_bridge_smoke() -> None:
    bridge = AndroidChildScreenTimePolicyBridge(
        policy_id="android_child_time_policy_001",
        child_device_id="child_android_device_001",
        guardian_authority_verified=True,
        family_policy_enabled=True,
        daily_limit_minutes=90,
        emergency_lock_allowed_by_guardian_policy=True,
        audit_required=True,
        dashboard_bypass_allowed=False,
        android_platform_api_call_allowed=False,
        screen_time_enforcement_runtime_allowed=False,
        emergency_lock_runtime_allowed=False,
        runtime_execution_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
    )

    contract = bridge.build_policy_contract()
    read_model = bridge.to_read_model()

    assert isinstance(contract, ChildScreenTimePolicyContract)
    assert contract.policy_id == "android_child_time_policy_001"
    assert contract.child_device_id == "child_android_device_001"
    assert contract.guardian_authority_verified is True
    assert contract.family_policy_enabled is True
    assert contract.daily_limit_minutes == 90
    assert contract.emergency_lock_allowed_by_guardian_policy is True
    assert contract.audit_required is True
    assert contract.dashboard_bypass_allowed is False
    assert contract.runtime_execution_allowed is False

    assert read_model["bridge"] == "child_screen_time_policy"
    assert read_model["android_platform_api_call_allowed"] is False
    assert read_model["screen_time_enforcement_runtime_allowed"] is False
    assert read_model["emergency_lock_runtime_allowed"] is False
    assert read_model["runtime_execution_allowed"] is False


def test_android_child_screen_time_policy_bridge_rejects_emergency_lock_runtime() -> None:
    with pytest.raises(ValueError, match="emergency_lock_runtime_allowed must be False"):
        AndroidChildScreenTimePolicyBridge(
            policy_id="android_child_time_policy_001",
            child_device_id="child_android_device_001",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            daily_limit_minutes=90,
            emergency_lock_allowed_by_guardian_policy=True,
            audit_required=True,
            dashboard_bypass_allowed=False,
            android_platform_api_call_allowed=False,
            screen_time_enforcement_runtime_allowed=False,
            emergency_lock_runtime_allowed=True,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
