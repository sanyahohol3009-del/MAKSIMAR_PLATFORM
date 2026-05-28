import pytest

from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_profile_contract import (
    ChildDeviceProfileContract,
)


def test_child_device_profile_contract_smoke() -> None:
    profile = ChildDeviceProfileContract(
        child_device_id="child_device_001",
        child_profile_id="child_profile_001",
        device_profile="child_managed_device",
        family_policy_enabled=True,
        visible_child_device_status_required=True,
        audit_required=True,
        dashboard_bypass_allowed=False,
    )

    assert profile.is_child_managed() is True


def test_child_device_profile_rejects_non_child_device() -> None:
    with pytest.raises(ValueError, match="device_profile must be child_managed_device"):
        ChildDeviceProfileContract(
            child_device_id="adult_device_001",
            child_profile_id="child_profile_001",
            device_profile="adult_personal_device",
            family_policy_enabled=True,
            visible_child_device_status_required=True,
            audit_required=True,
            dashboard_bypass_allowed=False,
        )
