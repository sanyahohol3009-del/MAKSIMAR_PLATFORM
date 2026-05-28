import pytest

from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_audit_contract import (
    ChildDeviceAuditContract,
)
from MAKSIMAR_SERVER.FAMILY_CHILD_DEVICE_RUNTIME.child_device_audit_runtime import (
    ChildDeviceAuditRuntime,
)


def _event() -> ChildDeviceAuditContract:
    return ChildDeviceAuditContract(
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


def test_child_device_audit_runtime_smoke() -> None:
    runtime = ChildDeviceAuditRuntime()
    runtime.append(_event())

    assert runtime.list_event_ids() == ("child_audit_001",)
    assert runtime.to_read_model()["append_only"] is True
    assert runtime.to_read_model()["visible_on_child_device_required"] is True


def test_child_device_audit_runtime_rejects_duplicate_event() -> None:
    runtime = ChildDeviceAuditRuntime()
    runtime.append(_event())

    with pytest.raises(ValueError, match="audit event already exists"):
        runtime.append(_event())
