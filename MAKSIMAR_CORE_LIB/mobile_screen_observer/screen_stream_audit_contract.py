from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_AUDIT_ACTIONS = ("session_declared", "consent_requested", "consent_granted", "frame_reference_seen", "remote_assistance_requested", "blocked")


@dataclass(frozen=True)
class ScreenStreamAuditContract:
    """Append-only audit event contract for screen observer references."""

    audit_event_id: str
    session_id: str
    action: str
    actor_id: str
    device_id: str
    event_epoch_ms: int
    append_only: bool
    visible_to_owner: bool
    contains_pixel_payload: bool
    contains_secret: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("audit_event_id", "session_id", "actor_id", "device_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be non-empty")
        if self.action not in _ALLOWED_AUDIT_ACTIONS:
            raise ValueError(f"action must be one of {_ALLOWED_AUDIT_ACTIONS}")
        if not isinstance(self.event_epoch_ms, int) or self.event_epoch_ms < 0:
            raise ValueError("event_epoch_ms must be a non-negative integer")
        if not self.append_only:
            raise ValueError("append_only must be True")
        if not self.visible_to_owner:
            raise ValueError("visible_to_owner must be True")
        if self.contains_pixel_payload:
            raise ValueError("contains_pixel_payload must be False")
        if self.contains_secret:
            raise ValueError("contains_secret must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")
