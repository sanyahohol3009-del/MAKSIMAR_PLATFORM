from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_INTENTS = ("screen_view", "screenshot", "screen_recording", "touch_control", "keyboard_input", "app_block", "screen_time_limit", "emergency_lock")


@dataclass(frozen=True)
class ChildRemoteControlIntentContract:
    intent_id: str
    child_device_id: str
    guardian_id: str
    intent_type: str
    guardian_authority_verified: bool
    family_policy_enabled: bool
    audit_required: bool
    visible_child_device_status_required: bool
    dashboard_bypass_allowed: bool
    runtime_execution_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("intent_id", "child_device_id", "guardian_id"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")
        if self.intent_type not in _ALLOWED_INTENTS:
            raise ValueError(f"intent_type must be one of {_ALLOWED_INTENTS}")
        if not self.guardian_authority_verified:
            raise ValueError("guardian_authority_verified must be True")
        if not self.family_policy_enabled:
            raise ValueError("family_policy_enabled must be True")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if not self.visible_child_device_status_required:
            raise ValueError("visible_child_device_status_required must be True")
        if self.dashboard_bypass_allowed:
            raise ValueError("dashboard_bypass_allowed must be False")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False in BATCH 4.2")

    def is_policy_intent_only(self) -> bool:
        return True
