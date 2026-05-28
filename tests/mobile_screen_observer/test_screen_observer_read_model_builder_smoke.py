from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.mobile_screen_observer.mobile_screen_session_contract import (
    MobileScreenSessionContract,
)
from MAKSIMAR_SERVER.MOBILE_SCREEN_OBSERVER_RUNTIME.mobile_screen_observer_session_registry import (
    MobileScreenObserverSessionRegistry,
)
from MAKSIMAR_SERVER.MOBILE_SCREEN_OBSERVER_RUNTIME.screen_frame_ingest_runtime import (
    ScreenFrameIngestRuntime,
)
from MAKSIMAR_SERVER.MOBILE_SCREEN_OBSERVER_RUNTIME.screen_observer_read_model_builder import (
    ScreenObserverReadModelBuilder,
)


@dataclass(frozen=True)
class FrameReference:
    session_id: str = "screen_session_001"
    frame_ref: str = "artifact://screen/frame/001"
    inline_binary_payload_present: bool = False
    pixel_decode_allowed: bool = False
    screenshot_capture_allowed: bool = False
    screen_recording_allowed: bool = False


def test_screen_observer_read_model_builder_smoke() -> None:
    registry = MobileScreenObserverSessionRegistry()
    registry.register(
        MobileScreenSessionContract(
            session_id="screen_session_001",
            device_id="adult_device_001",
            owner_identity_id="owner_001",
            device_type="android",
            session_state="consent_required",
            consent_required=True,
            audit_required=True,
            read_only=True,
            frame_reference_only=True,
            direct_screen_capture_allowed=False,
            remote_control_allowed=False,
            touch_injection_allowed=False,
            keyboard_injection_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
            source_of_truth_override_allowed=False,
        )
    )

    frame_runtime = ScreenFrameIngestRuntime()
    frame_runtime.ingest_reference(FrameReference())

    read_model = ScreenObserverReadModelBuilder(
        session_registry=registry,
        frame_runtime=frame_runtime,
    ).build()

    assert read_model["panel"] == "phone_window"
    assert read_model["read_only"] is True
    assert read_model["child_control_enabled"] is False
    assert read_model["screen_capture_runtime_enabled"] is False
