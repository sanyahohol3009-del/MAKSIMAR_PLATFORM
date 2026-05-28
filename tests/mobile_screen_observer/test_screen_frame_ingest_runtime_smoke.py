from dataclasses import dataclass

import pytest

from MAKSIMAR_SERVER.MOBILE_SCREEN_OBSERVER_RUNTIME.screen_frame_ingest_runtime import (
    ScreenFrameIngestRuntime,
)


@dataclass(frozen=True)
class FrameReference:
    session_id: str = "screen_session_001"
    frame_ref: str = "artifact://screen/frame/001"
    inline_binary_payload_present: bool = False
    pixel_decode_allowed: bool = False
    screenshot_capture_allowed: bool = False
    screen_recording_allowed: bool = False


def test_screen_frame_ingest_runtime_smoke() -> None:
    runtime = ScreenFrameIngestRuntime()
    result = runtime.ingest_reference(FrameReference())

    assert result.accepted is True
    assert result.reason == "metadata_reference_accepted"
    assert runtime.list_refs_for_session("screen_session_001") == ("artifact://screen/frame/001",)
    assert runtime.to_read_model()["pixel_payloads_accepted"] is False


def test_screen_frame_ingest_rejects_inline_binary_payload() -> None:
    runtime = ScreenFrameIngestRuntime()

    with pytest.raises(ValueError, match="inline binary payload is forbidden"):
        runtime.ingest_reference(FrameReference(inline_binary_payload_present=True))
