from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_DEVICE_TYPES = ("android", "ios")
_ALLOWED_SESSION_STATES = ("declared", "consent_required", "active_reference", "paused", "blocked", "ended")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_allowed(value: str, field_name: str, allowed: Tuple[str, ...]) -> str:
    value = _ensure_non_empty(value, field_name)
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {allowed}: {value}")
    return value


@dataclass(frozen=True)
class MobileScreenSessionContract:
    """Read-only mobile screen observer session contract.

    This is metadata only. It does not start screen capture, open transport,
    mutate runtime, or control a device.
    """

    session_id: str
    device_id: str
    owner_identity_id: str
    device_type: str
    session_state: str
    consent_required: bool
    audit_required: bool
    read_only: bool
    frame_reference_only: bool
    direct_screen_capture_allowed: bool
    remote_control_allowed: bool
    touch_injection_allowed: bool
    keyboard_injection_allowed: bool
    external_network_access_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool
    source_of_truth_override_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "session_id", _ensure_non_empty(self.session_id, "session_id"))
        object.__setattr__(self, "device_id", _ensure_non_empty(self.device_id, "device_id"))
        object.__setattr__(
            self,
            "owner_identity_id",
            _ensure_non_empty(self.owner_identity_id, "owner_identity_id"),
        )
        object.__setattr__(
            self,
            "device_type",
            _ensure_allowed(self.device_type, "device_type", _ALLOWED_DEVICE_TYPES),
        )
        object.__setattr__(
            self,
            "session_state",
            _ensure_allowed(self.session_state, "session_state", _ALLOWED_SESSION_STATES),
        )

        if not self.consent_required:
            raise ValueError("consent_required must be True")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.frame_reference_only:
            raise ValueError("frame_reference_only must be True")
        if self.direct_screen_capture_allowed:
            raise ValueError("direct_screen_capture_allowed must be False")
        if self.remote_control_allowed:
            raise ValueError("remote_control_allowed must be False")
        if self.touch_injection_allowed:
            raise ValueError("touch_injection_allowed must be False")
        if self.keyboard_injection_allowed:
            raise ValueError("keyboard_injection_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")
        if self.source_of_truth_override_allowed:
            raise ValueError("source_of_truth_override_allowed must be False")
