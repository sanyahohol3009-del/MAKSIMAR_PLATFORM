from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_audit_contract import (
    ChildDeviceAuditContract,
)


@dataclass(frozen=True)
class IOSChildDeviceAuditBridge:
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
    ios_platform_api_call_allowed: bool
    runtime_execution_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("audit_event_id", "child_device_id", "guardian_id", "action"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

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
        if self.ios_platform_api_call_allowed:
            raise ValueError("ios_platform_api_call_allowed must be False")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")

    def build_audit_contract(self) -> ChildDeviceAuditContract:
        return ChildDeviceAuditContract(
            audit_event_id=self.audit_event_id,
            child_device_id=self.child_device_id,
            guardian_id=self.guardian_id,
            action=self.action,
            event_epoch_ms=self.event_epoch_ms,
            append_only=self.append_only,
            visible_to_guardian=self.visible_to_guardian,
            visible_on_child_device=self.visible_on_child_device,
            contains_pixel_payload=self.contains_pixel_payload,
            dashboard_bypass_allowed=self.dashboard_bypass_allowed,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "shell": "IOS_SHELL",
            "bridge": "child_device_audit",
            "audit_event_id": self.audit_event_id,
            "child_device_id": self.child_device_id,
            "guardian_id": self.guardian_id,
            "action": self.action,
            "event_epoch_ms": self.event_epoch_ms,
            "append_only": self.append_only,
            "visible_to_guardian": self.visible_to_guardian,
            "visible_on_child_device": self.visible_on_child_device,
            "contains_pixel_payload": self.contains_pixel_payload,
            "dashboard_bypass_allowed": self.dashboard_bypass_allowed,
            "ios_platform_api_call_allowed": self.ios_platform_api_call_allowed,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
        }
