import pytest

from IOS_SHELL.family_child_device.ios_child_device_profile_bridge import (
    IOSChildDeviceProfileBridge,
)


def test_ios_child_bridge_rejects_dashboard_bypass_smoke() -> None:
    with pytest.raises(ValueError, match="dashboard_bypass_allowed must be False"):
        IOSChildDeviceProfileBridge(
            child_device_id="child_ios_device_001",
            child_profile_id="child_profile_001",
            device_profile="child_managed_device",
            family_policy_enabled=True,
            visible_child_device_status_required=True,
            audit_required=True,
            dashboard_bypass_allowed=True,
            ios_platform_api_call_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )
