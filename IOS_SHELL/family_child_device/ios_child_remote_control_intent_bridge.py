from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.family_child_device_control.child_remote_control_intent_contract import (
    ChildRemoteControlIntentContract,
)


_ALLOWED_INTENTS: tuple[str, ...] = (
    "screen_view",
    "screenshot",
    "screen_recording",
    "touch_control",
    "keyboard_input",
    "app_block",
    "screen_time_limit",
    "emergency_lock",
)


@dataclass(frozen=True)
class IOSChildRemoteControlIntentBridge:
    intent_id: str
    child_device_id: str
    guardian_id: str
    intent_type: str
    guardian_authority_verified: bool
    family_policy_enabled: bool
    audit_required: bool
    visible_child_device_status_required: bool
    dashboard_bypass_allowed: bool
    ios_platform_api_call_allowed: bool
    runtime_execution_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("intent_id", "child_device_id", "guardian_id", "intent_type"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if self.intent_type not in _ALLOWED_INTENTS:
            raise ValueError(f"unsupported intent_type: {self.intent_type}")
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
        if self.ios_platform_api_call_allowed:
            raise ValueError("ios_platform_api_call_allowed must be False")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")

    def build_intent_contract(self) -> ChildRemoteControlIntentContract:
        return ChildRemoteControlIntentContract(
            intent_id=self.intent_id,
            child_device_id=self.child_device_id,
            guardian_id=self.guardian_id,
            intent_type=self.intent_type,
            guardian_authority_verified=self.guardian_authority_verified,
            family_policy_enabled=self.family_policy_enabled,
            audit_required=self.audit_required,
            visible_child_device_status_required=self.visible_child_device_status_required,
            dashboard_bypass_allowed=self.dashboard_bypass_allowed,
            runtime_execution_allowed=self.runtime_execution_allowed,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "shell": "IOS_SHELL",
            "bridge": "child_remote_control_intent",
            "intent_id": self.intent_id,
            "child_device_id": self.child_device_id,
            "guardian_id": self.guardian_id,
            "intent_type": self.intent_type,
            "guardian_authority_verified": self.guardian_authority_verified,
            "family_policy_enabled": self.family_policy_enabled,
            "audit_required": self.audit_required,
            "visible_child_device_status_required": self.visible_child_device_status_required,
            "dashboard_bypass_allowed": self.dashboard_bypass_allowed,
            "ios_platform_api_call_allowed": self.ios_platform_api_call_allowed,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
        }
