import pytest

from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_profile_contract import (
    ChildDeviceProfileContract,
)


def test_child_control_rejects_dashboard_bypass_smoke() -> None:
    with pytest.raises(ValueError, match="dashboard_bypass_allowed must be False"):
        ChildDeviceProfileContract(
            child_device_id="child_device_001",
            child_profile_id="child_profile_001",
            device_profile="child_managed_device",
            family_policy_enabled=True,
            visible_child_device_status_required=True,
            audit_required=True,
            dashboard_bypass_allowed=True,
        )
