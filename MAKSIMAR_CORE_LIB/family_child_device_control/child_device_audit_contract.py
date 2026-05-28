from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChildDeviceAuditContract:
    audit_event_id: str
    child_device_id: str
    guardian_id: str
    action: str
    event_epoch_ms: int
    append_only: bool
    visible_to_guardian: bool
    visible_on_child_device: bool
    contains_pixel_payload: bool
    dashboard_bypass_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("audit_event_id", "child_device_id", "guardian_id", "action"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")
        if not isinstance(self.event_epoch_ms, int) or self.event_epoch_ms < 0:
            raise ValueError("event_epoch_ms must be a non-negative integer")
        if not self.append_only:
            raise ValueError("append_only must be True")
        if not self.visible_to_guardian:
            raise ValueError("visible_to_guardian must be True")
        if not self.visible_on_child_device:
            raise ValueError("visible_on_child_device must be True")
        if self.contains_pixel_payload:
            raise ValueError("contains_pixel_payload must be False")
        if self.dashboard_bypass_allowed:
            raise ValueError("dashboard_bypass_allowed must be False")
