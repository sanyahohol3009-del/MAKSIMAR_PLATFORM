import pytest

from IOS_SHELL.family_child_device.ios_child_device_profile_bridge import (
    IOSChildDeviceProfileBridge,
)
from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_profile_contract import (
    ChildDeviceProfileContract,
)


def test_ios_child_device_profile_bridge_smoke() -> None:
    bridge = IOSChildDeviceProfileBridge.default(
        child_device_id="child_ios_device_001",
        child_profile_id="child_profile_001",
    )

    contract = bridge.build_profile_contract()
    read_model = bridge.to_read_model()

    assert isinstance(contract, ChildDeviceProfileContract)
    assert contract.child_device_id == "child_ios_device_001"
    assert contract.child_profile_id == "child_profile_001"
    assert contract.device_profile == "child_managed_device"
    assert contract.family_policy_enabled is True
    assert contract.visible_child_device_status_required is True
    assert contract.audit_required is True
    assert contract.dashboard_bypass_allowed is False

    assert read_model["shell"] == "IOS_SHELL"
    assert read_model["bridge"] == "family_child_device_profile"
    assert read_model["dashboard_section"] == "Family / Children"
    assert read_model["ios_platform_api_call_allowed"] is False
    assert read_model["runtime_execution_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["core_write_allowed"] is False
    assert read_model["source_of_truth_override_allowed"] is False


def test_ios_child_device_profile_bridge_rejects_platform_api_call() -> None:
    with pytest.raises(ValueError, match="ios_platform_api_call_allowed must be False"):
        IOSChildDeviceProfileBridge(
            child_device_id="child_ios_device_001",
            child_profile_id="child_profile_001",
            device_profile="child_managed_device",
            family_policy_enabled=True,
            visible_child_device_status_required=True,
            audit_required=True,
            dashboard_bypass_allowed=False,
            ios_platform_api_call_allowed=True,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )
