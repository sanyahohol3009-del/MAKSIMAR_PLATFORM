import pytest

from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_profile_contract import (
    ChildDeviceProfileContract,
)
from MAKSIMAR_SERVER.FAMILY_CHILD_DEVICE_RUNTIME.child_device_session_registry import (
    ChildDeviceSessionRegistry,
)


def _profile() -> ChildDeviceProfileContract:
    return ChildDeviceProfileContract(
        child_device_id="child_device_001",
        child_profile_id="child_profile_001",
        device_profile="child_managed_device",
        family_policy_enabled=True,
        visible_child_device_status_required=True,
        audit_required=True,
        dashboard_bypass_allowed=False,
    )


def test_child_device_session_registry_smoke() -> None:
    registry = ChildDeviceSessionRegistry()
    record = registry.register(_profile())

    assert record.profile.child_device_id == "child_device_001"
    assert registry.contains("child_device_001") is True
    assert registry.to_read_model()["dashboard_section"] == "Family / Children"
    assert registry.to_read_model()["dashboard_bypass_allowed"] is False


def test_child_device_session_registry_rejects_duplicate() -> None:
    registry = ChildDeviceSessionRegistry()
    registry.register(_profile())

    with pytest.raises(ValueError, match="child device already registered"):
        registry.register(_profile())
