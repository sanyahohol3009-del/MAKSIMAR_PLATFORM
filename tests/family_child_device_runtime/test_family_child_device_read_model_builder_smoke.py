from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_audit_contract import (
    ChildDeviceAuditContract,
)
from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_profile_contract import (
    ChildDeviceProfileContract,
)
from MAKSIMAR_SERVER.FAMILY_CHILD_DEVICE_RUNTIME.child_device_audit_runtime import (
    ChildDeviceAuditRuntime,
)
from MAKSIMAR_SERVER.FAMILY_CHILD_DEVICE_RUNTIME.child_device_session_registry import (
    ChildDeviceSessionRegistry,
)
from MAKSIMAR_SERVER.FAMILY_CHILD_DEVICE_RUNTIME.family_child_device_read_model_builder import (
    FamilyChildDeviceReadModelBuilder,
)


def test_family_child_device_read_model_builder_smoke() -> None:
    registry = ChildDeviceSessionRegistry()
    registry.register(
        ChildDeviceProfileContract(
            child_device_id="child_device_001",
            child_profile_id="child_profile_001",
            device_profile="child_managed_device",
            family_policy_enabled=True,
            visible_child_device_status_required=True,
            audit_required=True,
            dashboard_bypass_allowed=False,
        )
    )

    audit = ChildDeviceAuditRuntime()
    audit.append(
        ChildDeviceAuditContract(
            audit_event_id="child_audit_001",
            child_device_id="child_device_001",
            guardian_id="guardian_001",
            action="screen_view_requested",
            event_epoch_ms=1000,
            append_only=True,
            visible_to_guardian=True,
            visible_on_child_device=True,
            contains_pixel_payload=False,
            dashboard_bypass_allowed=False,
        )
    )

    read_model = FamilyChildDeviceReadModelBuilder(
        session_registry=registry,
        audit_runtime=audit,
    ).build()

    assert read_model["dashboard_section"] == "Family / Children"
    assert read_model["normal_phone_window"] is False
    assert read_model["guardian_authority_required"] is True
    assert read_model["runtime_execution_allowed"] is False
    assert read_model["platform_api_calls_allowed"] is False
