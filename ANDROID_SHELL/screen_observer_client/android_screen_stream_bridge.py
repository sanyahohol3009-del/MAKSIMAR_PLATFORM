from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AndroidScreenFrameReference:
    session_id: str
    device_id: str
    frame_ref: str
    sequence_index: int
    created_epoch_ms: int
    metadata_reference_only: bool
    inline_binary_payload_present: bool
    pixel_decode_allowed: bool
    screenshot_capture_allowed: bool
    screen_recording_allowed: bool
    media_projection_allowed: bool
    android_platform_api_call_allowed: bool
    network_upload_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("session_id", "device_id", "frame_ref"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if not isinstance(self.sequence_index, int) or self.sequence_index < 0:
            raise ValueError("sequence_index must be a non-negative integer")
        if not isinstance(self.created_epoch_ms, int) or self.created_epoch_ms < 0:
            raise ValueError("created_epoch_ms must be a non-negative integer")
        if not self.metadata_reference_only:
            raise ValueError("metadata_reference_only must be True")
        if self.inline_binary_payload_present:
            raise ValueError("inline_binary_payload_present must be False")
        if self.pixel_decode_allowed:
            raise ValueError("pixel_decode_allowed must be False")
        if self.screenshot_capture_allowed:
            raise ValueError("screenshot_capture_allowed must be False")
        if self.screen_recording_allowed:
            raise ValueError("screen_recording_allowed must be False")
        if self.media_projection_allowed:
            raise ValueError("media_projection_allowed must be False")
        if self.android_platform_api_call_allowed:
            raise ValueError("android_platform_api_call_allowed must be False")
        if self.network_upload_allowed:
            raise ValueError("network_upload_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")

    def to_server_ingest_payload(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "device_id": self.device_id,
            "frame_ref": self.frame_ref,
            "sequence_index": self.sequence_index,
            "created_epoch_ms": self.created_epoch_ms,
            "metadata_reference_only": self.metadata_reference_only,
            "inline_binary_payload_present": self.inline_binary_payload_present,
            "pixel_decode_allowed": self.pixel_decode_allowed,
            "screenshot_capture_allowed": self.screenshot_capture_allowed,
            "screen_recording_allowed": self.screen_recording_allowed,
            "media_projection_allowed": self.media_projection_allowed,
            "android_platform_api_call_allowed": self.android_platform_api_call_allowed,
            "network_upload_allowed": self.network_upload_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
        }


@dataclass(frozen=True)
class AndroidScreenStreamBridge:
    device_id: str
    session_id: str
    metadata_reference_only: bool
    android_platform_api_call_allowed: bool
    network_upload_allowed: bool
    child_control_enabled: bool

    def __post_init__(self) -> None:
        for field_name in ("device_id", "session_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if not self.metadata_reference_only:
            raise ValueError("metadata_reference_only must be True")
        if self.android_platform_api_call_allowed:
            raise ValueError("android_platform_api_call_allowed must be False")
        if self.network_upload_allowed:
            raise ValueError("network_upload_allowed must be False")
        if self.child_control_enabled:
            raise ValueError("normal Android screen stream cannot enable child control")

    @classmethod
    def default(cls, *, device_id: str, session_id: str) -> "AndroidScreenStreamBridge":
        return cls(
            device_id=device_id,
            session_id=session_id,
            metadata_reference_only=True,
            android_platform_api_call_allowed=False,
            network_upload_allowed=False,
            child_control_enabled=False,
        )

    def build_frame_reference(
        self,
        *,
        frame_ref: str,
        sequence_index: int,
        created_epoch_ms: int,
    ) -> AndroidScreenFrameReference:
        return AndroidScreenFrameReference(
            session_id=self.session_id,
            device_id=self.device_id,
            frame_ref=frame_ref,
            sequence_index=sequence_index,
            created_epoch_ms=created_epoch_ms,
            metadata_reference_only=self.metadata_reference_only,
            inline_binary_payload_present=False,
            pixel_decode_allowed=False,
            screenshot_capture_allowed=False,
            screen_recording_allowed=False,
            media_projection_allowed=False,
            android_platform_api_call_allowed=self.android_platform_api_call_allowed,
            network_upload_allowed=self.network_upload_allowed,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "shell": "ANDROID_SHELL",
            "bridge": "screen_stream",
            "device_id": self.device_id,
            "session_id": self.session_id,
            "metadata_reference_only": self.metadata_reference_only,
            "android_platform_api_call_allowed": self.android_platform_api_call_allowed,
            "network_upload_allowed": self.network_upload_allowed,
            "child_control_enabled": self.child_control_enabled,
        }
