import pytest

from ANDROID_SHELL.screen_observer_client.android_screen_observer_client import (
    AndroidScreenObserverClient,
)
from MAKSIMAR_CORE_LIB.mobile_screen_observer.mobile_screen_session_contract import (
    MobileScreenSessionContract,
)


def test_android_screen_observer_client_smoke() -> None:
    client = AndroidScreenObserverClient.default(
        device_id="android_device_001",
        owner_identity_id="owner_001",
    )

    session = client.build_session_contract(session_id="android_screen_session_001")
    read_model = client.to_read_model()

    assert isinstance(session, MobileScreenSessionContract)
    assert session.session_id == "android_screen_session_001"
    assert session.device_id == "android_device_001"
    assert session.device_type == "android"
    assert session.read_only is True
    assert session.frame_reference_only is True
    assert session.direct_screen_capture_allowed is False
    assert session.remote_control_allowed is False
    assert session.touch_injection_allowed is False
    assert session.keyboard_injection_allowed is False
    assert session.external_network_access_allowed is False
    assert session.runtime_mutation_allowed is False
    assert session.core_write_allowed is False
    assert session.source_of_truth_override_allowed is False

    assert read_model["shell"] == "ANDROID_SHELL"
    assert read_model["client"] == "screen_observer_client"
    assert read_model["read_only"] is True
    assert read_model["child_control_enabled"] is False
    assert read_model["media_projection_allowed"] is False
    assert read_model["accessibility_service_allowed"] is False


def test_android_screen_observer_client_rejects_child_control() -> None:
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


def test_android_screen_observer_client_rejects_direct_capture() -> None:
    with pytest.raises(ValueError, match="direct_screen_capture_allowed must be False"):
        AndroidScreenObserverClient(
            device_id="android_device_001",
            owner_identity_id="owner_001",
            device_type="android",
            read_only=True,
            consent_required=True,
            audit_required=True,
            frame_reference_only=True,
            direct_screen_capture_allowed=True,
            screenshot_runtime_allowed=False,
            screen_recording_runtime_allowed=False,
            media_projection_allowed=False,
            accessibility_service_allowed=False,
            remote_control_allowed=False,
            child_control_enabled=False,
            touch_injection_allowed=False,
            keyboard_injection_allowed=False,
            gesture_injection_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )
