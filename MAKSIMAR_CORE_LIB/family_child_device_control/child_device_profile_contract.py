from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChildDeviceProfileContract:
    child_device_id: str
    child_profile_id: str
    device_profile: str
    family_policy_enabled: bool
    visible_child_device_status_required: bool
    audit_required: bool
    dashboard_bypass_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("child_device_id", "child_profile_id"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")
        if self.device_profile != "child_managed_device":
            raise ValueError("device_profile must be child_managed_device")
        if not self.family_policy_enabled:
            raise ValueError("family_policy_enabled must be True")
        if not self.visible_child_device_status_required:
            raise ValueError("visible_child_device_status_required must be True")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if self.dashboard_bypass_allowed:
            raise ValueError("dashboard_bypass_allowed must be False")

    def is_child_managed(self) -> bool:
        return True
