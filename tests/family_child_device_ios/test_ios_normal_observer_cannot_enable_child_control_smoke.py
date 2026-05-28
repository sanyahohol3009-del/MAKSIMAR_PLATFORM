import pytest

from IOS_SHELL.screen_observer_client.ios_screen_observer_client import (
    IOSScreenObserverClient,
)


def test_ios_normal_observer_cannot_enable_child_control_smoke() -> None:
    with pytest.raises(ValueError, match="normal iOS observer cannot enable child control"):
        IOSScreenObserverClient(
            device_id="ios_device_001",
            owner_identity_id="owner_001",
            device_type="ios",
            read_only=True,
            consent_required=True,
            audit_required=True,
            frame_reference_only=True,
            direct_screen_capture_allowed=False,
            screenshot_runtime_allowed=False,
            screen_recording_runtime_allowed=False,
            replaykit_allowed=False,
            accessibility_api_allowed=False,
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
