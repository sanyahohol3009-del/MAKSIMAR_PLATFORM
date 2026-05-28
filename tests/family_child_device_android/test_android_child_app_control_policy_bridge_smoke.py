import pytest

from ANDROID_SHELL.family_child_device.android_child_app_control_policy_bridge import (
    AndroidChildAppControlPolicyBridge,
)
from MAKSIMAR_CORE_LIB.family_child_device_control.child_app_control_policy_contract import (
    ChildAppControlPolicyContract,
)


def test_android_child_app_control_policy_bridge_smoke() -> None:
    bridge = AndroidChildAppControlPolicyBridge(
        policy_id="android_child_app_policy_001",
        child_device_id="child_android_device_001",
        guardian_authority_verified=True,
        family_policy_enabled=True,
        app_blocking_allowed_by_guardian_policy=True,
        install_approval_required=True,
        audit_required=True,
        dashboard_bypass_allowed=False,
        android_platform_api_call_allowed=False,
        app_control_runtime_allowed=False,
        runtime_execution_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
    )

    contract = bridge.build_policy_contract()
    read_model = bridge.to_read_model()

    assert isinstance(contract, ChildAppControlPolicyContract)
    assert contract.policy_id == "android_child_app_policy_001"
    assert contract.child_device_id == "child_android_device_001"
    assert contract.guardian_authority_verified is True
    assert contract.family_policy_enabled is True
    assert contract.app_blocking_allowed_by_guardian_policy is True
    assert contract.install_approval_required is True
    assert contract.audit_required is True
    assert contract.dashboard_bypass_allowed is False
    assert contract.runtime_execution_allowed is False

    assert read_model["bridge"] == "child_app_control_policy"
    assert read_model["android_platform_api_call_allowed"] is False
    assert read_model["app_control_runtime_allowed"] is False
    assert read_model["runtime_execution_allowed"] is False


def test_android_child_app_control_policy_bridge_rejects_app_control_runtime() -> None:
    with pytest.raises(ValueError, match="app_control_runtime_allowed must be False"):
        AndroidChildAppControlPolicyBridge(
            policy_id="android_child_app_policy_001",
            child_device_id="child_android_device_001",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            app_blocking_allowed_by_guardian_policy=True,
            install_approval_required=True,
            audit_required=True,
            dashboard_bypass_allowed=False,
            android_platform_api_call_allowed=False,
            app_control_runtime_allowed=True,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
