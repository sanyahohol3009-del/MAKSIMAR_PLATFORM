from ANDROID_SHELL.family_child_device.android_child_app_control_policy_bridge import (
    AndroidChildAppControlPolicyBridge,
)
from ANDROID_SHELL.family_child_device.android_child_device_audit_bridge import (
    AndroidChildDeviceAuditBridge,
)
from ANDROID_SHELL.family_child_device.android_child_device_profile_bridge import (
    AndroidChildDeviceProfileBridge,
)
from ANDROID_SHELL.family_child_device.android_child_remote_control_intent_bridge import (
    AndroidChildRemoteControlIntentBridge,
)
from ANDROID_SHELL.family_child_device.android_child_screen_control_policy_bridge import (
    AndroidChildScreenControlPolicyBridge,
)
from ANDROID_SHELL.family_child_device.android_child_screen_time_policy_bridge import (
    AndroidChildScreenTimePolicyBridge,
)
from ANDROID_SHELL.family_child_device.android_family_child_device_policy_binding import (
    AndroidFamilyChildDevicePolicyBinding,
)
from ANDROID_SHELL.family_child_device.android_guardian_authority_bridge import (
    AndroidGuardianAuthorityBridge,
)


def _binding() -> AndroidFamilyChildDevicePolicyBinding:
    return AndroidFamilyChildDevicePolicyBinding(
        profile_bridge=AndroidChildDeviceProfileBridge.default(
            child_device_id="child_android_device_001",
            child_profile_id="child_profile_001",
        ),
        guardian_authority_bridge=AndroidGuardianAuthorityBridge(
            guardian_id="guardian_001",
            child_profile_id="child_profile_001",
            guardian_authority_verified=True,
            authority_scope="family_child_device_control",
            audit_required=True,
            expires_epoch_ms=999999,
            dashboard_bypass_allowed=False,
            android_platform_api_call_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        ),
        screen_control_policy_bridge=AndroidChildScreenControlPolicyBridge(
            policy_id="android_child_screen_policy_001",
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
            android_platform_api_call_allowed=False,
            screen_capture_runtime_allowed=False,
            touch_execution_allowed=False,
            keyboard_execution_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        ),
        remote_control_intent_bridge=AndroidChildRemoteControlIntentBridge(
            intent_id="android_child_remote_intent_001",
            child_device_id="child_android_device_001",
            guardian_id="guardian_001",
            intent_type="touch_control",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            audit_required=True,
            visible_child_device_status_required=True,
            dashboard_bypass_allowed=False,
            android_platform_api_call_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        ),
        audit_bridge=AndroidChildDeviceAuditBridge(
            audit_event_id="android_child_audit_001",
            child_device_id="child_android_device_001",
            guardian_id="guardian_001",
            action="touch_control_requested",
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
        ),
        app_control_policy_bridge=AndroidChildAppControlPolicyBridge(
            policy_id="android_child_app_policy_001",
            child_device_id="child_android_device_001",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            app_blocking_allowed_by_guardian_policy=True,
            install_approval_required=True,
            audit_required=True,
            dashboard_bypass_allowed=False,
            android_platform_api_call_allowed=False,
            app_control_runtime_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        ),
        screen_time_policy_bridge=AndroidChildScreenTimePolicyBridge(
            policy_id="android_child_time_policy_001",
            child_device_id="child_android_device_001",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            daily_limit_minutes=90,
            emergency_lock_allowed_by_guardian_policy=True,
            audit_required=True,
            dashboard_bypass_allowed=False,
            android_platform_api_call_allowed=False,
            screen_time_enforcement_runtime_allowed=False,
            emergency_lock_runtime_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        ),
        dashboard_section="Family / Children",
        policy_projection_only=True,
        android_platform_api_call_allowed=False,
        runtime_execution_allowed=False,
        dashboard_bypass_allowed=False,
        normal_observer_client_allowed=False,
    )


def test_android_family_child_device_policy_binding_smoke() -> None:
    binding = _binding()
    read_model = binding.to_read_model()

    assert read_model["shell"] == "ANDROID_SHELL"
    assert read_model["binding"] == "family_child_device_policy"
    assert read_model["dashboard_section"] == "Family / Children"
    assert read_model["policy_projection_only"] is True
    assert read_model["android_platform_api_call_allowed"] is False
    assert read_model["runtime_execution_allowed"] is False
    assert read_model["dashboard_bypass_allowed"] is False
    assert read_model["normal_observer_client_allowed"] is False
    assert read_model["profile"]["child_device_id"] == "child_android_device_001"
    assert read_model["guardian_authority"]["guardian_id"] == "guardian_001"
