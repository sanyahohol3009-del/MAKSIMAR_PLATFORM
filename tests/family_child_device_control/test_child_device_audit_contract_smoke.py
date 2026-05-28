import pytest

from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_audit_contract import (
    ChildDeviceAuditContract,
)


def test_child_device_audit_contract_smoke() -> None:
    event = ChildDeviceAuditContract(
        audit_event_id="child_audit_001",
        child_device_id="child_device_001",
        guardian_id="guardian_001",
        action="touch_control_requested",
        event_epoch_ms=1000,
        append_only=True,
        visible_to_guardian=True,
        visible_on_child_device=True,
        contains_pixel_payload=False,
        dashboard_bypass_allowed=False,
    )

    assert event.append_only is True


def test_child_device_audit_rejects_hidden_child_device_status() -> None:
    with pytest.raises(ValueError, match="visible_on_child_device must be True"):
        ChildDeviceAuditContract(
            audit_event_id="child_audit_bad",
            child_device_id="child_device_001",
            guardian_id="guardian_001",
            action="touch_control_requested",
            event_epoch_ms=1000,
            append_only=True,
            visible_to_guardian=True,
            visible_on_child_device=False,
            contains_pixel_payload=False,
            dashboard_bypass_allowed=False,
        )
