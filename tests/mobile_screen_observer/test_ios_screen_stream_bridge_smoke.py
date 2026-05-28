import pytest

from IOS_SHELL.screen_observer_client.ios_screen_stream_bridge import (
    IOSScreenFrameReference,
    IOSScreenStreamBridge,
)


def test_ios_screen_stream_bridge_smoke() -> None:
    bridge = IOSScreenStreamBridge.default(
        device_id="ios_device_001",
        session_id="ios_screen_session_001",
    )

    frame = bridge.build_frame_reference(
        frame_ref="artifact://ios/screen/frame/001",
        sequence_index=1,
        created_epoch_ms=1000,
    )

    payload = frame.to_server_ingest_payload()
    read_model = bridge.to_read_model()

    assert isinstance(frame, IOSScreenFrameReference)
    assert payload["session_id"] == "ios_screen_session_001"
    assert payload["device_id"] == "ios_device_001"
    assert payload["frame_ref"] == "artifact://ios/screen/frame/001"
    assert payload["metadata_reference_only"] is True
    assert payload["inline_binary_payload_present"] is False
    assert payload["pixel_decode_allowed"] is False
    assert payload["screenshot_capture_allowed"] is False
    assert payload["screen_recording_allowed"] is False
    assert payload["replaykit_allowed"] is False
    assert payload["ios_platform_api_call_allowed"] is False
    assert payload["network_upload_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["core_write_allowed"] is False

    assert read_model["bridge"] == "screen_stream"
    assert read_model["metadata_reference_only"] is True
    assert read_model["child_control_enabled"] is False


def test_ios_screen_stream_bridge_rejects_child_control() -> None:
    with pytest.raises(ValueError, match="normal iOS screen stream cannot enable child control"):
        IOSScreenStreamBridge(
            device_id="ios_device_001",
            session_id="ios_screen_session_001",
            metadata_reference_only=True,
            ios_platform_api_call_allowed=False,
            network_upload_allowed=False,
            child_control_enabled=True,
        )


def test_ios_screen_frame_reference_rejects_inline_payload() -> None:
    with pytest.raises(ValueError, match="inline_binary_payload_present must be False"):
        IOSScreenFrameReference(
            session_id="ios_screen_session_001",
            device_id="ios_device_001",
            frame_ref="artifact://ios/screen/frame/001",
            sequence_index=1,
            created_epoch_ms=1000,
            metadata_reference_only=True,
            inline_binary_payload_present=True,
            pixel_decode_allowed=False,
            screenshot_capture_allowed=False,
            screen_recording_allowed=False,
            replaykit_allowed=False,
            ios_platform_api_call_allowed=False,
            network_upload_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
