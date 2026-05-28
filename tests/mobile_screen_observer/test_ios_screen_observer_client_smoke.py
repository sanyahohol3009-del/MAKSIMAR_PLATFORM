import pytest

from IOS_SHELL.screen_observer_client.ios_screen_observer_client import (
    IOSScreenObserverClient,
)
from MAKSIMAR_CORE_LIB.mobile_screen_observer.mobile_screen_session_contract import (
    MobileScreenSessionContract,
)


def test_ios_screen_observer_client_smoke() -> None:
    client = IOSScreenObserverClient.default(
        device_id="ios_device_001",
        owner_identity_id="owner_001",
    )

    session = client.build_session_contract(session_id="ios_screen_session_001")
    read_model = client.to_read_model()

    assert isinstance(session, MobileScreenSessionContract)
    assert session.session_id == "ios_screen_session_001"
    assert session.device_id == "ios_device_001"
    assert session.device_type == "ios"
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

    assert read_model["shell"] == "IOS_SHELL"
    assert read_model["client"] == "screen_observer_client"
    assert read_model["read_only"] is True
    assert read_model["child_control_enabled"] is False
    assert read_model["replaykit_allowed"] is False
    assert read_model["accessibility_api_allowed"] is False


def test_ios_screen_observer_client_rejects_child_control() -> None:
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


def test_ios_screen_observer_client_rejects_replaykit() -> None:
    with pytest.raises(ValueError, match="replaykit_allowed must be False"):
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
            replaykit_allowed=True,
            accessibility_api_allowed=False,
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
