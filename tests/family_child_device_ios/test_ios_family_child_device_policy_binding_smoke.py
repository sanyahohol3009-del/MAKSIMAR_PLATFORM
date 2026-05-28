from IOS_SHELL.family_child_device.ios_child_app_control_policy_bridge import (
    IOSChildAppControlPolicyBridge,
)
from IOS_SHELL.family_child_device.ios_child_device_audit_bridge import (
    IOSChildDeviceAuditBridge,
)
from IOS_SHELL.family_child_device.ios_child_device_profile_bridge import (
    IOSChildDeviceProfileBridge,
)
from IOS_SHELL.family_child_device.ios_child_remote_control_intent_bridge import (
    IOSChildRemoteControlIntentBridge,
)
from IOS_SHELL.family_child_device.ios_child_screen_control_policy_bridge import (
    IOSChildScreenControlPolicyBridge,
)
from IOS_SHELL.family_child_device.ios_child_screen_time_policy_bridge import (
    IOSChildScreenTimePolicyBridge,
)
from IOS_SHELL.family_child_device.ios_family_child_device_policy_binding import (
    IOSFamilyChildDevicePolicyBinding,
)
from IOS_SHELL.family_child_device.ios_guardian_authority_bridge import (
    IOSGuardianAuthorityBridge,
)


def _binding() -> IOSFamilyChildDevicePolicyBinding:
    return IOSFamilyChildDevicePolicyBinding(
        profile_bridge=IOSChildDeviceProfileBridge.default(
            child_device_id="child_ios_device_001",
            child_profile_id="child_profile_001",
        ),
        guardian_authority_bridge=IOSGuardianAuthorityBridge(
            guardian_id="guardian_001",
            child_profile_id="child_profile_001",
            guardian_authority_verified=True,
            authority_scope="family_child_device_control",
            audit_required=True,
            expires_epoch_ms=999999,
            dashboard_bypass_allowed=False,
            ios_platform_api_call_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        ),
        screen_control_policy_bridge=IOSChildScreenControlPolicyBridge(
            policy_id="ios_child_screen_policy_001",
            device_profile="child_managed_device",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            audit_required=True,
            visible_child_device_status_required=True,
            dashboard_bypass_allowed=False,
            screen_view_allowed_by_guardian_policy=True,
            screenshot_allowed_by_guardian_policy=True,
            screen_recording_allowed_by_guardian_policy=False,
            touch_control_allowed_by_guardian_policy=True,
            keyboard_input_allowed_by_guardian_policy=False,
            ios_platform_api_call_allowed=False,
            screen_capture_runtime_allowed=False,
            touch_execution_allowed=False,
            keyboard_execution_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        ),
        remote_control_intent_bridge=IOSChildRemoteControlIntentBridge(
            intent_id="ios_child_remote_intent_001",
            child_device_id="child_ios_device_001",
            guardian_id="guardian_001",
            intent_type="touch_control",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            audit_required=True,
            visible_child_device_status_required=True,
            dashboard_bypass_allowed=False,
            ios_platform_api_call_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        ),
        audit_bridge=IOSChildDeviceAuditBridge(
            audit_event_id="ios_child_audit_001",
            child_device_id="child_ios_device_001",
            guardian_id="guardian_001",
            action="touch_control_requested",
            event_epoch_ms=1000,
            append_only=True,
            visible_to_guardian=True,
            visible_on_child_device=True,
            contains_pixel_payload=False,
            dashboard_bypass_allowed=False,
            ios_platform_api_call_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        ),
        app_control_policy_bridge=IOSChildAppControlPolicyBridge(
            policy_id="ios_child_app_policy_001",
            child_device_id="child_ios_device_001",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            app_blocking_allowed_by_guardian_policy=True,
            install_approval_required=True,
            audit_required=True,
            dashboard_bypass_allowed=False,
            ios_platform_api_call_allowed=False,
            app_control_runtime_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        ),
        screen_time_policy_bridge=IOSChildScreenTimePolicyBridge(
            policy_id="ios_child_time_policy_001",
            child_device_id="child_ios_device_001",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            daily_limit_minutes=90,
            emergency_lock_allowed_by_guardian_policy=True,
            audit_required=True,
            dashboard_bypass_allowed=False,
            ios_platform_api_call_allowed=False,
            screen_time_enforcement_runtime_allowed=False,
            emergency_lock_runtime_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        ),
        dashboard_section="Family / Children",
        policy_projection_only=True,
        ios_platform_api_call_allowed=False,
        runtime_execution_allowed=False,
        dashboard_bypass_allowed=False,
        normal_observer_client_allowed=False,
    )


def test_ios_family_child_device_policy_binding_smoke() -> None:
    binding = _binding()
    read_model = binding.to_read_model()

    assert read_model["shell"] == "IOS_SHELL"
    assert read_model["binding"] == "family_child_device_policy"
    assert read_model["dashboard_section"] == "Family / Children"
    assert read_model["policy_projection_only"] is True
    assert read_model["ios_platform_api_call_allowed"] is False
    assert read_model["runtime_execution_allowed"] is False
    assert read_model["dashboard_bypass_allowed"] is False
    assert read_model["normal_observer_client_allowed"] is False
    assert read_model["profile"]["child_device_id"] == "child_ios_device_001"
    assert read_model["guardian_authority"]["guardian_id"] == "guardian_001"
