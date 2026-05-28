import pytest

from ANDROID_SHELL.family_child_device.android_child_device_audit_bridge import (
    AndroidChildDeviceAuditBridge,
)
from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_audit_contract import (
    ChildDeviceAuditContract,
)


def test_android_child_device_audit_bridge_smoke() -> None:
    bridge = AndroidChildDeviceAuditBridge(
        audit_event_id="android_child_audit_001",
        child_device_id="child_android_device_001",
        guardian_id="guardian_001",
        action="screen_view_requested",
        event_epoch_ms=1000,
        append_only=True,
        visible_to_guardian=True,
        visible_on_child_device=True,
        contains_pixel_payload=False,
        dashboard_bypass_allowed=False,
        android_platform_api_call_allowed=False,
        runtime_execution_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
    )

    contract = bridge.build_audit_contract()
    read_model = bridge.to_read_model()

    assert isinstance(contract, ChildDeviceAuditContract)
    assert contract.audit_event_id == "android_child_audit_001"
    assert contract.child_device_id == "child_android_device_001"
    assert contract.guardian_id == "guardian_001"
    assert contract.action == "screen_view_requested"
    assert contract.event_epoch_ms == 1000
    assert contract.append_only is True
    assert contract.visible_to_guardian is True
    assert contract.visible_on_child_device is True
    assert contract.contains_pixel_payload is False
    assert contract.dashboard_bypass_allowed is False

    assert read_model["bridge"] == "child_device_audit"
    assert read_model["contains_pixel_payload"] is False
    assert read_model["android_platform_api_call_allowed"] is False
    assert read_model["runtime_execution_allowed"] is False


def test_android_child_device_audit_bridge_rejects_pixel_payload() -> None:
    with pytest.raises(ValueError, match="contains_pixel_payload must be False"):
        AndroidChildDeviceAuditBridge(
            audit_event_id="android_child_audit_001",
            child_device_id="child_android_device_001",
            guardian_id="guardian_001",
            action="screen_view_requested",
            event_epoch_ms=1000,
            append_only=True,
            visible_to_guardian=True,
            visible_on_child_device=True,
            contains_pixel_payload=True,
            dashboard_bypass_allowed=False,
            android_platform_api_call_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
