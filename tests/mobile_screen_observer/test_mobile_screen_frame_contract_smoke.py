import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.mobile_screen_frame_contract import (
    MobileScreenFrameContract,
)


def test_mobile_screen_frame_contract_smoke() -> None:
    frame = MobileScreenFrameContract(
        frame_id="frame_001",
        session_id="screen_session_001",
        frame_state="reference_available",
        frame_ref="artifact://screen/frame_001",
        width=1080,
        height=2400,
        sequence_number=1,
        captured_at_epoch_ms=1000,
        metadata_only=True,
        inline_binary_payload_allowed=False,
        pixel_decode_allowed=False,
        screen_recording_allowed=False,
        screenshot_capture_allowed=False,
        external_network_access_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
    )

    assert frame.metadata_only is True
    assert frame.inline_binary_payload_allowed is False


def test_mobile_screen_frame_rejects_inline_binary_payload() -> None:
    with pytest.raises(ValueError, match="inline_binary_payload_allowed must be False"):
        MobileScreenFrameContract(
            frame_id="frame_bad",
            session_id="screen_session_001",
            frame_state="reference_available",
            frame_ref="artifact://screen/frame_bad",
            width=1080,
            height=2400,
            sequence_number=1,
            captured_at_epoch_ms=1000,
            metadata_only=True,
            inline_binary_payload_allowed=True,
            pixel_decode_allowed=False,
            screen_recording_allowed=False,
            screenshot_capture_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )


def test_mobile_screen_frame_rejects_screenshot_capture() -> None:
    with pytest.raises(ValueError, match="screenshot_capture_allowed must be False"):
        MobileScreenFrameContract(
            frame_id="frame_screenshot_bad",
            session_id="screen_session_001",
            frame_state="reference_available",
            frame_ref="artifact://screen/frame_bad",
            width=1080,
            height=2400,
            sequence_number=1,
            captured_at_epoch_ms=1000,
            metadata_only=True,
            inline_binary_payload_allowed=False,
            pixel_decode_allowed=False,
            screen_recording_allowed=False,
            screenshot_capture_allowed=True,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
