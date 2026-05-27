from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_FRAME_STATES = ("metadata_declared", "reference_available", "quarantine_required", "blocked")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")
    return value


@dataclass(frozen=True)
class MobileScreenFrameContract:
    """Metadata/reference-only phone screen frame contract.

    The frame payload is not stored inline. This contract never captures,
    decodes, renders, streams, or transmits pixels.
    """

    frame_id: str
    session_id: str
    frame_state: str
    frame_ref: str
    width: int
    height: int
    sequence_number: int
    captured_at_epoch_ms: int
    metadata_only: bool
    inline_binary_payload_allowed: bool
    pixel_decode_allowed: bool
    screen_recording_allowed: bool
    screenshot_capture_allowed: bool
    external_network_access_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "frame_id", _ensure_non_empty(self.frame_id, "frame_id"))
        object.__setattr__(self, "session_id", _ensure_non_empty(self.session_id, "session_id"))
        object.__setattr__(self, "frame_ref", _ensure_non_empty(self.frame_ref, "frame_ref"))
        if self.frame_state not in _ALLOWED_FRAME_STATES:
            raise ValueError(f"frame_state must be one of {_ALLOWED_FRAME_STATES}: {self.frame_state}")
        object.__setattr__(self, "width", _ensure_non_negative_int(self.width, "width"))
        object.__setattr__(self, "height", _ensure_non_negative_int(self.height, "height"))
        object.__setattr__(
            self,
            "sequence_number",
            _ensure_non_negative_int(self.sequence_number, "sequence_number"),
        )
        object.__setattr__(
            self,
            "captured_at_epoch_ms",
            _ensure_non_negative_int(self.captured_at_epoch_ms, "captured_at_epoch_ms"),
        )

        if self.width == 0:
            raise ValueError("width must be greater than zero")
        if self.height == 0:
            raise ValueError("height must be greater than zero")
        if not self.metadata_only:
            raise ValueError("metadata_only must be True")
        if self.inline_binary_payload_allowed:
            raise ValueError("inline_binary_payload_allowed must be False")
        if self.pixel_decode_allowed:
            raise ValueError("pixel_decode_allowed must be False")
        if self.screen_recording_allowed:
            raise ValueError("screen_recording_allowed must be False")
        if self.screenshot_capture_allowed:
            raise ValueError("screenshot_capture_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")
