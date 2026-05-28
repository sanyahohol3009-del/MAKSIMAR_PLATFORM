import pytest

from ANDROID_SHELL.screen_observer_client.android_screen_observer_client import (
    AndroidScreenObserverClient,
)


def test_android_normal_observer_cannot_enable_child_control_smoke() -> None:
    with pytest.raises(ValueError, match="normal Android observer cannot enable child control"):
        AndroidScreenObserverClient(
            device_id="android_device_001",
            owner_identity_id="owner_001",
            device_type="android",
            read_only=True,
            consent_required=True,
            audit_required=True,
            frame_reference_only=True,
            direct_screen_capture_allowed=False,
            screenshot_runtime_allowed=False,
            screen_recording_runtime_allowed=False,
            media_projection_allowed=False,
            accessibility_service_allowed=False,
            remote_control_allowed=False,
            child_control_enabled=True,
            touch_injection_allowed=False,
            keyboard_injection_allowed=False,
            gesture_injection_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )
